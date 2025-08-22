from flask import Flask, request, jsonify
from ai_edge_litert.interpreter import Interpreter
import numpy as np
from PIL import Image
from disease_info import DISEASES
import io, base64

app = Flask(__name__)

# Load TFLite model
interpreter = Interpreter(model_path="")
interpreter.allocate_tensors()

# Causes and remedies
remedies = {
    "Maize_Blight": [
        "Use disease-resistant maize varieties if available.",
        "Rotate crops and bury or remove any infected debris to reduce sources of the fungus.",
        "Provide balanced NPK and ensure sufficient nitrogen to maintain vigorous plant growth."
    ],
    "Maize_Common_Rust": [
        "Remove plant residues and volunteer corn to reduce overwintering spores.",
        "Use a strobilurin (azoxystrobin) or triazole (propiconazole) fungicide at early signs of rust.",
        "Avoid over-fertilizing with nitrogen, as overly lush growth can sometimes be more susceptible."
    ],
    "Maize_Healthy": [
        "No immediate action needed beyond normal good agronomic practices.",
        "Continue with standard fertilizer program as guided by soil testing."
    ],
    "Maize_leaf_spot": [
        "Rotate with non-corn crops to break the pathogen’s life cycle.",
        "Apply a preventive fungicide when conditions are favorable.",
        "Ensure balanced nutrients to keep plants healthy."
    ],
    "Tomato_Yellow_Leaf_Curl_Virus": [
        "Control whiteflies using insecticidal soaps or oils (like neem oil).",
        "Remove and destroy infected plants."
    ],
    "Tomato___Bacterial_spot": [
        "Use certified disease-free seeds or transplants.",
        "Avoid overhead watering; use drip irrigation.",
        "Provide adequate nutrients without overdoing nitrogen."
    ],
    "Tomato___Early_blight": [
        "Remove infected leaves.",
        "Rotate crops yearly.",
        "Use balanced fertilizer to boost plant resistance."
    ],
    "Tomato___healthy": [
        "No immediate action needed."
    ],
    "unknown": [
        "The issue could not be classified."
    ]
}

causes = {
    "Maize_Blight": [
        "Caused by the fungus Exserohilum turcicum.",
        "Spread through infected crop debris and windborne spores.",
        "Favored by warm, humid conditions."
    ],
    "Maize_Common_Rust": [
        "Caused by the fungus Puccinia sorghi.",
        "Spread by windborne spores from infected plants.",
        "Favored by cool, moist conditions."
    ],
    "Maize_Healthy": [
        "No disease present; healthy growth due to good agronomic practices."
    ],
    "Maize_leaf_spot": [
        "Caused by fungal pathogens like Bipolaris maydis.",
        "Spread through infected debris and spores.",
        "Favored by warm, wet conditions."
    ],
    "Tomato_Yellow_Leaf_Curl_Virus": [
        "Caused by a virus transmitted by whiteflies.",
        "Spread through infected plants and whitefly activity.",
        "Favored by warm climates."
    ],
    "Tomato___Bacterial_spot": [
        "Caused by Xanthomonas bacteria.",
        "Spread through seeds, transplants, and water splash.",
        "Favored by warm, wet conditions."
    ],
    "Tomato___Early_blight": [
        "Caused by the fungus Alternaria solani.",
        "Spread through infected debris, seeds, and water splash.",
        "Favored by warm, humid conditions."
    ],
    "Tomato___healthy": [
        "No disease present; healthy growth due to good agronomic practices."
    ],
    "unknown": [
        "The issue could not be classified."
    ]
}

# The keys in the output layer must match these class names exactly
disease_classes = list(causes.keys())

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((96, 96))  # Adjust based on model input
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_disease(image):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index'])

    max_index = np.argmax(prediction[0])
    predicted_class = disease_classes[max_index] if max_index < len(disease_classes) else "unknown"
    confidence = float(prediction[0][max_index])

    return {
        "disease": predicted_class,
        "confidence": confidence,
        "causes": causes.get(predicted_class, ["No causes available."]),
        "remedies": remedies.get(predicted_class, ["No remedies available."])
    }

@app.route('/', methods=['GET'])
def home():
    return "🍅🌽 Leaf-Disease API is running!", 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        image_data = None

        # Case 1: multipart/form-data
        if 'file' in request.files:
            image_data = request.files['file'].read()

        # Case 2: base64 in JSON
        elif request.is_json:
            data = request.get_json()
            if 'image' not in data:
                return jsonify({'error': 'No "image" field found in JSON.'}), 400
            try:
                image_data = base64.b64decode(data['image'])
            except Exception:
                return jsonify({'error': 'Invalid base64 image data.'}), 400

        if not image_data:
            return jsonify({'error': 'No image data received.'}), 400

        # Preprocess and predict
        processed_image = preprocess_image(image_data)
        result = predict_disease(processed_image)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Required by Render/Vercel
api = app

# Local testing
if __name__ == '__main__':
    app.run(debug=True)
