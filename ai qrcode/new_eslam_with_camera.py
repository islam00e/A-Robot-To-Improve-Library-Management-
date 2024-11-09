import cv2
from pyzbar.pyzbar import decode
import sqlite3

def create_table(conn):
    # Create a new table with the desired schema
    conn.execute('''CREATE TABLE IF NOT EXISTS BOOKS
                     (BOOK_NAME TEXT NOT NULL);''')

def extract_qrcodes(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use OpenCV to detect QR codes in the image
    qr_codes = decode(gray_image)
    
    # Extract and decode the data from QR codes
    extracted_data = []
    for qr_code in qr_codes:
        qr_data = qr_code.data.decode("utf-8")
        extracted_data.append((qr_data,))  # Add book name to the list
    
    return extracted_data

def insert_books(conn, extracted_data):
    # Insert extracted book names into the table
    conn.executemany("INSERT INTO BOOKS (BOOK_NAME) VALUES (?)", extracted_data)

def main():
    # Connect to SQLite database
    conn = sqlite3.connect('librarynewdb.sqlite')
    
    # Create the table if it doesn't exist
    create_table(conn)
    
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 represents the default camera
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return
    
    # Capture a photo from the camera
    ret, frame = cap.read()
    
    # Release the camera
    cap.release()
    
    # Check if the photo was captured successfully
    if not ret:
        print("Error: Unable to capture photo.")
        return
    
    # Extract QR codes and their data from the captured photo
    extracted_data = extract_qrcodes(frame)
    
    # Insert extracted book names into the table
    insert_books(conn, extracted_data)
    
    # Commit changes to the database
    conn.commit()

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
