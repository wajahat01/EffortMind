# EffortMind

EffortMind is an open-source, full-stack application that predicts the estimated effort (in hours) required to complete a software development task based on its characteristics. The project features a machine learning backend (Flask + scikit-learn) and a modern React frontend, and is designed for easy deployment using Docker and Nginx.

## Project Description

EffortMind helps teams and individuals estimate the time required for various software tasks. By leveraging a dataset of historical tasks and a trained machine learning model, users can input task details (priority, module, and type) and receive an instant prediction of the expected effort in hours.

## Dataset

- **Location:** `backend/data/tasks_dataset.csv`
- **Structure:** The dataset contains 2000+ rows, each representing a software task with the following columns:
  - `task_title`: Short description of the task (not used for prediction)
  - `priority`: Task priority (e.g., High, Medium, Low)
  - `module`: Software module (e.g., Database, UI, API, etc.)
  - `task_type`: Type of task (e.g., Bug, Feature, Chore)
  - `estimated_effort_hours`: Actual effort spent (target variable)
- **Source:** The dataset is included in the repository for full transparency and reproducibility.

## Model Training

The model is trained using a Random Forest Regressor on the categorical features: `priority`, `module`, and `task_type`. The training script is located at `backend/model/train.py` and performs the following steps:

1. Loads the dataset from `backend/data/tasks_dataset.csv`.
2. One-hot encodes the categorical features.
3. Splits the data into training and test sets.
4. Trains a Random Forest regression model.
5. Evaluates the model using Mean Absolute Error (MAE).
6. Saves the trained model and encoder to `backend/model/effort_model.pkl`.

To retrain the model with new data:
```bash
cd backend/model
python train.py
```

## Backend Setup (Flask API)

### Requirements

- Python 3.10+
- See `backend/requirements.txt` for dependencies.

### Running Locally

```bash
cd backend
pip install -r requirements.txt
python app.py
```

- The API will be available at `http://localhost:5000`.
- Main endpoint: `POST /predict` (expects JSON with `priority`, `module`, and `task_type`).

## Frontend Setup (React)

### Requirements

- Node.js 18+

### Running Locally

```bash
cd frontend
npm install
npm start
```

- The app will be available at `http://localhost:3000`.
- The frontend communicates with the backend at `http://localhost:5000/predict`.

## Deployment Instructions

EffortMind is ready for containerized deployment using Docker and Nginx.

### Build and Run with Docker

1. Build the Docker image:
   ```bash
   docker build -t effortmind .
   ```
2. Run the container:
   ```bash
   docker run -p 3000:3000 -p 5000:5000 effortmind
   ```

- The React frontend will be served at `http://localhost:3000`.
- The Flask backend will be available at `http://localhost:5000`.
- Nginx is configured (see `nginx.conf`) to serve the frontend and proxy API requests to the backend.

## 🚀 Deploying to Render.com (Alternate Option)

You can deploy EffortMind to [Render.com](https://render.com/) using the provided Dockerfile. This will serve both the Flask backend and React frontend together using Nginx.

1. **Push your code to GitHub.**
2. **Create a new Web Service on Render:**
   - Go to your Render dashboard and click **New +** → **Web Service**.
   - Connect your GitHub repository.
   - For **Environment**, select **Docker**.
   - For **Build Command**, leave blank (Render uses your Dockerfile).
   - For **Start Command**, leave blank (Render uses the `CMD` in your Dockerfile).
   - Set the **Port** to `80` (Nginx serves on port 80 inside the container).
   - Click **Create Web Service**.
3. **(Optional) Add environment variables** in the Render dashboard if needed.
4. **Wait for build and deploy.**
5. **Access your app** at the provided Render URL (e.g., `https://your-app.onrender.com`).

**Note:**
- For production, use relative API URLs (e.g., `/predict`) in your frontend code. Nginx will proxy these requests to Flask.
- This is an alternate deployment option to running locally or using Docker directly.

## Hackathon Compliance & Open Source

- This project **fully complies with all hackathon rules**.
- All code, data, and configuration files are included and open-source under the terms of the provided LICENSE.
- No proprietary or closed-source components are used.

## Repository Structure

```
EffortMind/
  backend/
    app.py                # Flask API
    requirements.txt      # Backend dependencies
    data/
      tasks_dataset.csv   # Training dataset
    model/
      train.py            # Model training script
      effort_model.pkl    # Trained model (generated)
  frontend/
    src/
      App.js              # Main React app
      api.js              # API helper
      components/
        TaskForm.js       # Task input form
    package.json          # Frontend dependencies
  Dockerfile              # Multi-stage build for frontend, backend, and Nginx
  nginx.conf              # Nginx configuration
  README.md               # Project documentation
``` 