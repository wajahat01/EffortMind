import React, { useState } from 'react';
import axios from '../api';
import { postPrediction } from '../api';

const priorities = ['High', 'Medium', 'Low'];
const modules = ['Frontend', 'Backend', 'DevOps', 'API'];
const taskTypes = ['Bug', 'Feature', 'Improvement', 'Research'];
const resourceLevels = ['SENIOR', 'MID', 'JUNIOR'];

function TaskForm({ onPrediction }) {
  const [taskTitle, setTaskTitle] = useState('');
  const [priority, setPriority] = useState(priorities[0]);
  const [module, setModule] = useState(modules[0]);
  const [taskType, setTaskType] = useState(taskTypes[0]);
  const [taskDescription, setTaskDescription] = useState('');
  const [resourceLevel, setResourceLevel] = useState(resourceLevels[0]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const data = await postPrediction({
        task_title: taskTitle,
        task_description: taskDescription,
        priority,
        module,
        task_type: taskType,
        resource_level: resourceLevel
      });
      onPrediction(data.estimated_effort_hours);
    } catch (err) {
      setError(err.response?.data?.error || 'Error connecting to backend');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div style={{ marginBottom: 10 }}>
        <label>Task Title: </label>
        <input type="text" value={taskTitle} onChange={e => setTaskTitle(e.target.value)} required />
      </div>
      <div style={{ marginBottom: 10 }}>
        <label>Priority: </label>
        <select value={priority} onChange={e => setPriority(e.target.value)}>
          {priorities.map(p => <option key={p} value={p}>{p}</option>)}
        </select>
      </div>
      <div style={{ marginBottom: 10 }}>
        <label>Module: </label>
        <select value={module} onChange={e => setModule(e.target.value)}>
          {modules.map(m => <option key={m} value={m}>{m}</option>)}
        </select>
      </div>
      <div style={{ marginBottom: 10 }}>
        <label>Task Type: </label>
        <select value={taskType} onChange={e => setTaskType(e.target.value)}>
          {taskTypes.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>
      <div style={{ marginBottom: 10 }}>
        <label>Task Description: </label>
        <textarea value={taskDescription} onChange={e => setTaskDescription(e.target.value)} required rows={3} style={{ width: '100%' }} />
      </div>
      <div style={{ marginBottom: 10 }}>
        <label>Resource Level: </label>
        <select value={resourceLevel} onChange={e => setResourceLevel(e.target.value)}>
          {resourceLevels.map(lvl => <option key={lvl} value={lvl}>{lvl}</option>)}
        </select>
      </div>
      <button type="submit" disabled={loading}>{loading ? 'Predicting...' : 'Predict'}</button>
      {error && <div style={{ color: 'red', marginTop: 10 }}>{error}</div>}
    </form>
  );
}

export default TaskForm; 