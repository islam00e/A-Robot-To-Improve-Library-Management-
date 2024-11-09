import cv2
import pytesseract
import numpy as np
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('librarydb.db')

# Create COMPANY table if not exists
conn.execute('''CREATE TABLE IF NOT EXISTS COMPANY
         (ID INT PRIMARY KEY NOT NULL,
         NAME TEXT NOT NULL,
         x REAL DEFAULT 0,
         y REAL DEFAULT 0,
         bookNumber REAL DEFAULT 0);''')

# Read the image
img_path = "d:/project3/ai for project3/opencvproj/image2.jpg"
img = cv2.imread(img_path)

# Check if image was successfully loaded
if img is None:
    print(f"Error: Unable to read the image '{img_path}'")
    exit(1)

# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply denoising
noiseless_image_bw = cv2.fastNlMeansDenoising(gray, None, 21, 7, 30)

# Apply adaptive thresholding
adaptive_threshold = cv2.adaptiveThreshold(noiseless_image_bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)

# Perform OCR
pytesseract.pytesseract.tesseract_cmd = "path_to_your_tesseract_executable"
text = pytesseract.image_to_string(adaptive_threshold, config="--psm 3")
lines = text.split("\n")

# Insert extracted text into database
conn.execute("INSERT INTO COMPANY (ID, NAME, x, y, bookNumber) VALUES (1, ?, 0, 0, 1)", (lines[0],))
conn.commit()

# Retrieve data from COMPANY table and print
cursor = conn.execute("SELECT id, name, x, y, bookNumber FROM COMPANY")
for row in cursor:
    print("ID =", row[0])
    print("NAME =", row[1])
    print("x =", row[2])
    print("y =", row[3])
    print("bookNumber =", row[4])

# Close database connection
conn.close()
