import streamlit as st

def show_about():
    st.title("About AI-Forgery Guard")
    st.write("""
    **AI-Forgery Guard** is a state-of-the-art image forgery detection tool that leverages advanced algorithms to determine the authenticity of images.
    We use techniques like Error Level Analysis (ELA) to detect inconsistencies that are indicative of manipulations.
    Our tool provides an easy-to-use interface for users to upload images and receive a detailed forgery analysis report.
    """)

    st.write("""
---

### What is Error Level Analysis (ELA)?

**Error Level Analysis (ELA)** is a digital forensic technique used to detect image manipulation. It works by analyzing the compression artifacts in a JPEG image to identify areas that may have been altered.

#### How ELA Detects Forgeries:

1. **Compression Patterns**:
   - Original images have consistent compression artifacts across the entire image.
   
2. **Recompression**:
   - The image is resaved at a known compression level to create an ELA map.

3. **Analyzing Discrepancies**:
   - The ELA map highlights differences in error levels. Areas with inconsistent compression (appearing brighter or with different colors) indicate potential tampering.

    """)
