
import pytesseract
from PIL import Image

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the image file
image_path = r"D:\project3\ai qrcode\Screenshot (173).png"

# Open the image file
with Image.open(image_path) as img:
    # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(img)
    
    # Print the extracted text
    print(extracted_text)
