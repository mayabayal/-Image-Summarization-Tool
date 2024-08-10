from fastapi import FastAPI, File, UploadFile, HTTPException
import pytesseract
from PIL import Image
import torch
from torchvision import transforms
from transformers import pipeline
import os

app = FastAPI()

# Specify the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Update if needed

# Initialize the summarization pipeline using a pre-trained transformer model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def preprocess_image_for_ocr(image_path):
    """Apply image preprocessing to enhance OCR accuracy."""
    img = Image.open(image_path)
    img = img.convert('L')  # Convert to grayscale
    img = img.point(lambda x: 0 if x < 140 else 255)  # Binarize image for clarity
    return img

def extract_text_from_image(image_path):
    """Extract text from an image using Tesseract OCR with custom configurations."""
    img = preprocess_image_for_ocr(image_path)
    custom_config = r'--oem 3 --psm 6'  # Using OCR Engine Mode 3 (both LSTM and legacy) and PSM 6
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

def summarize_text(text):
    """Generate a summary of the extracted text."""
    try:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize/")
async def summarize_image(file: UploadFile = File(...)):
    """API endpoint to receive image files and return a text summary."""
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        # Extract text from the image
        extracted_text = extract_text_from_image(file_path)
        
        # Summarize the extracted text
        summary = summarize_text(extracted_text)
        
        # Return the summary as a JSON response
        return {"summary": summary}
    
    finally:
        # Clean up the temporary file
        os.remove(file_path)

# To run the FastAPI app, use the following command:
# uvicorn image_summarizer:app --reload
