import cv2
import pytesseract
import numpy as np
import sqlite3
import os
import csv

# Set path to Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path according to your Tesseract installation

# Connect to SQLite database
conn = sqlite3.connect('library4444db.sqlite')

# Create BOOKS table if not exists
conn.execute('''CREATE TABLE IF NOT EXISTS BOOKS
         (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
         NAME   TEXT    NOT NULL
        );''')

# Read image
img = cv2.imread(r"D:\project3\ai for project3\opencvproj 2\cup.png")  # Escaped backslashes

# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Further noise reduction using morphological operations
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

# Find contours
contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize variables
newbooks = []

# Loop through contours
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if h > 50 and w > 50:  # Filter out small contours
        # Extract ROI
        roi = gray[y:y+h, x:x+w]
        # Resize ROI for better OCR performance
        roi_resized = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(roi_resized)
        newbooks.append(text.strip())  # Remove leading/trailing whitespace

# Write book names to recognized.txt
with open("recognized.txt", "w") as text_file:
    for book_name in newbooks:
        text_file.write(book_name + "\n")

# Insert data into SQLite database - using parameterized query
for book in newbooks:
    conn.execute("INSERT INTO BOOKS (NAME) VALUES (?)", (book,))

# Commit changes
conn.commit()

# Write data to CSV - fetching data from cursor
cursor = conn.cursor()
cursor.execute("SELECT ID, NAME FROM BOOKS")
data = cursor.fetchall()
with open("books_data.csv", "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(data)

# Close connection
conn.close()
