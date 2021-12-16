# -*- coding: utf-8 -*-
"""Dog-Breed-Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ymQKM8IFdscD9VANYjm9Ji_aB8SvEjFf
"""

# Basic Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split
from IPython.display import Image

# Loading our data labels
labels_csv = pd.read_csv("/content/drive/MyDrive/Training Dog Breed/labels.csv")
labels_csv.head()

labels_csv.info()

labels_csv.describe()

len(labels_csv)

np.unique(labels_csv)

labels_csv['breed']

len(labels_csv['breed'])

labels_csv['breed'].value_counts()

labels_csv['breed'].value_counts().plot.bar(figsize=(25, 10))

# Visualize the Image using Ipython library

Image('/content/drive/MyDrive/Training Dog Breed/train/' + labels_csv['id'][444] + '.jpg')

# Check the breed name
labels_csv['breed'][444]

Image('/content/drive/MyDrive/Training Dog Breed/train/0a9322a30aff755dac328022266e3740.jpg')

labels_csv['breed'][444]

"""# Convert the Dataset into Labels and Data (Images) from labels_csv"""

Labels = labels_csv['breed']

Labels

len(Labels)

Image_Filename = ['drive/MyDrive/Training Dog Breed/train/' + fname + '.jpg' for fname in labels_csv['id']]
len(Image_Filename)

# visualize images using Image_Filename that we are going to use in colab
Image(Image_Filename[780])

Labels[780]

# Match the labels and Images path with actuall amount of Images in drive

import os

len(os.listdir('drive/MyDrive/Training Dog Breed/train/'))

# Match the Images with actual images in drive
if len((os.listdir('drive/MyDrive/Training Dog Breed/train/'))) == len(Image_Filename):
  print("Ready to go..")
else:
  print("Check the data labels")

# Match the labels with actual labels
if len((os.listdir('drive/MyDrive/Training Dog Breed/train/'))) == len(Labels):
  print("Ready to go..")
else:
  print("Check the data labels")

# One more check using Image_Filename 
Image(Image_Filename[7223])

# Let's have a look on our labels
Labels

# Let's have look on Inamge File Paths
Image_Filename

"""# **Now We have our Images and Labels Now Convert them into tensors**"""

Labels = Labels.to_numpy()

Labels.dtype

Labels

type(Labels)

# Find the unique names from our labels that will help us to compare each label to generate boolean values in future cells
Unique_Labels = np.unique(Labels)
Unique_Labels

len(Labels)

# Let's use our unique names to try one from labels and convert True False values in 0 & 1 using .astype(int) short function
(Labels[88] == Unique_Labels).astype(int)

# Let's convert our Numpy array labels into boolean labels and store them into a variable Bool_Labels
Bool_Labels = [label == Unique_Labels for label in Labels]
Bool_Labels

# Now convert the boolean labels from True False to 0 1 
Labels_Integer = [label.astype(int) for label in Bool_Labels]

Labels_Integer

# Check the length of labels before and after converting into number
len(Labels), len(Bool_Labels), len(Labels_Integer)

# Up to now we do have our labels ready in boolean form but not in tensor now convert only single to check how a tensor look like

# tf.constant is use to convert numpy array to tensor

tf.constant(Labels_Integer[876])

#  Let's check this on Bool_Labels

tf.constant(Bool_Labels[876])

# Let's convert our numpy array labels into tensor

tf.constant(Labels[876])

# so 'yorkshire_terrier' is like a girl and I like girls, so I will check this in my notebook 

plt.imshow(plt.imread(Image_Filename[876]));

# Now convert our Labels_Integers into tensor form

Labels_Tensor = [tf.constant(label) for label in Labels_Integer]

type(Labels_Tensor), len(Labels_Tensor)

# Check the one Tensor Labels

Labels_Tensor[987]

"""Upto Now We do have our Labels in the form of tensors:❤

## Now Convert Our Images into Tensors 

### For that we have to create a function that can take images as input and convert them into tensor
"""

# Let's create a function that convert images to tensors

# define the output image size in square
IMG_SIZE = 224

def Images_To_Tensors(images, img_size=IMG_SIZE):
  
  # use tensorflow to read the images and save into a variable
  image = tf.io.read_file(images)

  # convert the .jpg file to 3 colors channel
  image = tf.image.decode_jpeg(image, channels=3)

  # now resize the tensor values form 0-255 to 0-1
  image = tf.image.convert_image_dtype(image, tf.float32)

  # set up the shape of image of size 224, 224
  image = tf.image.resize(image, size=[img_size, img_size])

  # at the last return thte tensor
  return image

# Let's pass a filepath and check the output of our function
Images_To_Tensors(Image_Filename[87])

"""## Before Go the next step which is train our model, first create validation set and create data batches"""

Image_Filename

Bool_Labels

len(Image_Filename), len(Bool_Labels)

# Create X and Y

x = Image_Filename
y = Bool_Labels

# define the np seed
np.random.seed(43)

# create train and validation set using first 1000 only

x_train, x_val, y_train, y_val = train_test_split(x[:1000], y[:1000], test_size=0.2)

len(x_train), len(x_val), len(y_train), len(y_val)

# Hence our data is in the form of tensor tuple "(image, label)", let's create a function for that

