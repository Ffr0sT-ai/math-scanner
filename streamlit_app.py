import streamlit as st
import pytesseract
from PIL import Image, ImageOps, ImageEnhance
from streamlit_cropper import st_cropper
import numpy as np
import cv2
import sympy as sp

st.set_page_config(page_title="Math Scanner Pro", page_icon="🔢")

st.title("🔢 Pro Math Scanner")
st.write("Crop it tight to the numbers to ignore the grid!")

img_file = st.camera_input("Take a photo")

if img_file:
    img = Image.open(img_file)
    
    # 1. The Cropper
    st.write("### Step 1: Crop the equation")
    cropped_img = st_cropper(img, realtime_update=True, box_color='#00FF00', aspect_ratio=None)
    
    # 2. THE GRID ERASER (Image Processing)
    # Convert to grayscale
    gray = ImageOps.grayscale(cropped_img)
    # Boost contrast massively
    enhancer = ImageEnhance.Contrast(gray)
    high_contrast = enhancer.enhance(3.0)
    
    # Convert to OpenCV format for a "Digital Bath"
    opencv_img = np.array(high_contrast)
    # This specific filter removes light-colored grid lines
    _, final_img = cv2.threshold(opencv_img, 140, 255, cv2.THRESH_BINARY)

    st.image(final_img, caption="AI's Cleaned View", width=300)

    if st.button("Solve This!"):
        with st.spinner('Reading...'):
            # Math Glasses
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789+-*/()'
            raw_text = pytesseract.image_to_string(final_img, config=custom_config)
            clean_text = raw_text.strip().replace(" ", "").lower()

        if clean_text:
            st.subheader(f"Detected: {clean_text}")
            try:
                answer = sp.sympify(clean_text)
                st.success(f"✅ The Answer is: {answer}")
            except:
                st.error(f"❌ Could read '{clean_text}' but couldn't solve it.")
        else:
            st.warning("Still seeing an empty crop. Try getting more light on the paper!")
