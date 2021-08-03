import os
import io
import time
import pathlib
import numpy as np
from PIL import Image
from PIL import ImageFile
from flask import Flask, request, jsonify

import tensorflow as tf

# Specify the TensorFlow model, labels, and image
script_dir = pathlib.Path(__file__).parent.absolute()
model_file = os.path.join(script_dir, 'modelV5.tflite')
#label_file = os.path.join(script_dir, 'human_labels.txt')
labels = ['nonhuman', 'human']

# Initialize the TF interpreter
interpreter = tf.lite.Interpreter(model_path=model_file)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Allow Pillow to load truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Initiate FuncXClient. The very first time, it will prompt you to
# authorize via Globus
try:
    from funcx.sdk.client import FuncXClient
    fxc = FuncXClient()
except:
    print("Couldn't start a funcX client")

# define the functions and endpoint uuids
hello_uuid = "8b9d784c-d661-44eb-9df0-0f3e1ef3e762"
endpoint_id = "0e9c7503-3291-41bd-80b7-ae4f9dd91924"
human_uuid = "849b13dc-fdcb-4e73-a927-315155d9960a"

# define the image size for your neural network model
image_x_size = 80
image_y_size = 80

app = Flask(__name__)
 
@app.route('/image_receiver', methods = ["POST"])
def image_receiver():
    # receive the bytearray data from Nano RP2040 Connect
    byte_data = request.data
    img = Image.open(io.BytesIO(byte_data))
    
    # Comment out if you don't want to see the received images
    img.show()
    
    # Convert the image to an appropriate Machine Learning input
    img = img.resize((image_x_size, image_y_size))
    img = np.asarray(img)
    img = img / 255
    img = np.array([img], dtype='float32')
    
    # Run an inference
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Print the result
    classification = np.argmax(output_data[0])
    score = np.max(output_data[0])
    label = labels[classification]

    string_response = f"{label}: {score}"
    print(string_response)
    
    # if it's a human, request a funcX task from the endpoint
    if classification == 1:
        print("sending the funcx task to the endpoint")
        try:
            res = fxc.run(img, endpoint_id=endpoint_id, function_id=human_uuid)
            # depending on the task and endpoint, it might take a while
            # to receive the results back. Modify the pause time below.
            time.sleep(5)
            print(f"Result: {fxc.get_result(res)}")
        except Exception as e:
            print("Exception: {}".format(e))
        
    return string_response

@app.route("/test", methods=["GET"])
def test():
    print("Successfully received a GET request!")
    return "The server successfully received your GET request!"

app.run(host='0.0.0.0', port=8090)

