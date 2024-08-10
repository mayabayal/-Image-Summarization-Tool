
# Image Summarization Tool

## Overview
The Image Summarization Tool is designed to extract text from images using Optical Character Recognition (OCR) and then summarize the text using Natural Language Processing (NLP). This project utilizes Tesseract OCR for text extraction and the BART model for generating summaries. The application provides two interfaces: a FastAPI backend for API interactions and a Streamlit frontend for a user-friendly graphical interface.

## Installation

### Prerequisites
- Python 3.8+
- Tesseract OCR

### Setup
Clone the repository:
```bash
git clone https://github.com/mayabayal/-Image-Summarization-Tool.git
cd -Image-Summarization-Tool
```

Install the required Python libraries:
```bash
pip install -r requirements.txt
```

Ensure Tesseract OCR is installed and configured:
- For Windows, Mac, and Linux: Follow the instructions at https://github.com/tesseract-ocr/tesseract

### Running the Application

#### FastAPI Backend
Start the FastAPI server:
```bash
uvicorn app:app --reload
```
This command will host the API on `http://127.0.0.1:8000`.

#### Using `curl` to Interact with the API
To send an image to the FastAPI server and get a text summary, use the following `curl` command:
```bash
curl -X POST -F "file=@path_to_your_image.jpg" http://127.0.0.1:8000/summarize/
```
Replace `path_to_your_image.jpg` with the path to your image file.

#### Streamlit Frontend
To run the Streamlit interface:
```bash
streamlit run streamlit_app.py
```
This command will start the Streamlit server and open the application in your web browser.

## Usage

### FastAPI
Navigate to `http://127.0.0.1:8000/docs` to see the Swagger UI where you can test the API directly from your browser.

### Streamlit
Access the Streamlit application in your browser to upload images and view both the extracted text and its summary in real-time.

## Future Enhancements
- Improve OCR accuracy with advanced image processing techniques.
- Enhance the summarization model to handle complex texts better.
- Implement functionality for batch image processing.
- Add support for multiple languages.
