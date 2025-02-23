import React, { useState } from 'react';
import Confetti from 'react-confetti';

function App() {
  const [goldenData, setGoldenData] = useState(null);
  const [newtonData, setNewtonData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [transitioning, setTransitioning] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [error, setError] = useState(null);

  const handleGoldenSelection = async () => {
    setLoading(true);
    setTransitioning(true);
    setGoldenData(null);
    setNewtonData(null);
    const drumRoll = new Audio('/drumroll.wav');
    drumRoll.playbackRate = 1.5;
    drumRoll.play();

    try {
      const response = await fetch('http://localhost:8000/lab_3/golden_selection/');
      if (!response.ok) {
        throw new Error('Ошибка при получении данных золотого сечения');
      }
      const data = await response.json();
      setGoldenData(data);
    } catch (err) {
      setError(err);
    }
    setTimeout(() => {
      setTransitioning(false);
      setLoading(false);
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 5000);
    }, 3000);
  };

  const handleNewton = async () => {
    setLoading(true);
    setTransitioning(true);
    setGoldenData(null);
    setNewtonData(null);
    const drumRoll = new Audio('/drumroll.wav');
    drumRoll.playbackRate = 1.5;
    drumRoll.play();

    try {
      const response = await fetch('http://localhost:8000/lab_3/newton/');
      if (!response.ok) {
        throw new Error('Ошибка при получении данных метода Ньютона');
      }
      const data = await response.json();
      setNewtonData(data);
    } catch (err) {
      setError(err);
    }
    setTimeout(() => {
      setTransitioning(false);
      setLoading(false);
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 5000);
    }, 3000);
  };

  return (
    <>
      {/* Определяем анимацию через встроенные стили */}
      <style>
        {`
          @keyframes fadeInBlack {
            0% { opacity: 1; }
            20% { opacity: 1; } /* Затемнение за 1.2 сек (20% от 6 сек) */
            80% { opacity: 0.8; } /* Держим экран тёмным */
            100% { opacity: 0; } /* Плавное исчезновение */
          }

          .fade-overlay {
            animation: fadeInBlack 6s forwards;
          }
        `}
      </style>
      <div style={{ padding: '20px', position: 'relative' }}>
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

        {/* Затемняющий оверлей */}
        {transitioning && (
          <div
            className="fade-overlay"
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              backgroundColor: 'black',
              zIndex: 1000,
            }}
          />
        )}

        {/* Конфетти */}
        {showConfetti && <Confetti />}
      </div>
    </>
  );
}

export default App;
