import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import sympy as sp
import cv2

st.set_page_config(page_title="Math Scanner", page_icon="🔢")

st.title("🔢 Math Equation Scanner")
st.write("Point your camera at a math problem and I'll solve it!")

# 1. Camera Input
img_file = st.camera_input("Take a photo")

if img_file:
    # Load image and convert to Grayscale
    img = Image.open(img_file).convert('L')
    st.image(img, caption="Original Scan", use_container_width=True)
    
    img_np = np.array(img)
    
    # 2. AUTO-ENHANCE (The "Sharper Eyes")
    # This removes shadows and makes the ink pop
    _, img_enhanced = cv2.threshold(img_np, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Show the user what the AI is actually looking at
    st.image(img_enhanced, caption="What the AI sees", use_container_width=True)
    
    # 3. The "PRO Brain" Setup
    reader = easyocr.Reader(['en'])
    
    # Process the enhanced image
    with st.spinner('Thinking...'):
        result = reader.readtext(img_enhanced, detail=0)
        raw_text = "".join(result).replace(" ", "").lower()
        
        # Safety Net for common handwriting mistakes
        mapping = {')': '2', 'z': '2', 's': '5', 'i': '1', 'o': '0'}
        clean_text = "".join([mapping.get(char, char) for char in raw_text])

    st.subheader(f"Detected: {clean_text}")

    # 4. The Math Solver
    try:
        # A quick fix just in case they write 'x' instead of '*'
        calc_text = clean_text.replace('x', '*')
        answer = sp.sympify(calc_text)
        st.success(f"✅ The Answer is: {answer}")
    except:
        st.error("❌ Couldn't solve it. Check the 'What the AI sees' image to see what went wrong!")
