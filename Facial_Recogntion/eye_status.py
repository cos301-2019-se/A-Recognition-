##
# Filename: eye_status.py
# Version: V1.0
# Author: Adrian le Grange
# Project name: A-Recognition (Advance)
# Organization: Singularity
# Funtional description: Used to build a model to detect open and closed eyes. Provides functions for the loading and saving of the model.

import os
from PIL import Image
import numpy as np

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import AveragePooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator

from imageio import imread
import scipy as sp

IMG_SIZE = 24

##
#Function retrives all training samples, produces more samples. Returns generator objects used for training function
#
#@return: tuple of generator objects
def collect():
	train_datagen = ImageDataGenerator(
			rescale=1./255,
			shear_range=0.2,
			horizontal_flip=True, 
		)

	val_datagen = ImageDataGenerator(
			rescale=1./255,
			shear_range=0.2,
			horizontal_flip=True,		)

	absPath = os.path.dirname(os.path.abspath(__file__))
	fileName = os.path.join(absPath, 'dataset/train')
	train_generator = train_datagen.flow_from_directory(
	    directory=fileName,
	    target_size=(IMG_SIZE, IMG_SIZE),
	    color_mode="grayscale",
	    batch_size=32,
	    class_mode="binary",
	    shuffle=True,
	    seed=42
	)

	fileName = os.path.join(absPath, 'dataset/val')
	val_generator = val_datagen.flow_from_directory(
	    directory=fileName,
	    target_size=(IMG_SIZE, IMG_SIZE),
	    color_mode="grayscale",
	    batch_size=32,
	    class_mode="binary",
	    shuffle=True,
	    seed=42
	)
	return train_generator, val_generator

##
#Function that saves the trained net to a file
#
#@param model: The neural net
def save_model(model):
	absPath = os.path.dirname(os.path.abspath(__file__))
	modelFile = os.path.join(absPath, 'model.json')
	model_json = model.to_json()
	with open(modelFile, "w") as json_file:
		json_file.write(model_json)
	# serialize weights to HDF5
	model.save_weights("model.h5")

##
#Function that constructs a neural net from file
#
#@return: The neural net
def load_model():
	absPath = os.path.dirname(os.path.abspath(__file__))
	modelFile = os.path.join(absPath, 'model.json')
	json_file = open(modelFile, 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights("model.h5")
	loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return loaded_model

##
#Function that trains the neural net with the data from the generators. The saves it to a file
#
#@param train_generator: Generator for training data
#@param val_generator: Generates corresponding value for the training data
def train(train_generator, val_generator):
	STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
	STEP_SIZE_VALID=val_generator.n//val_generator.batch_size

	print('[LOG] Intialize Neural Network')
	
	model = Sequential()

	model.add(Conv2D(filters=6, kernel_size=(3, 3), activation='relu', input_shape=(IMG_SIZE,IMG_SIZE,1)))
	model.add(AveragePooling2D())

	model.add(Conv2D(filters=16, kernel_size=(3, 3), activation='relu'))
	model.add(AveragePooling2D())

	model.add(Flatten())

	model.add(Dense(units=120, activation='relu'))

	model.add(Dense(units=84, activation='relu'))

	model.add(Dense(units=1, activation = 'sigmoid'))


	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

	model.fit_generator(generator=train_generator,
	                    steps_per_epoch=STEP_SIZE_TRAIN,
	                    validation_data=val_generator,
	                    validation_steps=STEP_SIZE_VALID,
	                    epochs=20
	)
	save_model(model)

resolution = (IMG_SIZE, IMG_SIZE)

##
#Function that uses given neural net to determine if the given image has a closed or open eye
#
#@param img: A string containing a sequence of past eye statuses
#@param model: The neural net that will be used to determine eye status
#@return: Returns string with the result
#
#Returns "open", "closed" or "idk"
def predict(img, model):
	img = Image.fromarray(img, 'RGB').convert('L')
	img = np.array(img.resize(resolution, Image.ANTIALIAS)).astype('float32')
	img /= 255
	img = img.reshape(1,IMG_SIZE,IMG_SIZE,1)
	prediction = model.predict(img)
	if prediction < 0.1:
		prediction = 'closed'
	elif prediction > 0.9:
		prediction = 'open'
	else:
		prediction = 'idk'
	return prediction

##
#Function that determines the accuracy of the neural net
#
#@param X_test: X_test object
#@param y_test: Y_test_object
def evaluate(X_test, y_test):
	model = load_model()
	print('Evaluate model')
	loss, acc = model.evaluate(X_test, y_test, verbose = 0)
	print(acc * 100)

if __name__ == '__main__':	
	train_generator , val_generator = collect()
	train(train_generator,val_generator)
