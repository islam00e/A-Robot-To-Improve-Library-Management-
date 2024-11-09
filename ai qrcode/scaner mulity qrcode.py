import cv2
from pyzbar.pyzbar import decode

def extract_qrcodes(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use OpenCV to detect QR codes in the image
    qr_codes = decode(gray_image)
    
    # Extract and decode the data from QR codes
    extracted_data = []
    for qr_code in qr_codes:
        qr_data = qr_code.data.decode("utf-8")
        extracted_data.append(qr_data)
    
    return extracted_data

def main():
    # Input image containing QR codes
    image_path = r"D:\project3\ai for project3\opencvproj 2\New folder\opencvproj 2\2.jpg"
    
    # Extract QR codes and their data
    extracted_data = extract_qrcodes(image_path)
    
    # Print the extracted data
    for i, data in enumerate(extracted_data):
        print(f"QR Code {i+1} data: {data}")

if __name__ == "__main__":
    main()
