import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Path to your TFLite model file
MODEL_PATH = 'mobilenetv2_model (2).tflite'

def load_model():
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    return interpreter

def preprocess_image(file, img_size=(96, 96)):
    img = Image.open(io.BytesIO(file.read())).convert('RGB')
    img = img.resize(img_size)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)

def predict_disease(interpreter, img_array):
    inp_details  = interpreter.get_input_details()
    out_details = interpreter.get_output_details()
    interpreter.set_tensor(inp_details[0]['index'], img_array)
    interpreter.invoke()
    output = interpreter.get_tensor(out_details[0]['index'])
    class_id = int(np.argmax(output))
    prob     = float(np.max(output))
    return class_id, prob
