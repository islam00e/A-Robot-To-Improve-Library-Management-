import cv2
import numpy as np
import pytesseract

# Set the path to Tesseract executable (change this to your installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load pre-trained object detection model
net = cv2.dnn.readNet("frozen_inference_graph.pb", "ssd_mobilenet_v3_large_coco.pbtxt")

# Function to capture image from camera
def capture_image():
    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Capture frame
    ret, frame = cap.read()

    # Release camera
    cap.release()

    return frame

# Function to extract text from book region
def extract_text_from_book(image, bbox):
    # Extract region of interest (ROI) containing the book
    x, y, w, h = bbox
    book_roi = image[y:y+h, x:x+w]

    # Convert ROI to grayscale
    gray_roi = cv2.cvtColor(book_roi, cv2.COLOR_BGR2GRAY)

    # Use Tesseract to extract text from the book ROI
    text = pytesseract.image_to_string(gray_roi, lang='eng')

    return text

# Main function
def main():
    # Capture image
    print("Capturing image...")
    image = capture_image()

    # Get image dimensions
    height, width = image.shape[:2]

    # Prepare input image for object detection
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # Pass the input image through the network to perform object detection
    net.setInput(blob)
    detections = net.forward()

    # Loop over the detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections and only consider "book" class
        if confidence > 0.5 and int(detections[0, 0, i, 1]) == 84:  # 84 corresponds to the "book" class label
            # Extract bounding box coordinates
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (x, y, w, h) = box.astype("int")

            # Extract text from the book region
            book_text = extract_text_from_book(image, (x, y, w, h))

            # Print the extracted text
            print("Extracted Text from Book:")
            print(book_text)

            # Draw bounding box around the book
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)

    # Display the image
    cv2.imshow("Image with Detected Book", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
