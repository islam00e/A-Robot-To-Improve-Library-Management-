from PIL import Image
from pytesseract import image_to_string
import cv2
image=Image.open('SAMPLE3.jpg') #specify the image name
text=image_to_string(image,lang='eng')
print(text)
file=open('output.txt','w')
text=repr(text)
file.write(text)
file.close
