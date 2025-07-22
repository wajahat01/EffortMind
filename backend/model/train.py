import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
import joblib
import os


def main():
    # Load dataset
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tasks_dataset.csv')
    df = pd.read_csv(data_path)

    # Use only categorical features for prediction
    categorical_features = ['priority', 'module', 'task_type']
    X = df[categorical_features]
    y = df['estimated_effort_hours']

    # One-hot encode categorical features
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error (MAE): {mae:.2f}")

    # Save model and encoder
    model_path = os.path.join(os.path.dirname(__file__), 'effort_model.pkl')
    joblib.dump({'model': model, 'encoder': encoder, 'features': categorical_features}, model_path)
    print(f"Model and encoder saved to {model_path}")


if __name__ == '__main__':
    main() 