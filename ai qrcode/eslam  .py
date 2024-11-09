import cv2
from pyzbar.pyzbar import decode
import sqlite3

def create_table(conn):
    # Create a new table with the desired schema
    conn.execute('''CREATE TABLE IF NOT EXISTS BOOKS
                     (BOOK_NAME TEXT NOT NULL);''')

def extract_qrcodes_from_camera():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    
    print("Press 'q' to capture the QR code and exit.")
    
    extracted_data = []
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        
        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect QR codes in the frame
        qr_codes = decode(gray_frame)
        
        # Extract and decode the data from QR codes
        for qr_code in qr_codes:
            qr_data = qr_code.data.decode("utf-8")
            extracted_data.append((qr_data,))  # Add book name to the list
        
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()
    
    return extracted_data

def insert_books(conn, extracted_data):
    # Insert extracted book names into the table
    conn.executemany("INSERT INTO BOOKS (BOOK_NAME) VALUES (?)", extracted_data)

def main():
    # Connect to SQLite database
    conn = sqlite3.connect('librarynewdb.sqlite')
    
    # Create the table if it doesn't exist
    create_table(conn)
    
    # Extract QR codes and their data from the camera
    extracted_data = extract_qrcodes_from_camera()
    
    # Insert extracted book names into the table
    insert_books(conn, extracted_data)
    
    # Commit changes to the database
    conn.commit()

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
