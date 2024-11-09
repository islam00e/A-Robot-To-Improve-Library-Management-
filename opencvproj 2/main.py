

#from cgitb import reset
from pickle import DICT
from tkinter import Image
import cv2
from cv2 import adaptiveThreshold
import pytesseract
import numpy as np
import sqlite3
from pytesseract import Output
#import easyocr
image_number = 0
import os
import csv

conn = sqlite3.connect('library4444db.sqlite')

conn.execute('''CREATE TABLE IF NOT EXISTS COMPANY
         (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
         NAME   TEXT    NOT NULL
        );''')


img = cv2.imread("cup.png") #specify the image

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)
noiseless_image_bw = cv2.fastNlMeansDenoising(gray, None, 21, 0, 0 ) 
gray = cv2.GaussianBlur(gray, (11, 11), 0)
gary = cv2.Canny(gray, 30, 150, 3)

# Performing OTSU threshold
ret, thresh1 = cv2.threshold(noiseless_image_bw, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)

 
# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
 
# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                 cv2.CHAIN_APPROX_NONE)
 
# Creating a copy of image
im2 = img.copy()
 
# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()
text=""
# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
i=0
txt=[]
for cnt in contours:
    
    x, y, w, h = cv2.boundingRect(cnt)
     
    # Drawing a rectangle on copied image
    rect = cv2.rectangle(dilation, (x, y), (x + w, y +h), (60, 0, 0), 1)
    cv2.imwrite('/Users/admin/Desktop/opencvproj/image2.jpg',rect)
    # Cropping the text block for giving input to OCR
    cropped = thresh1[y:y+h, x:x+w]
    cv2.imwrite('/Users/admin/Desktop/opencvproj/image3.jpg',cropped)

#     # Open the file in append mode
#          file = open("recognized.txt", "a")

     
#     # Apply OCR on the cropped image
#          result=pytesseract.image_to_data(cropped, lang='eng', output_type=Output.BYTES)

#          text = pytesseract.image_to_data('image3.jpg',output_type=Output.STRING)
#          text1 = pytesseract.image_to_string(cropped,output_type=Output.DICT)
#     # print(text[0]['text'])
#     # Appending the text into file
#          txt.append( str(text1.get('text')))
   


    # cv2.waitKey(0)
    
    # Close the file
# file.close

# THIS BLOCK UNTIL THE LINE MAY WORK BETTER ON SOME TYPE OF PHOTOS

# EASYOCR Block
# reader=easyocr.Reader(["en"])
# txt=reader.readtext(cropped,output_format= Output.DICT)
# file = open("recognized.txt", "a")
# file.write(str(txt))
# for i in range (len(txt)):
#    file.write(str(txt[i]['text'])+"\n")
# c=0
# boxes=[]
# fullname=""
# books=[]
# for j in range(len(txt)):
#     if j < len(txt) :
#        if txt[j]!='' :
#          fullnume=txt[j]
#          if txt[j]['confident']>0.8:
#            books.append(fullnume)
#            boxes.append(txt[j]["boxes"][0][0])
# for n in range(len(boxes)):
#     if n<len(boxes)-1:
#         if boxes[n]-boxes[n+1]>5 or boxes[n]-boxes[n+1]<-5:
#             boxes.remove(boxes[n+1])
#             books.remove(books[n+1])
# for r in range(len(boxes)):
#     if r<len(boxes)-1:
#         if boxes[r]-boxes[r+1]<=1 and boxes[r]-boxes[r+1]>=-1:
#             books[r]['text']=books[r]['text']+" "+ books[r+1]['text']
#             boxes.remove(boxes[r+1])

#             books.remove(books[r+1])

###########################################################
cv2.imwrite('/Users/admin/Desktop/opencvproj/image55.jpg',gray)


img2 =[]
txt=[]
newbooks=[]
c=0
for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if h < 200:
           
            if w > 100:
                if w < 15000:
                    rect =cv2.rectangle(dilation, (x, y), (x + w, y + h), (36,255,12), 2)
                    #---format is height y to y +h and width x to x+w
                    roi = thresh1[y: y+h, x:x+w]
                    cv2.imwrite('ROI_{}.png'.format(image_number), roi)
                    cv2.imwrite('/Users/admin/Desktop/opencvproj/image55.jpg',thresh1)
                    
                    img2.append('ROI_{}.png'.format(image_number))
                    text= pytesseract.image_to_string(img2[image_number])
                    
                    file = open("recognized.txt", "w+")
                    file.write(str(text))
                    newbooks.append(text)
                    image_number += 1

for l in range(len(newbooks)):
    file.write(str(newbooks[l])+"\n")
    conn.execute("INSERT INTO COMPANY (NAME) \
      VALUES (?)",(str(newbooks[l]),))
cursor = conn.cursor()
cursor.execute("select ID,NAME from COMPANY")

with open("books_data.csv", "w") as csv_file:
     csv_writer = csv.writer(csv_file)
     csv_writer.writerow([i[0] for i in cursor.description])
      
     csv_writer.writerows(cursor)

dirpath = os.getcwd() + "/books_data2.csv"
