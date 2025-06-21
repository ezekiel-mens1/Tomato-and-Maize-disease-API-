from flask import Flask, request, jsonify
from model import load_model, preprocess_image, predict_disease
from disease_info import DISEASES

app = Flask(__name__)
model = load_model()

@app.route('/', methods=['GET'])
def home():
    return "🍅🌽 Leaf-Disease API is running!", 200

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the request is multipart/form-data
    if 'file' not in request.files:
        return jsonify({'error': 'No file found in the request. Make sure to send a multipart/form-data with a "file" field.'}), 400

    image_file = request.files['file']

    if image_file.filename == '':
        return jsonify({'error': 'The file has no filename.'}), 400

    try:
        img = preprocess_image(image_file)
        class_id, prob = predict_disease(model, img)
    except Exception as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500

    disease = DISEASES.get(class_id, None)
    if disease is None:
        return jsonify({'error': 'Unknown prediction class.'}), 500

    return jsonify({
        'disease':     disease['name'],
        'probability': float(prob),
        'cause':       disease['cause'],
        'remedy':      disease['remedy']
    })

# For Render or Vercel
api = app

# Run locally
if __name__ == '__main__':
    app.run()
