import cv2
import pytesseract
import numpy as np
from imutils.object_detection import non_max_suppression
from PIL import Image
import os

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image, boxes):
    # Convert the PIL Image to a numpy array
    image_np = np.array(image)

    # Extract text from each bounding box
    extracted_text = ''
    for box in boxes:
        (startX, startY, endX, endY) = box.astype("int")
        roi = image_np[startY:endY, startX:endX]
        text = pytesseract.image_to_string(roi)
        extracted_text += text.strip() + '\n'

    return extracted_text.strip()

def capture_from_webcam():
    # Check if the EAST model file exists
    model_file = "D:/project3/ai for project3/opencvproj 2/frozen_east_text_detection.pb"
    if not os.path.isfile(model_file):
        print("Error: The EAST model file '{}' is not found.".format(model_file))
        print("Please download the model file from the following link:")
        print("https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/download_models.py")
        print("and add it to the same directory as your Python script.")
        exit()

    # Load pre-trained EAST text detector
    net = cv2.dnn.readNet(model_file)

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

        # Resize frame to have a width of 320 pixels (required input size for EAST text detector)
        (H, W) = frame.shape[:2]
        (newW, newH) = (320, 320)
        rW = W / float(newW)
        rH = H / float(newH)
        resized_frame = cv2.resize(frame, (newW, newH))

        # Prepare input image for EAST text detector
        blob = cv2.dnn.blobFromImage(resized_frame, 1.0, (newW, newH),
                                      (123.68, 116.78, 103.94), swapRB=True, crop=False)

        # Forward pass through EAST text detector
        net.setInput(blob)
        (scores, geometry) = net.forward(["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"])

        # Post-process the results
        (boxes, scores) = non_max_suppression(geometry, scores)

        # Display the frame with text boxes
        for (startX, startY, endX, endY) in boxes:
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

        cv2.imshow('Webcam Preview', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam
    cap.release()

    # Convert the frame to a PIL Image
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Extract text from the image
    extracted_text = extract_text_from_image(pil_image, boxes)

    cv2.destroyAllWindows()

    return extracted_text
