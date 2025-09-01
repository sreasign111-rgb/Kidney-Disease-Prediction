# This Flask application serves the front-end and handles predictions.

from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load the trained model. This is done once when the application starts.
MODEL_PATH = os.path.join('model', 'Kidney_Disease_Prediction_Model.pkl')
loaded_model = None

try:
    if os.path.exists(MODEL_PATH):
        loaded_model = joblib.load(MODEL_PATH)
        print("Machine learning model loaded successfully.")
    else:
        print(f"Error: Model file '{MODEL_PATH}' not found. Please run 'train_model.py' first.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")

# --- Flask Routes ---

@app.route('/')
def home():
    """Renders the main HTML page for the predictor."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives patient data, makes a prediction using the model,
    and returns the result as JSON.
    """
    if loaded_model is None:
        return jsonify({'error': 'Model not available. Please check the server logs.'}), 500

    try:
        data = request.get_json(force=True)

        # Map the limited input fields to the full set of features
        # For this demo, we use a placeholder value (e.g., 0) for the missing fields.
        input_features = {
            'age': data.get('age', 0),
            'bp': data.get('bp', 0),
            'sg': data.get('sg', 0),
            'al': data.get('al', 0),
            'su': data.get('su', 0),
            'rbc': 0, # Placeholder for the missing features
            'pc': 0,
            'pcc': 0,
            'ba': 0,
            'bgr': data.get('bgr', 0),
            'bu': 0,
            'sc': data.get('sc', 0), # Added
            'sod': 0,
            'pot': 0,
            'hemo': data.get('hemo', 0), # Added
            'pcv': 0,
            'wc': 0,
            'rc': 0,
            'htn': 0,
            'dm': 0,
            'cad': 0,
            'appet': 0,
            'pe': 0,
            'ane': 0
        }

        # Create a DataFrame from the input data, ensuring the order matches
        # the model's training features.
        input_data = pd.DataFrame([list(input_features.values())], columns=list(input_features.keys()))

        # Make the prediction and get the probability
        prediction = loaded_model.predict(input_data)
        probability = loaded_model.predict_proba(input_data)[0][1]

        result = 'Kidney Disease (CKD)' if prediction[0] == 1 else 'No Kidney Disease (Not CKD)'
        probability_percent = f'{probability * 100:.2f}%'

        return jsonify({
            'prediction': result,
            'probability': probability_percent
        })
    except KeyError as e:
        return jsonify({'error': f'Missing data field: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
