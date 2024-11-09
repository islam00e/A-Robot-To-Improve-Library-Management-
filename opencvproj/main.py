import string
import cv2
import pytesseract
import numpy as np
import sqlite3
conn = sqlite3.connect('librarydb.sql')

conn.execute('''CREATE TABLE IF NOT EXISTS COMPANY
         (ID INT PRIMARY KEY   NOT NULL,
         NAME   TEXT    NOT NULL,
         x         REAL ALLOW NULL,
         y         REAL ALLOW NULL,
         bookNumber  REAL ALLOW NULL);''')
img = cv2.imread("D:\project3\ai for project3\opencvproj\image2.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


dilated_img = cv2.dilate(gray, np.ones((7, 7), np.uint8))
gray = cv2.resize(gray, None, fx=0.23, fy=0.5)

gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)

noiseless_image_bw = cv2.fastNlMeansDenoising(gray, None, 21, 7, 30) 

adaptive_threshold = cv2.adaptiveThreshold(noiseless_image_bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)

# contours, hierarchy = cv2.findContours(dilated_img, cv2.RETR_EXTERNAL,
#  												cv2.CHAIN_APPROX_NONE)

im2 = img.copy()
cv2.imwrite("D:\project3\ai for project3\opencvproj\image2.jpg",adaptive_threshold)
file = open("recognized.txt", "w+")
file.write("")
file.close()

pytesseract.pytesseract.tesseract_cmd="/usr/local/Cellar/tesseract/5.2.0/bin/tesseract"
# for cnt in contours:
    # x, y, w, h = cv2.boundingRect(cnt)
     
    # # Drawing a rectangle on copied image
    # rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
     
    # # Cropping the text block for giving input to OCR
    # cropped = noiseless_image_bw[y:y + h, x:x + w]

    # Open the file in append mode
    # 
file = open("recognized.txt", "a")
     
text = pytesseract.image_to_string(adaptive_threshold,config="--psm 3")
    # Appending the text into file
ch=text.split("\n")

file.write(ch[0])
file.write("\n")
     
    # Close the file
file.close
conn.execute("INSERT INTO COMPANY (ID,NAME,x,y,bookNumber) \
      VALUES (1,?, 0, 0, 1 )",(ch[0],));

cursor=conn.execute("select ID,NAME from company")
cursor = conn.execute("SELECT id, name, x, y,bookNumber from COMPANY")
for row in cursor:
   print ("ID = ", row[0])
   print ("NAME = ", row[1])
   print ("x = ", row[2])
   print ("y = ", row[3])
   print ("bookNumber = ", row[4] )
   
conn.close()


# cv2.imwrite('/Users/admin/Desktop/opencvproj/cropped.jpg',cropped)
