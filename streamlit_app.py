import streamlit as st
import pytesseract
from PIL import Image, ImageEnhance
from streamlit_cropper import st_cropper
import sympy as sp

st.set_page_config(page_title="Math Scanner Pro", page_icon="🔢")

st.title("🔢 Pro Math Scanner")
st.write("Crop the image to focus on the equation!")

# 1. Capture the image
img_file = st.camera_input("Take a photo")

if img_file:
    img = Image.open(img_file)
    
    # 2. THE CROPPER: This lets you select just the math
    st.write("### Step 1: Drag the box to crop your equation")
    cropped_img = st_cropper(img, realtime_update=True, box_color='#00FF00', aspect_ratio=None)
    
    # 3. GRID FIX: Boost contrast to make the grid disappear
    # We make the ink super dark and the paper/grid super bright
    enhancer = ImageEnhance.Contrast(cropped_img)
    processed_img = enhancer.enhance(2.5) # Increase contrast 2.5x
    
    st.image(processed_img, caption="What the AI sees", width=300)

    if st.button("Solve Crop"):
        with st.spinner('Reading...'):
            # Math Glasses config
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789+-*/()'
            raw_text = pytesseract.image_to_string(processed_img, config=custom_config)
            clean_text = raw_text.strip().replace(" ", "").lower()

        st.subheader(f"Detected: {clean_text}")

        try:
            if clean_text:
                answer = sp.sympify(clean_text)
                st.success(f"✅ The Answer is: {answer}")
            else:
                st.warning("Empty crop! Try again.")
        except:
            st.error("❌ Math error. Try cropping closer to the numbers!")
