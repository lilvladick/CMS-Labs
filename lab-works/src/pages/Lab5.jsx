import { useState, useEffect, useRef } from 'react';

function App() {
  const [simulationData, setSimulationData] = useState({
    total: 0,
    served: 0,
    lost: 0,
    finished: false,
    p_served: 0,
    p_lost: 0,
    ratio: null
  });
  const [ws, setWs] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  const prevServedRef = useRef(simulationData.served);

  useEffect(() => {
    if (simulationData.served > prevServedRef.current) {
      const audio = new Audio('/ring.wav');
      audio.play().catch(err => console.error("Ошибка воспроизведения аудио:", err));
    }
    prevServedRef.current = simulationData.served;
  }, [simulationData.served]);

  const startSimulation = async () => {
    await fetch('http://localhost:8000/lab_5/telephone_line_simulation/', { method: 'POST' });
 
    const socket = new WebSocket('ws://localhost:8000/ws/telephone_line_simulation');
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setSimulationData(data);
      if (data.finished) {
        setModalVisible(true);
        socket.close();
      }
    };
    setWs(socket);
  };

  const closeModal = () => {
    setModalVisible(false);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Симуляция телефонной линии</h1>
      <button onClick={startSimulation}>Запустить симуляцию</button>
      <div style={{ marginTop: '20px' }}>
        <h2>Счётчики</h2>
        <p>Принято: {simulationData.served}</p>
        <p>Отклонено: {simulationData.lost}</p>
        <p>Всего: {simulationData.total}</p>
      </div>
      
      {modalVisible && (
        <div style={{
          position: 'fixed', top: '20%', left: '20%',
          backgroundColor: '#fff', padding: '20px', border: '1px solid #000'
        }}>
          <h2>Итоговая статистика симуляции</h2>
          <p>Общее число вызовов: {simulationData.total}</p>
          <p>Обслужено: {simulationData.served}</p>
          <p>Отказов: {simulationData.lost}</p>
          <p>Вероятность обслуживания: {simulationData.p_served.toFixed(4)}</p>
          <p>Вероятность отказа: {simulationData.p_lost.toFixed(4)}</p>
          <p>Отношение обслуженных к отказам: {simulationData.ratio !== null ? simulationData.ratio.toFixed(4) : "N/A"}</p>
          <button onClick={closeModal}>Закрыть</button>
        </div>
      )}
    </div>
  );
}

export default App;