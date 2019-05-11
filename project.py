import zipfile
import PIL
from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
search_name=input("Search name: ")


with zipfile.ZipFile("readonly/images.zip","r") as f:

    for name in f.namelist():
        cv_images=[]
        im=Image.open(f.extract(name))
        text=pytesseract.image_to_string(im)
        if (search_name in text):

            img2 = cv.imread(name)
            gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.36,6)

            if (len(faces)==0):
                print("Result found in file {}".format(name))
                print("But there were not faces in that file!")
            else:
                for x,y,w,h in faces:
                    cv_images.append(im.crop((x,y,x+w,y+h)))

                cv_images[0]=cv_images[0].resize((190,190))
                n=len(cv_images)//5+1
                contact_sheet=PIL.Image.new(cv_images[0].mode, (190*5,190*n))

                x,y=0,0

                for img in cv_images[0:]:
                    contact_sheet.paste(img.resize((190,190)), (x, y) )
                    if x+190 == contact_sheet.width:
                        x=0
                        y=y+190
                    else:
                        x=x+190

                contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
                print("Result found in file {}".format(name))
                display(contact_sheet)
