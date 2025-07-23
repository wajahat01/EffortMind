import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import joblib
import os


def main():
    # Load dataset
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tasks_dataset.csv')
    df = pd.read_csv(data_path)

    # Features
    categorical_features = ['priority', 'module', 'task_type']
    text_feature = 'task_title'
    y = df['estimated_effort_hours']

    # One-hot encode categorical features
    cat_encoder = OneHotEncoder(sparse=True, handle_unknown='ignore')
    X_cat = cat_encoder.fit_transform(df[categorical_features])

    # TF-IDF vectorize text feature
    tfidf = TfidfVectorizer()
    X_text = tfidf.fit_transform(df[text_feature].fillna(''))

    # Combine all features
    from scipy.sparse import hstack
    X_all = hstack([X_cat, X_text])

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error (MAE): {mae:.2f}")

    # Save model, encoders, and feature info
    model_path = os.path.join(os.path.dirname(__file__), 'effort_model.pkl')
    joblib.dump({
        'model': model,
        'cat_encoder': cat_encoder,
        'tfidf': tfidf,
        'categorical_features': categorical_features,
        'text_feature': text_feature
    }, model_path)
    print(f"Model and encoders saved to {model_path}")


if __name__ == '__main__':
    main() 