from flask import Flask, request, jsonify
from model import load_model, preprocess_image, predict_disease
from disease_info import DISEASES
import base64

app = Flask(__name__)
model = load_model()

@app.route('/', methods=['GET'])
def home():
    return "🍅🌽 Leaf-Disease API is running!", 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        image_data = None

        # Log for debugging
        print("Request content type:", request.content_type)
        print("Request files:", request.files)
        print("Request form:", request.form)

        # Case 1: multipart/form-data (Flutter, Postman)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'Uploaded file has no name.'}), 400
            image_data = file.read()

        # Case 2: base64-encoded image in JSON (e.g., mobile apps)
        elif request.is_json:
            data = request.get_json()
            if 'image' not in data:
                return jsonify({'error': 'No "image" field found in JSON data.'}), 400
            try:
                image_data = base64.b64decode(data['image'])
            except Exception:
                return jsonify({'error': 'Invalid base64 image data.'}), 400

        else:
            return jsonify({'error': 'Unsupported content type. Use multipart/form-data or application/json.'}), 400

        # Process image and make prediction
        img = preprocess_image(image_data)
        class_id, prob = predict_disease(model, img)

        disease = DISEASES.get(class_id)
        if disease is None:
            return jsonify({'error': 'Unknown prediction class.'}), 500

        return jsonify({
            'disease': disease['name'],
            'confidence': float(prob),
            'cause': disease['cause'],
            'remedy': disease['remedy']
        })

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# For Vercel/Render
api = app

# For local testing
if __name__ == '__main__':
    app.run()
