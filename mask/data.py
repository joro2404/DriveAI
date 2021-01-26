import cv2, os, keras
import numpy as np
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator

TRAINING_DIR = "./data/train"
train_datagen = ImageDataGenerator(rescale=1.0/255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest')

train_generator = train_datagen.flow_from_directory(TRAINING_DIR, batch_size=10, target_size=(150, 150))

VALIDATION_DIR = "./data/test"
validation_datagen = ImageDataGenerator(rescale=1.0/255)

validation_generator = validation_datagen.flow_from_directory(VALIDATION_DIR, batch_size=10, target_size=(150, 150))