from easyocr import Reader
import argparse
import cv2

reader = Reader(['en']) # this needs to run only once to load the model into memory

result = reader.readtext('books3.png')
print(result)
