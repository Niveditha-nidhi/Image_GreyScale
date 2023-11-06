# -*- coding: utf-8 -*-
"""alpha_version_notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19zER0T3H4AglEvGbjDkgERURSdKvcChh
"""

from keras.layers import Conv2D, UpSampling2D, InputLayer, Conv2DTranspose
from keras.layers import Activation, Dense, Dropout, Flatten
#from keras.layers.normalization import BatchNormalization
from tensorflow.keras.layers import BatchNormalization
from keras.models import Sequential
from keras.callbacks import TensorBoard
#from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from tensorflow.keras.preprocessing.image import array_to_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import load_img
from skimage.color import rgb2lab, lab2rgb, rgb2gray, xyz2lab
from skimage.io import imsave
import numpy as np
import os
import random
import tensorflow as tf

# Get images
from PIL import Image
import IPython.display as display

# Replace 'image.jpg' with the filename of your uploaded image
uploaded_image_path = '/content/bw.png'
image = img_to_array(load_img(uploaded_image_path))
image = np.array(image, dtype=float)

from PIL import Image
import IPython.display as display

# Replace 'image.jpg' with the filename of your uploaded image
uploaded_image_path = '/content/bw.png'

# Open the uploaded image
image = Image.open(uploaded_image_path)

# Display the image
display.display(image)

import numpy as np
from skimage.color import rgb2lab

# Assuming 'image' is your original RGB image with shape (400, 400, 3)
# Convert RGB image to LAB color space and extract L channel (X) and AB channels (Y)
image_lab = rgb2lab(1.0/255 * image)
X = image_lab[:, :, 0]  # L channel (grayscale)
Y = image_lab[:, :, 1:]  # AB channels

# Normalize the values in Y to the range [-1, 1]
Y /= 128

# Add batch dimension to X and Y
X = X.reshape(1, 400, 400, 1)  # Shape: (1, 400, 400, 1)
Y = Y.reshape(1, 400, 400, 2)  # Shape: (1, 400, 400, 2)

# Print the shape of X and Y
print("X shape:", X.shape)  # Should be (1, 400, 400, 1)
print("Y shape:", Y.shape)  # Should be (1, 400, 400, 2)

# Building the neural network
model = Sequential()
model.add(InputLayer(input_shape=(None, None, 1)))
model.add(Conv2D(8, (3, 3), activation='relu', padding='same', strides=2))
model.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(16, (3, 3), activation='relu', padding='same', strides=2))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same', strides=2))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(2, (3, 3), activation='tanh', padding='same'))

# Finish model
model.compile(optimizer='rmsprop',loss='mse')

model.fit(x=X,
    y=Y,
    batch_size=1,
    epochs=1000)



print(model.evaluate(X, Y, batch_size=1))
output = model.predict(X)
output *= 128
# Output colorizations
cur = np.zeros((400, 400, 3))
cur[:,:,0] = X[0][:,:,0]
cur[:,:,1:] = output[0]
imsave("img_result1.png", lab2rgb(cur))
imsave("img_gray_version1.png", rgb2gray(lab2rgb(cur)))
print(rgb2gray(lab2rgb(cur)))

