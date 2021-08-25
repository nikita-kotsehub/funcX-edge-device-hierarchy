# Thanks to devDeejay for the code:
# https://medium.com/softway-blog/building-a-facial-recognition-machine-learning-model-using-tensorflow-6e62fb349794

import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt

base_dir = "face_dataset/"

"""
    # Use `ImageDataGenerator` to rescale the images.
    # Create the train generator and specify where the train dataset directory, image size, batch size.
    # Create the validation generator with similar approach as the train generator with the flow_from_directory() method.
"""

IMAGE_SIZE = 224

BATCH_SIZE = 5

# We need a data generator which rescales the images
# Pre-processes the images like re-scaling and other required operations for the next steps
data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1. / 255,
    validation_split=0.2)

train_generator = data_generator.flow_from_directory(
    base_dir,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    subset='training')

# Create a validation generator
val_generator = data_generator.flow_from_directory(
    base_dir,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    subset='validation')

# Triggering a training generator for all the batches
for image_batch, label_batch in train_generator:
    break

# This will print all classification labels in the console
print(train_generator.class_indices)

# Creating a file which will contain all names in the format of next lines
labels = '\n'.join(sorted(train_generator.class_indices.keys()))

# Writing it out to the file which will be named 'labels.txt'
with open('labels.txt', 'w') as f:
    f.write(labels)

# Resolution of images (Width , Height, Array of size 3 to accommodate RGB Colors)
IMG_SHAPE = (IMAGE_SIZE, IMAGE_SIZE, 3)

base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')

base_model.trainable = False


model = tf.keras.Sequential([
    base_model,  # 1
    tf.keras.layers.Conv2D(32, 3, activation='relu'),  # 2
    tf.keras.layers.Dropout(0.2),  # 3
    tf.keras.layers.GlobalAveragePooling2D(),  # 4
    tf.keras.layers.Dense(3, activation='softmax')  # 5
])

# You must compile the model before training it.  Since there are two classes, use a binary cross-entropy loss.
# Since we have added more classification nodes, to our existing model, we need to compile the whole thing
# as a single model, hence we will compile the model now

# 1 - BP optimizer [Adam/Xavier algorithms help in Optimization]
# 2 - Weights are changed depending upon the 'LOSS' ['RMS, 'CROSS-ENTROPY' are some algorithms]
# 3 - On basis of which parameter our loss will be calculated? here we are going for accuracy
model.compile(optimizer=tf.keras.optimizers.Adam(),  # 1
              loss='categorical_crossentropy',  # 2
              metrics=['accuracy'])  # 3

# To see the model summary in a tabular structure
model.summary()

# Printing some statistics
print('Number of trainable variables = {}'.format(len(model.trainable_variables)))

# Train the model
# We will do it in 10 Iterations
epochs = 10

# Fitting / Training the model
history = model.fit(train_generator,
                    epochs=epochs,
                    validation_data=val_generator)


# Saving the Trained Model to the keras h5 format.
# So in future, if we want to convert again, we don't have to go through the whole process again
saved_model_dir = 'save/facial_recognition.h5'
model.save(saved_model_dir)
print("Model Saved to save/facial_recognition.h5")