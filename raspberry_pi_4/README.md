# Raspberry Pi 4 Image Receiver

The ```image_receiver``` receives a bytearray image from Nano RP2040, converts it to a proper Machine Learning input, and uses a pre-trained convolutional neural network to classify if it's an image of a human or not. If it is, it requests a funcX task from an endpoint. 

There are two versions:
1. Use `image_receiver_edgetpu` if you have the [Coral Edge TPU USB Accelerator][1]. It drastically speeds up inference for tensorflow lite models. If you decide to use your own model, at first you need to convert your `.tflite` model into an edge tpu specific model. You can do it with [this Google Colab][2].
2. `image_receiver_tflite` runs inference with a regular .tflite model on the Raspberry Pi 4 CPU. 

## Dependencies
* OS: Raspbian
* Python 3.7
* os
* io
* time
* pathlib
* numpy
* PIL/Pillow 

### For Coral USB Accelerator
* pycoral

### For Tensorflow Lite
* tensorflow

## Functions

Both functions are identical, besides the different inference processes. The main function runs a Flask server. Upon receiving the bytearray image from the Nano RP2040, it converts the image to a proper Machine Learning input and runs inference with the pre-trained Tensorflow model. If it classifies the image as `human`, it requests a funcX tasks from the endpoint.

- You need to provide your personal `endpoint_id`. It can be an AWS instance, a super-computer, or even your laptop. 
- You can use the `hello_uuid` to test your code. It is a simple function that returns 'Hello World'. The 'human_uuid' function has files specific to my endpoint, so you will not be able to use it. You can also easily register your own function and use it.
- Learn more about funcX [here][3]. Install it [[4]]. Practice it [[5]].
- If have the Coral USB Accelerator, make sure to install its dependencies first by following [this guide][6].


[1]: https://coral.ai/products/accelerator/ 
[2]: https://colab.research.google.com/github/google-coral/tutorials/blob/master/compile_for_edgetpu.ipynb#scrollTo=joxrIB0I3cdi
[3]: https://funcx.org/
[4]: https://funcx.readthedocs.io/en/latest/quickstart.html
[5]: https://mybinder.org/v2/gh/funcx-faas/examples/HEAD?filepath=notebooks%2FIntroduction.ipynb 
[6]: https://coral.ai/docs/accelerator/get-started/#requirements
