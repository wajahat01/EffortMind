from flask import Flask, request, jsonify
import joblib
import os
from flask_cors import CORS
from scipy.sparse import hstack

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'effort_model.pkl')

# Load model and transformers
try:
    model_bundle = joblib.load(MODEL_PATH)
    model = model_bundle['model']
    cat_encoder = model_bundle['cat_encoder']
    tfidf = model_bundle['tfidf']
    categorical_features = model_bundle['categorical_features']
    text_feature = model_bundle['text_feature']
except Exception as e:
    model = None
    cat_encoder = None
    tfidf = None
    categorical_features = None
    text_feature = None

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not cat_encoder or not tfidf or not categorical_features or not text_feature:
        return jsonify({'error': 'Model or transformers not loaded'}), 500
    data = request.get_json()
    # Validate input
    required_fields = ['task_title', 'task_description', 'priority', 'module', 'task_type', 'resource_level']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    # Prepare categorical features
    cat_input = [[data.get(f) for f in categorical_features]]
    try:
        X_cat = cat_encoder.transform(cat_input)
        # Prepare text feature (task_title)
        X_text = tfidf.transform([data.get(text_feature, '')])
        # Combine features
        X_all = hstack([X_cat, X_text])
        # Predict
        prediction = model.predict(X_all)[0]
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
    return jsonify({'estimated_effort_hours': float(prediction)})

if __name__ == '__main__':
    app.run(debug=True) 