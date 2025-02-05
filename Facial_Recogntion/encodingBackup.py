## 
# Filename: encodingBackup.py
# Version: V25.0
# Author: Richard McFadden
# Project name: A-Recognition (Advance)
# Organization: Singularity
# Funtional description: Provides ability to add add people to database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np
import face_recognition
import cv2
import sys
import os
# Fetch the service account key JSON file contents
#path = os.path.dirname(os.path.realpath(__file__))
cred = credentials.Certificate('./Facial_Recogntion/credentials.json')
firebase_admin.initialize_app(cred)

#Create the DB object
db = firestore.client()

#GET the collection Users for Facial Recognition
users_ref = db.collection(u'users')

#docs now contain the data in Users
docs = users_ref.stream()

##
#Function that stores encodings of given images in DB
#
#@param images: Images to be encoded
#@param name: The names of the corresponding images
#@param surname: The surnames of the corresonding images
#@param title: The titles of the corresponding images
#@param email: The emails of the corresponding images
#@return: Return status of function
imageFileName = sys.argv[1]
name = sys.argv[2]
surname = sys.argv[3]
title = sys.argv[4]
email = sys.argv[5]

encoding=[]
print("ENCODING the dataset")
try:
    temp = './Facial_Recogntion/'+imageFileName
    image = cv2.imread(temp)
    # Convert it from BGR to RGB
    #Because opencv uses RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # detect face in the image and get its location (square boxes coordinates)
    boxes = face_recognition.face_locations(image, model='hog')

    # Encode the face into a 128-d embeddings vector
    encoding.append(np.array(face_recognition.face_encodings(image,boxes)[0]).tolist())
    
    if len(encoding) > 0 :
        #Create an array of encoding objects
        arr=[]
        for enc in encoding:
            arr.append({"encoding":enc})
        user = {
            u'name': name,
            u'surname': surname,
            u'title': title,
            u'fd':arr,
            u'email':email,
            u'active': True
        }
        # Add the new user to the database
        users_ref.document(name).set(user)
        if user:
            print(True)
        else: 
            print(False)
    #After this delete the image as if it was never there
    os.remove(temp)
    print('File removed')

except TypeError:
    print("An error occured while trying to encode the image or saving to the database")
