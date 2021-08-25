import os
import io
import time
import pathlib
import numpy as np
from PIL import Image
from PIL import ImageFile
from flask import Flask, request, jsonify

import tensorflow as tf

# Specify the TensorFlow model and labels
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
hello_uuid = "cb7c2dde-5626-4588-bf85-613b911ddaa8"
endpoint_id = "5d7ff732-623a-4d5d-81d0-f65519f53ab0"

# the face recognition function
face_uuid = "d594bf23-5372-4ab4-89a4-362736970444"

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
        
        res = fxc.run(byte_data, endpoint_id=endpoint_id, function_id=face_uuid)

        while True:
            try:
                human_class_results = fxc.get_result(res)
                print(f"Result: {human_class_results}")
                break
            except:
                continue
        return str(human_class_results)
        
    return string_response

@app.route("/test", methods=["GET"])
def test():
    print("Successfully received a GET request!")
    return "The server successfully received your GET request!"

app.run(host='0.0.0.0', port=8090)


