import cv2
import numpy as np

def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    return blurred

def detect_vertical_lines(image):
    # Apply Canny edge detection
    edges = cv2.Canny(image, 100, 150, apertureSize=3)  # Adjust threshold values
    
    # Detect lines using Hough transform
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=100, maxLineGap=10)  # Adjust threshold and parameters
    
    return lines

def segment_books(image, lines):
    # Draw detected lines on the original image for visualization
    image_with_lines = image.copy()
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image_with_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Segment the image into boxes based on vertical lines
    boxes = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Segment the box using original coordinates
            box = image[:, x1:x2]  # Using full height of the image
            boxes.append(box)
    
    return image_with_lines, boxes

# Load the image
image_path = r"D:\project3\ai for project3\opencvproj 2\WhatsApp Image 2024-04-20 at 22.14.03_cc765041.jpg"
image = cv2.imread(image_path)

# Preprocess the image
preprocessed_image = preprocess_image(image)

# Detect vertical lines
lines = detect_vertical_lines(preprocessed_image)

# Segment the books based on vertical lines
image_with_lines, boxes = segment_books(image, lines)

# Visualize the result
cv2.imshow('Detected Vertical Lines', image_with_lines)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save segmented book images
for i, box in enumerate(boxes):
    cv2.imwrite(f"book_segment_{i}.jpg", box)
