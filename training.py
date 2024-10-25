#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 00:23:28 2023

@author: kunalpathak9826
"""

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3
from keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob

def CycloneSeverity():
    #resize image
   IMAGE_SIZE = [224,224]
   train_path = '/Users/kunalpathak9826/Desktop/Cyclone/training'
   valid_path = '/Users/kunalpathak9826/Desktop/Cyclone/testing'

    # import the inception v3 and add preprocessing layer
    # imagenet weights are used
   inception = VGG19(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)
    # false because we dont want to use first and the last layer

    #for not training the existing weights
   for layer in inception.layers:
      layer.trainable = False
      
    #useful for getting number of output classes
   folders = glob('/Users/kunalpathak9826/Desktop/Cyclone/training/*')
   folders

   x = Flatten()((inception.output))
   prediction = Dense(len(folders), activation='softmax') (x) # softmax for multiple categories
    # creating a model object
   model = Model(inputs=inception.input, outputs=prediction)
   model.summary()
    #92 layers of conv2D/ 8 avg_pooling/ 3 max_pooling/ 1 fully connected layer

   model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # adptive movement estimation(ADAM) is extension of stochastic gradient descent to update network weightage during training
    # using image data generator to import the images from dataset
   train_datagen = ImageDataGenerator(rescale = 1./255,shear_range = 0.2,zoom_range = 0.2,horizontal_flip = True)
   test_datagen = ImageDataGenerator(rescale = 1./255)
   validation_datagen = ImageDataGenerator (rescale= 1./255)
    # convert the pixels in range [0,255] to range [0,1],will make images contributes more evenly to the total loss



   training_set = train_datagen.flow_from_directory('/Users/kunalpathak9826/Desktop/Cyclone/training',
                                                     target_size = (224, 224),batch_size = 18,class_mode = 'categorical')
   test_set = test_datagen.flow_from_directory('/Users/kunalpathak9826/Desktop/Cyclone/testing',
                                                target_size = (224, 224),batch_size = 18,class_mode = 'categorical')
   validation_set = validation_datagen.flow_from_directory('/Users/kunalpathak9826/Desktop/Cyclone/validation',
                                                            target_size = (224,224),batch_size = 18,class_mode = 'categorical') 
   r = model.fit_generator( training_set, validation_data = validation_set,
                             epochs=20, verbose=2, steps_per_epoch=len(training_set),validation_steps=len(validation_set))


   from matplotlib import pyplot
   import matplotlib.pyplot as plt
   import numpy as np
   img = image.load_img("/Users/kunalpathak9826/Desktop/Cyclone/testing/stage1(2).jpg")
   plt.imshow(img)

   import cv2
   cv2.imread("/Users/kunalpathak9826/Desktop/Cyclone/testing")
   training_set.class_indices
   import os
    #dir_path = ("/content/drive/MyDrive/Cyclone/testing")
   for i in os.listdir():
      img = image.load_img('/Users/kunalpathak9826/Desktop/Documents/IMG_4940 copy.jpg', target_size = (224,224))
      plt.imshow(img)
      plt.show()

      X = image.img_to_array(img)
      X = np.expand_dims(X,axis=0)
      val = model.predict(X)
      #images = np.vstack([X])
      #p = model.predict(images)
      #print ('Predicted: {}'.format(argmax(p)))
      if val.any() == 0:
         print ("Stage 1")
      elif val.any() == 1:
         print ("Stage 2")
      elif val.any() == 2:
         print ("Stage 3")
      elif val.any() == 3:
         print ("Stage 4")
      elif val.any() == 4:
         print ("Stage 5")
      else:
         print ("N0 Cyclone")
      break

   import logging
   logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
   CycloneSeverity()



    