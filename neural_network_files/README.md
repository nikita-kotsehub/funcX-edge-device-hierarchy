# Neural Network Files

The project uses two Neural Networks.

# Human vs. Nonhuman CNN

The Human vs. Nonhuman Convolutional Neural Network classifies an image into human or nonhuman. The initial dataset, pre-processing, and other functions were borrowed from @agikarasugi's [HumanBinaryClassificationSuite][1]. We expanded the dataset with more images [[2]], [[3]], [[4]] and improved the model.

- Use 'modelV5.tflite' to do inference with Tensorflow Lite.
- Use 'modelV5_edgetpu.tflite' to do inference with Coral USB Accelerator.
- You can modify the dataset and model. Convert it to `.tflite` for inference on RPi 4. If using Coral USB Accelerator, also convert it to `_edgetpu`-specific model using [this Google Colab][5].

## Dependencies
* os
* numpy
* pickle
* numpy
* matplotlib
* datetime
* tensorflow
* cv2
* sklearn

# Temperature Prediction DNN

The Temperature Prediction DNN in `temperature_prediction_DNN.ipynb` is a simple neural network with a single neuron written for demonstrative purposes of running AI at the edge. After training the model and converting it to `.tflite`, the weights and biases are exported as `w1_temp.txt` and `b1_temp.txt`. We use them for temperature prediction on Arduino Nano RP2040 Connect.

## Dependencies
* numpy
* tensorflow
* matplotlib

# Facial Prediction CNN
The 'facial_recognition.h5` model classifies the human as either Ben Affleck, Madonna, or the repository's author. You can change the training images so it learns to classify your face. Thanks to devDeejay for providing the [Medium article][6] and [code][7] for the model.

## Contributing
- Improve the Human Classifier model's accuracy (although keep in mind the training time and the model weight).
- Find a more efficient way to export weights from `.tflite` model in `temperature_prediction_DNN.ipynb`.

[1]: https://github.com/agikarasugi/HumanBinaryClassificationSuite
[2]: https://www.kaggle.com/sanikamal/horses-or-humans-dataset
[3]: http://vision.stanford.edu/Datasets/40actions.html
[4]: https://www.kaggle.com/robinreni/house-rooms-image-dataset
[5]: https://colab.research.google.com/github/google-coral/tutorials/blob/master/compile_for_edgetpu.ipynb#scrollTo=joxrIB0I3cdi
[6]:https://medium.com/softway-blog/building-a-facial-recognition-machine-learning-model-using-tensorflow-6e62fb349794
[7]:https://gist.github.com/devDeejay/5f2cc735cb9cf1d2263273f646fed7ef


