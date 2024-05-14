'''import streamlit as st
from prediction import predict_result
import imageio.v3 as iio
from PIL import Image
import random
import os


st.title("Image Forgery Detection")

file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if file is None:
    if st.button("Use Sample Image"):
        sample = random.choice(os.listdir('examples'))
        sample_file = open(f"examples/{sample}", "rb")
        img = iio.imread(sample_file)
        image = Image.fromarray(img)
        original = "Authentic" if sample.startswith("A") else "Forged"
        st.write(f"Original: {original}") 
        predicted, confidence = predict_result(image) 
        st.write(f"Predicted: {predicted} with {confidence}% confidence")
        st.image(f"examples/{sample}", use_column_width=True)

else:
    img = iio.imread(file)
    image = Image.fromarray(img)

    if st.button("Predict"):

        predicted, confidence = predict_result(image) 
        st.write(f"Predicted: {predicted} with confidence {confidence}")
        st.image(image, use_column_width=True) '''

import streamlit as st
from fpdf import FPDF
from PIL import Image, ExifTags
from prediction import predict_result, prepare_image
from ela import convert_to_ela_image
from io import BytesIO
import imageio.v3 as iio
import random

import base64
import os

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
    return href

def resize_by_ratio(image, new_width):
    width, height = image.size
    ratio = height/width
    new_height = int(ratio * new_width)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def get_image_metadata(image):
    metadata = {}
    try:
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                metadata[tag_name] = value
    except AttributeError:
        pass
    return metadata

def exif_tag_to_str(tag):
    exif_tags = {
        271: 'ImageDescription',
        272: 'Make',
        274: 'Orientation',
        305: 'Software',
        306: 'DateTime',
        315: 'Artist',
        531: 'YCbCrPositioning',
        529: 'YCbCrSubSampling',
        33432: 'DateTimeOriginal',
        36867: 'DateTimeDigitized',
        42033: 'LensMake',
        42034: 'LensModel',
        42035: 'LensSerialNumber',
        37386: 'FocalLength',
        41495: 'LensSpecification',
        37378: 'ApertureValue',
        37379: 'ShutterSpeedValue',
        37380: 'BrightnessValue',
        37381: 'ExposureCompensation',
        37383: 'MeteringMode',
        37384: 'LightSource',
        37385: 'Flash',
        41986: 'ExposureMode',
        41987: 'WhiteBalance',
        41990: 'SceneCaptureType',
        41991: 'GainControl',
        41992: 'Contrast',
        41993: 'Saturation',
        41994: 'Sharpness',
        41995: 'DeviceSettingDescription',
        41996: 'SubjectDistanceRange',
        37521: 'ComponentsConfiguration',
        40960: 'FlashPixVersion',
        40961: 'ColorSpace',
        40962: 'ExifImageWidth',
        40963: 'ExifImageHeight',
        33434: 'ExposureTime',
        33437: 'FNumber',
        34850: 'ExposureProgram',
        34855: 'ISO',
        34856: 'ExifVersion',
        36864: 'ExifVersion',
        36868: 'ExifVersion',
        37377: 'ShutterSpeed',
        37382: 'Aperture',
        41985: 'CustomRendered',
        41988: 'DigitalZoomRatio',
        41989: 'FocalLengthIn35mmFilm',
        41994: 'SceneCaptureType',
        41995: 'GainControl',
        41996: 'Contrast',
        41997: 'Saturation',
        41998: 'Sharpness',
        42016: 'ImageUniqueID'
    }
    return exif_tags.get(tag, str(tag))

def display_metadata(metadata):
    st.subheader("Image Metadata")
    for key, value in metadata.items():
        st.write(f"**{key}:** {value}")

# Function to generate PDF
def generate_pdf(image,ela_img, confidence):
    '''pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add ELA image to the PDF
    ela_img_path = "ela_image.jpg"
    ela_img.save(ela_img_path)
    pdf.cell(200, 10, txt="ELA Image", ln=True, align="C")
    pdf.image(ela_img_path, x=10, y=20, w=180)
    
    # Add confidence score to the PDF
    pdf.cell(200, 10, txt=f"Confidence Score: {confidence}", ln=True, align="C")

    # Save the PDF
    pdf.output("forgery_detection_report.pdf")'''
    pdf = FPDF()
    pdf.add_page()

    # Add original image
    pdf.set_font("Arial", size=12)

    pdf.cell(120, 10, txt="Original Image", align="C")
    pdf.cell(40, 10, txt="ELA Image", align="C")
    original_img_resized = resize_by_ratio(image,200) # Resize the image
    original_img_resized_path = "original_img_resized.jpg"
    original_img_resized.save(original_img_resized_path)
    pdf.image(original_img_resized_path, x=40, y=20)

    # Add ELA image
    
    ela_img_resized = resize_by_ratio(ela_img,200)  # Resize the image
    ela_img_resized_path = "ela_img_resized.jpg"
    ela_img_resized.save(ela_img_resized_path)
    pdf.image(ela_img_resized_path, x=120, y=20)
    pdf.ln(160)

    # Add metadata details
    pdf.cell(200, 10, txt="Metadata", ln=True, align="C")
    for key, value in metadata.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align="C")

    # Add confidence score
    pdf.cell(200, 10, txt=f"Predicted: {predicted} with {confidence}% confidence", ln=True, align="C")

    # Save the PDF
    #pdf.output("forgery_detection_report.pdf")
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    #return "forgery_detection_report.pdf"
    return pdf_bytes

st.title("Image Forgery Detection")

file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if file is None:
    if st.button("Use Sample Image"):
        # Your existing code to load sample image and predict result
        sample = random.choice(os.listdir('examples'))
        sample_file = open(f"examples/{sample}", "rb")
        img = iio.imread(sample_file)
        image = Image.fromarray(img)
        original = "Authentic" if sample.startswith("A") else "Forged"
        st.write(f"Original: {original}") 
        predicted, confidence = predict_result(image) 
        st.write(f"Predicted: {predicted} with {confidence}% confidence")
        st.image(f"examples/{sample}", use_column_width=True)

        # Extract metadata
        metadata = get_image_metadata(image)
        #display_metadata(metadata)
        
        # Generate PDF
        ela_img = convert_to_ela_image(image, quality=90)
        #pdf_file = generate_pdf(image, ela_img, confidence)
        pdf_bytes = generate_pdf(image, ela_img, confidence)

        # Add download button
        st.download_button(label="Download PDF", data=pdf_bytes, file_name="forgery_detection_report.pdf", mime="application/pdf")

else:
    # Your existing code to read uploaded image and predict result
    img = iio.imread(file)
    image = Image.fromarray(img)

    if st.button("Predict"):
        predicted, confidence = predict_result(image) 
        st.write(f"Predicted: {predicted} with confidence {confidence}")
        st.image(image, use_column_width=True)

        # Extract metadata
        metadata = get_image_metadata(image)
        display_metadata(metadata)
        
        # Generate PDF
        ela_img = convert_to_ela_image(image, quality=90)
        #pdf_file = generate_pdf(image, ela_img, confidence)
        pdf_bytes = generate_pdf(image, ela_img, confidence)

        # Add download button
        #st.markdown(get_binary_file_downloader_html(pdf_file, 'Download PDF'), unsafe_allow_html=True)
        st.download_button(label="Download PDF", data=pdf_bytes, file_name="forgery_detection_report.pdf", mime="application/pdf")




