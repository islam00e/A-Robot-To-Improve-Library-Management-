import cv2
import pytesseract
import numpy as np
import sqlite3
import os
import csv

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to create SQLite database and table
def create_database():
    conn = sqlite3.connect('library4444db.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS COMPANY
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 NAME TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to perform image processing tasks
def process_image():
    image = cv2.imread=r"D:\project3\ai for project3\opencvproj 2\SAMPLE3.jpg"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    blurred = cv2.GaussianBlur(denoised, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 150)
    _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# Function to find contours and extract text
def extract_text(thresh):
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    recognized_text = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = thresh[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, lang='eng')
        recognized_text.append(text.strip())
    return recognized_text

# Function to insert text into SQLite database
def insert_into_database(text_list):
    conn = sqlite3.connect('library4444db.db')
    c = conn.cursor()
    for text in text_list:
        c.execute("INSERT INTO COMPANY (NAME) VALUES (?)", (text,))
    conn.commit()
    conn.close()

# Function to export data from SQLite database to CSV
def export_to_csv():
    conn = sqlite3.connect('library4444db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM COMPANY")
    rows = c.fetchall()
    with open('books_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ID', 'NAME'])
        csvwriter.writerows(rows)
    conn.close()

# Main function
def main():
    create_database()
    processed_image = process_image()
    text_list = extract_text(processed_image)
    insert_into_database(text_list)
    export_to_csv()

if __name__ == "__main__":
    main()