def Get_Image_Label(image, label):
  """
  this function take images and labels(boolean) as input and return the tensor
  """
  img = Images_To_Tensors(image)
  labl = label

  return img, labl

# check the function on some iteration
Get_Image_Label(x[3], y[3])

# Create Data Batches

BATCH_SIZE = 32

def Data_To_Batches(x, y=False, batch_size=BATCH_SIZE, valid_set=False, test_set=False):
  """
  This function is default takes training data set but if it is the validation or test set's it will create data batches without any shake
  """

  # if the dataset is test_set, we possibly have no labels for test set
  if test_set:
    print("Creating Data Bathes on Test Set....")

    # use tensorflow to create data set on images only
    data = tf.data.Dataset.from_tensor_slices((tf.constant(x)))

    # now create data batches
    data_batch = data.map(Images_To_Tensors).batch(batch_size)

    # return the batch
    return data_batch
  
  # if the dataset is valid_set we do have images and labels 
  if valid_set:
    print("Creating Data Bathes on Validation Set....")

    # creating dataset
    data = tf.data.Dataset.from_tensor_slices((tf.constant(x),
                                               tf.constant(y)))
    
    # creaing data batches of length of batch_size and call Get_Image_Label function because we do have images and labels
    data_batch = data.map(Get_Image_Label).batch(batch_size)

    # return the data batches
    return data_batch
  
  # if the dataset is train data we do shuffle the data for training
  else:
    print("Creating Data Batches on Training Set....... ")

    # creating data batch
    data = tf.data.Dataset.from_tensor_slices((tf.constant(x),
                                               tf.constant(y)))
    
    # shuffle the data
    data = data.shuffle(buffer_size=len(x))

    # creating data batches
    data_batch = data.map(Get_Image_Label).batch(batch_size)

    # return the data batches
    return data_batch

train_data_batch = Data_To_Batches(x_train, y_train)

valid_data_batch = Data_To_Batches(x_val, y_val, valid_set=True)

train_data_batch

"""## up to now we do have our data into batches in the form of tensors

## Let's build our machine learning model and for that we need 3 things❤

### 1) Input Shape of images and labels
### 2) Output Shape of our labels (because we are pridicting dog breed name)

### 3) The URL of tensorflow model
"""

# defining input shape

INPUT_SHAPE = [None, IMG_SIZE, IMG_SIZE, 3]    # this is because our data batches have the same shape

# defining output shape of our labels
OUTPUT_SHAPE = len(Unique_Labels)   # because we are pridicting dog breed name

# picking up the model
MODEL_URL = "https://tfhub.dev/google/imagenet/mobilenet_v3_large_100_224/classification/5"

IMG_SIZE

"""# So up to now we have evertythin except our model

1. create a model by defining layers and compile this model by defining the loss, optimizer and metrics and then build this on input shape

2. create callbacks for our model before training, one for early_stopping and second for tensorboard

3. run our model by defining epochs
"""

# 1. Create a model
# function to create a model 

def create_model(input_shape=INPUT_SHAPE, output_shape=OUTPUT_SHAPE, model_url=MODEL_URL):

  # define the layers of model 
  model = tf.keras.models.Sequential([
                                      hub.KerasLayer(model_url), # first layer 
                                      tf.keras.layers.Dense(units=output_shape,
                                                            activation="softmax") # the output layer
  ])

  # compile the model
  model.compile(loss=tf.keras.losses.CategoricalCrossentropy(),
                optimizer=tf.keras.optimizers.Adam(),
                metrics=["accuracy"])
  
  # build the model with input shape
  model.build(input_shape)

  # return the build model
  return model

model = create_model()

# check the summary of model

model.summary()

# Commented out IPython magic to ensure Python compatibility.
# 2. Let's create our callbacks 

# function to define callback for tensorboard

# first we need tensorboad extension and we define it as below
# %load_ext tensorboard

# import the datetime library to log the current data and time into tensorboard directory
import datetime

# create a function to build tensorboard callback
def create_tensorboard_callback():
  mydir = os.path.join("/content/drive/MyDrive/Training Dog Breed/tensorboard_callback",
                       # now define the time to log
                       datetime.datetime.now().strftime("%y%m%d-%h%m%s"))
  # return the tensorboard callback
  return tf.keras.callbacks.TensorBoard(mydir)

# now define early stopping callback

early_stopping = tf.keras.callbacks.EarlyStopping(monitor="accuracy",
                                                  patience=2)

# 3. now run the model on training dataset 

# define the epochs for model to check the patterns on training datasets
NUM_EPOCS = 30 #@param {type:"slider", min:10, max:100, step:10}

# create a function that train our model

def train_model():

  # create a model
  model = create_model()

  # create callbacks
  tensorboard = create_tensorboard_callback()

  # fit the model
  model.fit(x=train_data_batch,
            validation_data=valid_data_batch,
            epochs=NUM_EPOCS,
            validation_freq=1,
            callbacks=[tensorboard, early_stopping])
  
  # return the trained model
  return model

model = train_model()

# check the loss and accuracy of model on training dataset

test_loss, test_acc = model.evaluate(train_data_batch)

# check the loss and accuracy of model on validation dataset

val_loss, val_acc = model.evaluate(valid_data_batch)

len(y)

Unique_Labels

