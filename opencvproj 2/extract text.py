import cv2
import pytesseract
import numpy as np

# Set path to Tesseract OCR executable (update if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_photo(image_path):
    """Extracts text from an image with improved accuracy.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: The extracted text from the image.
    """

    try:
        # Read image in grayscale for faster processing
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print("Error: Unable to read the image file.")
            return

        # Enhance contrast using CLAHE for better text segmentation
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img_enhanced = clahe.apply(img)

        # Apply bilateral filtering to reduce noise while preserving edges
        img_bilateral = cv2.bilateralFiltering(img_enhanced, 9, 75, 75)

        # Apply Gaussian blur to reduce noise
        blur = cv2.GaussianBlur(img_bilateral, (5, 5), 0)

        # ... rest of the code remains the same ...

    except Exception as e:
        print(f"Error occurred during text extraction: {e}")
        return ""

# Example usage
image_path = r"D:\project3\ai for project3\opencvproj 2\pexels-fotios-photos-1485548.jpg"  # Replace with your image path
extracted_text = extract_text_from_photo(image_path)

if extracted_text:
    print("Extracted text:")
    print(extracted_text)
else:
    print("No text found in the image.")
