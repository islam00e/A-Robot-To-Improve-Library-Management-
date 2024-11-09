import cv2
import numpy as np

def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    return blurred

def detect_dark_vertical_lines(image):
    # Apply thresholding to isolate dark areas
    _, thresholded = cv2.threshold(image, 0, 50, cv2.THRESH_BINARY_INV)
    
    # Apply morphological operations to enhance the lines
    kernel = np.ones((3, 3), np.uint8)
    closed = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)
    
    # Detect contours of dark areas
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours to get vertical lines
    vertical_lines = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        if aspect_ratio < 0.2 and cv2.contourArea(contour) > 100:  # Adjust threshold parameters as needed
            vertical_lines.append(contour)
    
    return vertical_lines

def draw_lines(image, lines):
    # Draw detected lines on the original image
    image_with_lines = image.copy()
    cv2.drawContours(image_with_lines, lines, -1, (0, 255, 0), 2)
    
    return image_with_lines

# Load the image
image_path = r"D:\project3\ai for project3\opencvproj 2\pexels-photo-8123067.jpeg"
image = cv2.imread(image_path)

# Preprocess the image
preprocessed_image = preprocess_image(image)

# Detect dark vertical lines
dark_vertical_lines = detect_dark_vertical_lines(preprocessed_image)

# Draw the detected lines on the original image
image_with_lines = draw_lines(image, dark_vertical_lines)

# Visualize the result
cv2.imshow('Detected Dark Vertical Lines', image_with_lines)
cv2.waitKey(0)
cv2.destroyAllWindows()
