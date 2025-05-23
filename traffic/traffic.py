import cv2
import numpy as np
import os
import sys
import tensorflow as tf
#import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    images = list()
    labels = list()

    #use cvs opencv to read each image as numpy.ndarray
    for catfold in os.listdir(data_dir):
        for img_name in os.listdir(os.path.join(data_dir,catfold)):
            labels.append(catfold)

            img = cv2.imread(os.path.join(data_dir,catfold,img_name))
            h, w, ch = img.shape

            #resize to 30 30
            img_resize = cv2.resize(img,(IMG_WIDTH,IMG_HEIGHT))
            images.append(img_resize)
            #display the image (debugging)
            #cv2.imshow('original',img)
            #cv2.imshow('resized',img_resize)
           
    return images, labels
            
                             

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    # Create a convolutional neural network
    model = tf.keras.models.Sequential(name='trafiic_nn_seq')

    # Add a hidden layer with 8 units, with ReLU activation
    model.add(tf.keras.layers.Dense(12, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), activation="relu"))


        # Convolutional layer. Learn 32 filters using a 3x3 kernel
    model.add(tf.keras.layers.Conv2D(48, (3, 3), activation="relu"))

        # Max-pooling layer, using 2x2 pool size
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(8, 8)))

        # Flatten units
    model.add(tf.keras.layers.Flatten())

        # Add a hidden layer with dropout
    model.add(tf.keras.layers.Dense(254, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.2))

        # Add an output layer with output units for all 10 digits
        #tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
  
    # Add output layer with NUM_CATEGORIES unit, with sigmoid activation
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))
    
    # Display the model's architecture
    model.summary()

    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


if __name__ == "__main__":
    main()
