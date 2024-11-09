import cv2
import pytesseract
import re
import numpy as np
from PIL import Image

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image):
    # Convert the PIL Image to a numpy array
    image_np = np.array(image)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get a binary image
    _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Invert the binary image
    inverted_image = cv2.bitwise_not(thresh_image)

    # Use Tesseract to extract text
    extracted_text = pytesseract.image_to_string(inverted_image)

    return extracted_text.strip()

# Capture image from webcam with live preview and text contours
def capture_from_webcam(num_attempts=5):
    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Couldn't open webcam")
        return None

    # Show live preview window
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't capture frame")
            break

        # Display the frame
        cv2.imshow('Webcam Preview', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam
    cap.release()

    # Convert the frame to a PIL Image
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Extract text from the image
    extracted_text = extract_text_from_image(pil_image)

    cv2.destroyAllWindows()

    return extracted_text

# Example usage:
extracted_text = capture_from_webcam()
print("Extracted Text:", extracted_text)
