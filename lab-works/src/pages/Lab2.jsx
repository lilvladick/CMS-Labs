import React, { useState } from 'react';
import { motion } from 'framer-motion';

const liquids = {
  gasoline: { name: 'Бензин', rho: 680, mu: 0.0006, color: '#F4D03F' },
  glycerin: { name: 'Глицерин', rho: 1260, mu: 1.5, color: '#AED6F1' },
  water: { name: 'Вода', rho: 1000, mu: 0.001, color: '#85C1E9' },
};

const materials = {
  steel: { name: 'Сталь', rho: 7850, color: '#7F8C8D' },
  aluminum: { name: 'Алюминий', rho: 2700, color: '#BDC3C7' },
};

const Lab2 = () => {
  const [radius, setRadius] = useState(0.15);
  const [selectedLiquid, setSelectedLiquid] = useState('gasoline');
  const [selectedMaterial, setSelectedMaterial] = useState('steel');
  const [imageUrl, setImageUrl] = useState('');
  const [isCalculating, setIsCalculating] = useState(false);
  const [startAnimation, setStartAnimation] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);

  const handleOpenModal2 = () => {
    setModalOpen(true);
  };

  const handleCloseModal2 = () => {
    setModalOpen(false);
  };

  const handleCalculate = async () => {
    setIsCalculating(true);
    setStartAnimation(true);

    try {
      const liquid = liquids[selectedLiquid];
      const material = materials[selectedMaterial];

      const response = await fetch('http://localhost:8000/lab_2/drown_balls/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          r: radius,
          g: 9.81,
          rho_ball: material.rho,
          rho_liquid: liquid.rho,
          mu: liquid.mu,
          h: 1.5
        })
      });

      const data = await response.json();
      console.log("Received image data:", data);

      setTimeout(() => { 
        if (typeof data.image_url === "object" && data.image_url.image_url) {
            setImageUrl(data.image_url.image_url);
            handleOpenModal2();
          } else {
            console.error("Received image_url is not a valid object or missing image_url:", data.image_url);
          }
    }, 2000);

    } catch (error) {
      console.error('Ошибка при получении изображения:', error);
    } finally {
      setIsCalculating(false);
    }
  };

  const containerWidth = 200;
  const containerHeight = 300;
  const ballSize = radius * containerWidth;
  const finalBallTop = containerHeight - ballSize - 10;

  return (
    <div style={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center', backgroundColor: '#e0f2fe' }}>
      {/* Панель управления */}
      <div
        style={{
          position: 'absolute',
          top: '10px',
          left: '10px',
          width: '300px',
          padding: '20px',
          backgroundColor: 'white',
          borderRadius: '10px',
          boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)'
        }}
      >
        <h2 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '10px' }}>Настройки погружения</h2>

        {/* Ползунок для выбора радиуса шарика */}
        <div style={{ marginBottom: '15px' }}>
          <label>
            Размер шарика (r): {radius.toFixed(2)}
            <input
              type="range"
              min="0.05"
              max="0.5"
              step="0.01"
              value={radius}
              onChange={(e) => setRadius(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            />
          </label>
        </div>

        {/* Выбор жидкости */}
        <div style={{ marginBottom: '15px' }}>
          <label>
            Выберите жидкость:
            <select
              value={selectedLiquid}
              onChange={(e) => setSelectedLiquid(e.target.value)}
              style={{ display: 'block', width: '100%', marginTop: '5px', padding: '5px' }}
            >
              {Object.entries(liquids).map(([key, liquid]) => (
                <option key={key} value={key}>
                  {liquid.name}
                </option>
              ))}
            </select>
          </label>
        </div>

        {/* Выбор материала шарика */}
        <div style={{ marginBottom: '15px' }}>
          <label>
            Выберите материал шарика:
            <select
              value={selectedMaterial}
              onChange={(e) => setSelectedMaterial(e.target.value)}
              style={{ display: 'block', width: '100%', marginTop: '5px', padding: '5px' }}
            >
              {Object.entries(materials).map(([key, material]) => (
                <option key={key} value={key}>
                  {material.name}
                </option>
              ))}
            </select>
          </label>
        </div>

        <button
          onClick={handleCalculate}
          disabled={isCalculating}
          style={{
            marginTop: '10px',
            padding: '10px',
            width: '100%',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          {isCalculating ? 'Рассчитываю...' : 'Посчитать'}
        </button>
      </div>

      {/* Контейнер с жидкостью (цвет зависит от выбранной жидкости) */}
      <div
        style={{
          position: 'relative',
          width: `${containerWidth}px`,
          height: `${containerHeight}px`,
          backgroundColor: liquids[selectedLiquid].color,
          borderRadius: '10px',
          overflow: 'hidden'
        }}
      >
        {/* Анимированный шарик (цвет зависит от материала) */}
        <motion.div
          initial={{ top: 0 }}
          animate={startAnimation ? { top: finalBallTop } : { top: 0 }}
          transition={{ duration: 2, ease: 'easeInOut' }}
          style={{
            position: 'absolute',
            left: '50%',
            transform: 'translateX(-50%)',
            width: `${ballSize}px`,
            height: `${ballSize}px`,
            backgroundColor: materials[selectedMaterial].color,
            borderRadius: '50%',
            boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)'
          }}
        />
      </div>

      {/* Модальное окно для отображения результата */}
      {modalOpen && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}
        >
          <div
            style={{
              backgroundColor: 'white',
              padding: '20px',
              borderRadius: '10px',
              position: 'relative'
            }}
          >
            <button
              onClick={handleCloseModal2}
              style={{
                position: 'absolute',
                top: '10px',
                right: '10px',
                cursor: 'pointer',
                border: 'none',
                background: 'none',
                fontSize: '18px'
              }}
            >
              X
            </button>
            <img
              src={imageUrl}
              alt="Результат погружения"
              style={{ maxWidth: '500px', maxHeight: '80vh', borderRadius: '5px' }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Lab2;
