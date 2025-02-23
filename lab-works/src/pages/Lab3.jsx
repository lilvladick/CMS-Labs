import React, { useState } from 'react';

function App() {
  const [goldenData, setGoldenData] = useState(null);
  const [newtonData, setNewtonData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGoldenSelection = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/lab_3/golden_selection/');
      if (!response.ok) {
        throw new Error('Ошибка при получении данных золотого сечения');
      }
      const data = await response.json();
      setGoldenData(data);
      setNewtonData(null);
    } catch (err) {
      setError(err);
    }
    setLoading(false);
  };

  const handleNewton = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/lab_3/newton/');
      if (!response.ok) {
        throw new Error('Ошибка при получении данных метода Ньютона');
      }
      const data = await response.json();
      setNewtonData(data);
      setGoldenData(null);
    } catch (err) {
      setError(err);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Оптимизационные методы</h1>
      <div style={{ marginBottom: '20px' }}>
        <button onClick={handleGoldenSelection} style={{ marginRight: '10px' }}>
          Золотое сечение
        </button>
        <button onClick={handleNewton}>
          Ньютон
        </button>
      </div>

      {loading && <p>Загрузка...</p>}
      {error && <p style={{ color: 'red' }}>Ошибка: {error.message}</p>}

      {goldenData && (
        <div>
          <h2>Результаты метода золотого сечения</h2>
          <p>
            Локальный минимум: x = {goldenData.min.x}, y = {goldenData.min.y}
          </p>
          <p>
            Локальный максимум: x = {goldenData.max.x}, y = {goldenData.max.y}
          </p>
          <p>
            Интервал экстремумов: {goldenData.extrema_interval}
          </p>
          {goldenData.image && (
            <img
              src={`data:image/png;base64,${goldenData.image}`}
              alt="График золотого сечения"
              style={{ maxWidth: '100%', marginTop: '10px' }}
            />
          )}
        </div>
      )}

      {newtonData && (
        <div>
          <h2>Результаты метода Ньютона</h2>
          <ul>
            {newtonData.critical_points.map((point, index) => (
              <li key={index}>
                {point.type}: x = {point.x}, y = {point.y}
              </li>
            ))}
          </ul>
          {newtonData.image_base64 && (
            <img
              src={`data:image/png;base64,${newtonData.image_base64}`}
              alt="График метода Ньютона"
              style={{ maxWidth: '100%', marginTop: '10px' }}
            />
          )}
        </div>
      )}
    </div>
  );
}

export default App;
