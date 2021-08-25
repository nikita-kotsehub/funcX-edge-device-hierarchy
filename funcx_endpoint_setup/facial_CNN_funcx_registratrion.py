from funcx.sdk.client import FuncXClient
fxc = FuncXClient()

def facial_prediction(img):
    try:
        from keras.utils import get_file
    except:
        from keras.utils.data_utils import get_file
        
    from tensorflow.keras.models import load_model 
    from PIL import Image
    import numpy as np
    import io
    
    model_path = get_file(
            'facial_model_1.h5',
            'https://github.com/nikita-kotsehub/funcx-facial-test-2/releases/download/0.1/fine_tuning.h5')
    
    model = load_model(model_path)
    
    img = Image.open(io.BytesIO(img))
    img = img.resize((224, 224))
    img = np.asarray(img)
    img = img / 255
    img = np.array([img])
    
    prediction = model.predict(img)
    
    label = np.argmax(prediction)
    confidence = np.max(prediction)
    
    return label, confidence

func_uuid = fxc.register_function(facial_prediction)
print(func_uuid)