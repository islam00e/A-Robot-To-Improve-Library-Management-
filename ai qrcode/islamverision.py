import cv2
from pyzbar.pyzbar import decode
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('library4444db.sqlite')

def create_books_table():
    conn.execute('''CREATE TABLE IF NOT EXISTS BOOKS
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             BOOK_NAME TEXT NOT NULL,
             WRITER_NAME TEXT NOT NULL);''')

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
        extracted_data.append(qr_data.split('\n'))  # Assuming the QR code data contains book name and writer name separated by newline
    
    return extracted_data

def main():
    # Input image containing QR codes
    image_path = r"D:\project3\ai for project3\opencvproj 2\New folder\opencvproj 2\2.jpg"
    
    # Create the BOOKS table if it doesn't exist
    create_books_table()
    
    # Extract QR codes and their data
    extracted_data = extract_qrcodes(image_path)
    
    # Print the extracted data
    for i, data in enumerate(extracted_data):
        if len(data) >= 2:
            book_name = data[0]
            writer_name = data[1]
            print(f"Extracted Data: {data}")
            print(f"Book Name: {book_name}, Writer Name: {writer_name}")
            
            # Insert extracted book and writer names into the database
            conn.execute("INSERT INTO BOOKS (BOOK_NAME, WRITER_NAME) VALUES (?, ?)", (book_name, writer_name))
    
    # Commit changes to the database
    conn.commit()

if __name__ == "__main__":
    main()
import cv2
from pyzbar.pyzbar import decode
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('library4444db.sqlite')
conn.execute('''CREATE TABLE IF NOT EXISTS QR_CODES
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         DATA TEXT NOT NULL);''')

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
        
        # Insert extracted QR code data into the database
        conn.execute("INSERT INTO QR_CODES (DATA) VALUES (?)", (data,))
    
    # Commit changes to the database
    conn.commit()

if __name__ == "__main__":
    main()

# Close the database connection
conn.close()

# Close the database connection
conn.close()
