from __future__ import print_function
import numpy as np
from PIL import Image

import keras

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input,decode_predictions

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Lambda
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization as BN
from keras.layers import GaussianNoise as GN
from keras.optimizers import SGD, Adam, RMSprop
from keras.models import Model
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from keras.callbacks import ReduceLROnPlateau

from keras.callbacks import LearningRateScheduler as LRS
from keras.preprocessing.image import ImageDataGenerator

from keras import backend
from keras.models import Model
from scipy.optimize import fmin_l_bfgs_b
from scipy.misc import imsave

batch_size = 5
num_classes = 20
epochs = 500

#### LOAD AND TRANSFORM

# Load 
x_train = np.load('x_train.npy')
x_test = np.load('x_test.npy')

y_train = np.load('y_train.npy')
y_test = np.load('y_test.npy')

# Stats
print(x_train.shape)
print(y_train.shape)

print(x_test.shape)
print(y_test.shape)

## Transforms
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

y_train = y_train.astype('float32')
y_test = y_test.astype('float32')


x_train /= 255
x_test /= 255


## Labels
y_train=y_train-1

y_test=y_test-1

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# VGG pre-trained

model1=VGG16(weights='imagenet', include_top=False)
model1.summary()


model2=VGG16(weights='imagenet', include_top=False)
model2.summary()

for i, layer in enumerate(model1.layers):
    layer.name = layer.name + 'a'
    layer.trainable = True

for i, layer in enumerate(model2.layers):
    layer.name = layer.name + 'b'
    layer.trainable = True

def outer_product(x):
  phi_I = tf.einsum('ijkm,ijkn->imn',x[0],x[1])		# Einstein Notation  [batch,1,1,depth] x [batch,1,1,depth] -> [batch,depth,depth]
  phi_I = tf.reshape(phi_I,[-1,512*512])	        # Reshape from [batch_size,depth,depth] to [batch_size, depth*depth]
  phi_I = tf.divide(phi_I,7*7)								  # Divide by feature map size [sizexsize]

  y_ssqrt = tf.multiply(tf.sign(phi_I),tf.sqrt(tf.abs(phi_I)+1e-12))		# Take signed square root of phi_I
  z_l2 = tf.nn.l2_normalize(y_ssqrt, dim=1)								              # Apply l2 normalization
  return z_l2

conv1=model1.layers[-1].output
conv2=model2.layers[-1].output

x = Lambda(outer_product, name='outer_product')([conv1,conv2])

predictions=Dense(num_classes, activation='softmax', name='predictions')(x)

model = Model(inputs=[model1.input,model2.input], outputs=predictions)
  
model.summary()

## OPTIM AND COMPILE
opt = Adam(lr=0.001, decay=1e-6)

model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

# DEFINE A LEARNING RATE SCHEDULER
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, cooldown=1,
                              patience=10, min_lr=0.005)


##############################################
## DEFINE A DATA AUGMENTATION GENERATOR
## WITH MULTIPLE INPUTS
##############################################

datagen = ImageDataGenerator(
  width_shift_range=0.2,
  height_shift_range=0.2,
  rotation_range=20,
  zoom_range=[1.0,1.2],
  horizontal_flip=True)



def multiple_data_generator(generator, X,Y,bs):
    genX = generator.flow(X, Y,batch_size=bs)
    while True:
      [Xi,Yi] = genX.next()
      yield [Xi,Xi],Yi

##############################################


## TRAINING with DA and LRA
history=model.fit_generator(multiple_data_generator(datagen,x_train, y_train,batch_size),
                            steps_per_epoch=len(x_train) / batch_size, 
                            epochs=epochs,
                            validation_data=([x_test, x_test], y_test),
                            callbacks=[reduce_lr],
                            verbose=1)



