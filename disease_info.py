# disease_info.py

# The list of classes your model predicts, in order
CLASS_LABELS = [
    "Maize_Blight",
    "Maize_Common_Rust",
    "Maize_Healthy",
    "Maize_leaf_spot",
    "Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___healthy",
    "unknown"
]

# Detailed causes for each class
CAUSES = {
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
        "Caused by various fungal pathogens like Bipolaris maydis.",
        "Spread through infected debris and windborne spores.",
        "Favored by warm, wet conditions."
    ],
    "Tomato_Yellow_Leaf_Curl_Virus": [
        "Caused by a virus transmitted by whiteflies.",
        "Spread through infected plants and whitefly populations.",
        "Favored by warm climates with high whitefly activity."
    ],
    "Tomato___Bacterial_spot": [
        "Caused by Xanthomonas bacteria.",
        "Spread through infected seeds, transplants, and water splash.",
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

# Recommended remedies for each class
REMEDIES = {
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
        "No immediate action needed beyond normal good agronomic practices (weeding, proper irrigation, etc.).",
        "Continue with standard fertilizer program as guided by soil testing."
    ],
    "Maize_leaf_spot": [
        "Rotate with non-corn crops to break the pathogen’s life cycle.",
        "Apply a preventive fungicide (e.g., mancozeb or a strobilurin–triazole mix) when conditions are favorable for disease spread.",
        "Ensure balanced nutrients (especially nitrogen) to keep plants healthy; stressed plants are more vulnerable."
    ],
    "Tomato_Yellow_Leaf_Curl_Virus": [
        "Control whiteflies using insecticidal soaps or oils (like neem oil).",
        "Remove and destroy infected plants to stop the virus cycle."
    ],
    "Tomato___Bacterial_spot": [
        "Use certified disease-free seeds or transplants.",
        "Avoid overhead watering; switch to drip irrigation if possible.",
        "Provide adequate nutrients (NPK with trace elements). Don’t overdo nitrogen since dense foliage increases humidity and disease spread."
    ],
    "Tomato___Early_blight": [
        "Remove and destroy infected leaves to reduce the spread.",
        "Rotate crops and avoid planting tomatoes in the same spot each year.",
        "Use balanced tomato fertilizer with proper nitrogen, phosphorus, potassium, and calcium for strong, disease-tolerant plants."
    ],
    "Tomato___healthy": [
        "No immediate action needed."
    ],
    "unknown": [
        "No remedies available for unknown conditions."
    ]
}

# Combine into one dict keyed by class index
DISEASES = {
    idx: {
        "name": CLASS_LABELS[idx],
        "cause": CAUSES.get(CLASS_LABELS[idx], ["No cause information available."]),
        "remedy": REMEDIES.get(CLASS_LABELS[idx], ["No remedy information available."])
    }
    for idx in range(len(CLASS_LABELS))
}
