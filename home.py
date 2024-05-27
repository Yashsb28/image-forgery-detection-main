import streamlit as st
from PIL import Image, ExifTags
from fpdf import FPDF
from io import BytesIO
import base64
import os
import imageio.v3 as iio
from prediction import predict_result, prepare_image
from ela import convert_to_ela_image
import random


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
    return href

def resize_by_ratio(image, new_width):
    width, height = image.size
    ratio = height / width
    new_height = int(ratio * new_width)
    return image.resize((new_width, new_height))

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

def generate_pdf(image, ela_img, metadata, predicted, confidence):

    pdf = FPDF()
    pdf.add_page()

    # Add original image
    pdf.set_font("Arial", size=12)

    pdf.cell(120, 10, txt="Uploaded Image", align="C")
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
    pdf.cell(200, 10, txt=f"Prediction: {predicted} with {confidence}% confidence", ln=True, align="C")

    # Save the PDF
    #pdf.output("forgery_detection_report.pdf")
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    #return "forgery_detection_report.pdf"
    return pdf_bytes

def show_home():
    # st.image("logo1.jpg", use_column_width=True)
    st.title("Welcome to AI-Forgery Guard")
    st.write("Detect image forgeries with high accuracy.")
    

    file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    
    if file:
        img = iio.imread(file)
        image = Image.fromarray(img)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Predict"):
            predicted, confidence = predict_result(image)
            st.write(f"Prediction: {predicted} with {confidence}% confidence")
            
            ela_img = convert_to_ela_image(image, quality=90)
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Uploaded Image", use_column_width=True)
            with col2:
                st.image(ela_img, caption="ELA Image", use_column_width=True)
            
            metadata = get_image_metadata(image)
            
            pdf_bytes = generate_pdf(image, ela_img, metadata, predicted, confidence)
            st.download_button(label="Download PDF", data=pdf_bytes, file_name="forgery_detection_report.pdf", mime="application/pdf")

    if st.button("Use Sample Image"):
        sample = random.choice(os.listdir('examples'))
        sample_path = os.path.join('examples', sample)
        img = iio.imread(sample_path)
        image = Image.fromarray(img)
        predicted, confidence = predict_result(image)
        st.write(f"Uploaded image: {predicted}")
        st.write(f"Prediction: {predicted} with {confidence}% confidence")
        
        ela_img = convert_to_ela_image(image, quality=90)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        with col2:
            st.image(ela_img, caption="ELA Image", use_column_width=True)
        
        metadata = get_image_metadata(image)
        
        pdf_bytes = generate_pdf(image, ela_img, metadata, predicted, confidence)
        st.download_button(label="Download PDF", data=pdf_bytes, file_name="forgery_detection_report.pdf", mime="application/pdf")

# Define the main function to run the app
def main():
    show_home()

# Run the app
if __name__ == "__main__":
    main()
