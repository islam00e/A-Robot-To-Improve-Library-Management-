import pytesseract
from PIL import Image
import re

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Use Tesseract to get bounding boxes and text
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        # Extract text and concatenate it
        extracted_text = ''
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            if text:
                left, top, width, height = int(data['left'][i]), int(data['top'][i]), int(data['width'][i]), int(data['height'][i])
                extracted_text += ' ' + text
        # Remove extra spaces and return the extracted text
        return re.sub(' +', ' ', extracted_text.strip())

# Example usage:
image_path = r"D:\project3\ai for project3\opencvproj 2\text.png"
extracted_text = extract_text_from_image(image_path)
print(extracted_text)
