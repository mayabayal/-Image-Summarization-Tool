import streamlit as st
from PIL import Image
import pytesseract
from transformers import pipeline
import os

# Specify the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def preprocess_image_for_ocr(image):
    """Convert image to a format suitable for OCR."""
    image = image.convert('L')  # Convert to grayscale
    image = image.point(lambda x: 0 if x < 140 else 255)  # Binarize image for clarity
    return image

def extract_text_from_image(image):
    """Use Tesseract to extract text from an image."""
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

def summarize_text(text):
    """Use a pretrained model to summarize text."""
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    return summary

# Streamlit interface
st.title('Image Summarization Tool')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    st.write("Processing...")

    # Process the image
    try:
        preprocessed_image = preprocess_image_for_ocr(image)
        extracted_text = extract_text_from_image(preprocessed_image)
        if extracted_text:
            st.write("Extracted Text:", extracted_text)
            summary = summarize_text(extracted_text)
            st.write("Summary:", summary)
        else:
            st.write("No text could be extracted from the image.")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

# To run this Streamlit app, save the script and use:
# streamlit run streamlit_app.py
