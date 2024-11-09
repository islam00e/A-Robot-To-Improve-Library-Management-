import pytesseract
from PIL import Image

# Define the path to Tesseract executable (replace with your actual path)
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set the Tesseract path using pytesseract.pytesseract.tesseract_cmd
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Define the path to your image
image_path = r"D:\project3\ai for project3\opencvproj 2\text.png"

# Load the image
img = Image.open(image_path)

# Convert the image to grayscale (improves OCR accuracy)
gray = img.convert('L')

# Perform OCR using pytesseract
text = pytesseract.image_to_string(gray)

# Print the extracted text
print(text)
