import React, { useState } from 'react';
import axios from './api';
import TaskForm from './components/TaskForm';

function App() {
  const [prediction, setPrediction] = useState(null);

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto', padding: 20, border: '1px solid #ccc', borderRadius: 8 }}>
      <h2>Effort Prediction</h2>
      <TaskForm onPrediction={setPrediction} />
      {prediction !== null && (
        <div style={{ marginTop: 20 }}>
          Predicted Actual Hours: <b>{prediction}</b>
        </div>
      )}
    </div>
  );
}

export default App; 