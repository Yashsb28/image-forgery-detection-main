import streamlit as st
from PIL import Image
from prediction import predict_result
from ela import convert_to_ela_image
import os
import imageio.v3 as iio

def show_demo():
    st.title("Demo")
    st.write("Below are some demo images with their forgery detection results.")
    
    examples_path = "demo"
    example_images = os.listdir(examples_path)
    
    for img_name in example_images:
        img_path = os.path.join(examples_path, img_name)
        img = Image.open(img_path)
        
        # Predict result
        predicted, confidence = predict_result(img)
        
        # Convert to ELA image
        ela_img = convert_to_ela_image(img, quality=90)
        
        # Display images side by side
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, caption=f"Original Image: {img_name}", use_column_width=True)
            st.write(f"Predicted: {predicted} with {confidence}% confidence")
        with col2:
            st.image(ela_img, caption="ELA Image", use_column_width=True)
