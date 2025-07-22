from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'effort_model.pkl')

# Placeholder: Load model if exists
try:
    model_bundle = joblib.load(MODEL_PATH)
    model = model_bundle['model']
    encoder = model_bundle['encoder']
    feature_names = model_bundle['features']
except Exception as e:
    model = None
    encoder = None
    feature_names = None

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not encoder or not feature_names:
        return jsonify({'error': 'Model or encoder not loaded'}), 500
    data = request.get_json()
    # Validate input
    for field in ['priority', 'module', 'task_type']:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    # Extract features in the correct order
    input_features = [[data.get(f) for f in feature_names]]
    try:
        input_encoded = encoder.transform(input_features)
        prediction = model.predict(input_encoded)[0]
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
    return jsonify({'estimated_effort_hours': prediction})

if __name__ == '__main__':
    app.run(debug=True) 