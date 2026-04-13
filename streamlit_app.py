import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import sympy as sp

st.set_page_config(page_title="Math Scanner", page_icon="🔢")

st.title("🔢 Math Equation Scanner")
st.write("Point your camera at a math problem and I'll solve it!")

# Camera Input
img_file = st.camera_input("Take a photo")

if img_file:
    img = Image.open(img_file)
    st.image(img, caption="Scanning...", use_container_width=True)
    
    # Initialize EasyOCR
    reader = easyocr.Reader(['en'])
    
    # Process image
    with st.spinner('Thinking...'):
        result = reader.readtext(np.array(img), detail=0)
        raw_text = "".join(result).replace(" ", "").lower()
        
        # Simple mapping for common handwriting mistakes
        mapping = {')': '2', 'z': '2', 's': '5', 'i': '1', 'o': '0'}
        clean_text = "".join([mapping.get(char, char) for char in raw_text])

    st.subheader(f"Detected: {clean_text}")

    try:
        # Solve using SymPy
        answer = sp.sympify(clean_text)
        st.success(f"✅ The Answer is: {answer}")
    except:
        st.error("❌ Couldn't parse that as math. Try writing more clearly!")
