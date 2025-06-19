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
    files = list(request.files.values())
    
    # Validate exactly one file
    if len(files) == 0:
        return jsonify({'error': 'No file provided; please upload one image.'}), 400
    if len(files) > 1:
        return jsonify({'error': 'Too many files; please upload only one image at a time.'}), 400

    image_file = files[0]
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

# Vercel requires this named variable
api = app

# Only run locally when executed directly
if __name__ == '__main__':
    app.run()
