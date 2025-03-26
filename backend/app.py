import os
import requests
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv  # Load environment variables

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get the Dropbox URL from .env
DROPBOX_URL = os.getenv("DROPBOX_URL")
MODEL_PATH = "\\random_forest_model.pkl"

def download_model():
    """Download the model from Dropbox if it's not already present."""
    try:
        if not DROPBOX_URL:
            raise ValueError("Dropbox URL is not set in .env file")

        response = requests.get(DROPBOX_URL)
        if response.status_code == 200:
            with open(MODEL_PATH, "wb") as f:
                f.write(response.content)
            print("✅ Model downloaded successfully.")
        else:
            print(f"❌ Failed to download model: {response.status_code}")
    except Exception as e:
        print(f"❌ Error downloading model: {e}")

# Download model if it doesn’t exist
if not os.path.exists(MODEL_PATH):
    download_model()

# Load model and preprocessing objects
try:
    model = joblib.load(MODEL_PATH)
    labelencoder = joblib.load("label_encoder.pkl")
    scaler = joblib.load("scaler.pkl")
    print("✅ Model and preprocessing objects loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model, labelencoder, scaler = None, None, None

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not labelencoder or not scaler:
        return jsonify({"error": "Model or preprocessing objects failed to load"}), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        feature_keys = ["Su", "Sy", "E", "G", "mu", "Ro"]
        if not all(key in data for key in feature_keys):
            return jsonify({"error": "Missing one or more required features"}), 400
        
        features = np.array([data[key] for key in feature_keys]).reshape(1, -1)
        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)
        material_name = labelencoder.inverse_transform(prediction)

        return jsonify({"predicted_material": material_name[0]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False)
