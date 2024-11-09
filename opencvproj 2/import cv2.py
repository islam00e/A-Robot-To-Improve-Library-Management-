import cv2
import pytesseract
import numpy as np

# Set path to Tesseract OCR executable (update if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_photo(image_path):
    """Extracts text from an image with improved accuracy, attempting various strategies.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: The extracted text from the image, or an empty string if no text is found.
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

        # Strategy 1: Apply sharpening to enhance text edges
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        img_sharpened = cv2.filter2D(img_enhanced, -1, kernel)

        # Strategy 2: Try different adaptive thresholding parameters
        thresh1 = cv2.adaptiveThreshold(img_sharpened, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)
        thresh2 = cv2.adaptiveThreshold(img_enhanced, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY_INV, 15, 2)

        # Strategy 3: Explore combining both thresholded images (optional)
        combined_thresh = cv2.bitwise_or(thresh1, thresh2)  # Experiment with OR/AND operations

        # Morphological operations for noise reduction (fine-tune based on image type)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(combined_thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Find contours and filter based on aspect ratio and minimum area for text regions
        contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            if 0.2 < aspect_ratio < 1.5 and h > 20 and w > 50:  # Adjust thresholds as needed
                text_regions.append((x, y, w, h))

        # Extract text from each identified text region using Tesseract
        all_text = ""
        for x, y, w, h in text_regions:
            roi = img_enhanced[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            text = pytesseract.image_to_string(roi_resized, config='--psm 6')  # Single block mode
            all_text += text.strip() + "\n"  # Combine text with newlines

        # Return extracted text, or an empty string if none found
        return all_text.strip() if all_text else ""

    except Exception as e:
        print(f"Error occurred during text extraction: {e}")
        return ""

# Example usage
image_path = r"D:\project3\ai for project3\opencvproj 2\pexels-fotios-photos-1485548.jpg"  # Replace with your image path
extracted_text = extract_text_from_photo(image_path)

if extracted_text:
    print("Extracted text:")
    print
