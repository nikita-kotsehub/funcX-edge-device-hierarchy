from flask import Flask, request
try:
    from keras.utils import get_file
except:
    from keras.utils.data_utils import get_file

from tensorflow.keras.models import load_model 
from PIL import Image
import numpy as np
import io

# download the model
model_path = get_file(
        'facial_model_1.h5',
        'https://github.com/nikita-kotsehub/funcx-facial-test-2/releases/download/0.1/fine_tuning.h5')

model = load_model(model_path)

app = Flask(__name__)

# define Flask apps
@app.route('/face_recognition', methods=['POST'])
def face_recognition():
    # get the byte array data and convert it to the appropriate machine learning input
    img = request.data
    img = Image.open(io.BytesIO(img))
    img = img.resize((224, 224))
    img = np.asarray(img)
    img = img / 255
    img = np.array([img])
    
    # predict
    prediction = model.predict(img)
    
    label = np.argmax(prediction)
    confidence = np.max(prediction)
    
    return {'label':str(label), 'confidence':str(confidence)}

# you can test your server with this app
@app.route('/get', methods=['GET'])
def get():
    print("test")
    return('Hello World')

app.run(host='0.0.0.0', port=8090)