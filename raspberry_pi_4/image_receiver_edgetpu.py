import os
import io
import time
import pathlib
import numpy as np
from PIL import Image
from PIL import ImageFile
from flask import Flask, request, jsonify

from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify

# Specify the TensorFlow model and labels
script_dir = pathlib.Path(__file__).parent.absolute()
model_file = os.path.join(script_dir, 'modelV5_edgetpu.tflite')
label_file = os.path.join(script_dir, 'human_labels.txt')

# Initialize the TF interpreter
interpreter = edgetpu.make_interpreter(model_file)
interpreter.allocate_tensors()

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
    common.set_input(interpreter, img)
    interpreter.invoke()
    classes = classify.get_classes(interpreter, top_k=1)

    # Print the result
    result = classes[0]
    classification = result.id
    labels = dataset.read_label_file(label_file)
    
    string_response = f"{labels.get(result.id, result.id)}: {result.score}"
    print(string_response)
    
    # if it's a human, request a funcX task from the endpoint
    if classification == 1:
        print("sending the funcx task to the endpoint")
        try:
            res = fxc.run(img, endpoint_id=endpoint_id, function_id=human_uuid)
            # depending on the task and endpoint, it might take a while
            # to receive the results back. Modify the pause below.
            time.sleep(15)
            print(f"Result: {fxc.get_result(res)}")
        except Exception as e:
            print("Exception: {}".format(e))
        
    return string_response

@app.route("/test", methods=["GET"])
def test():
    print("Successfully received a GET request!")
    return "The server successfully received your GET request!"

app.run(host='0.0.0.0', port=8090)
