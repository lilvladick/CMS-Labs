import { useState, useEffect, useRef } from "react";

function App() {
  // Общие данные симуляции (используются для обоих сценариев)
  const [simulationData, setSimulationData] = useState({
    total: 0,
    served: 0,
    lost: 0,
    // Для телефонной линии:
    p_served: 0,
    p_lost: 0,
    ratio: null,
    // Для СТО:
    avg_wait_time: 0,
    avg_service_time: 0,
    finished: false,
  });
  const [ws, setWs] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  // 0 – Телефонная линия, 1 – СТО
  const [page, setPage] = useState(0);
  // Флаг для СТО: ограничивать ли очередь (true = лимит, false = без лимита)
  const [queryLimit, setQueryLimit] = useState(false);

  // Эффект для проигрывания звука при увеличении количества обслуженных звонков (для телефонной линии)
  const prevServedRef = useRef(simulationData.served);
  useEffect(() => {
    if (page === 0 && simulationData.served > prevServedRef.current) {
      const audio = new Audio("/ring.wav");
      audio.play().catch((err) =>
        console.error("Ошибка воспроизведения аудио:", err)
      );
    }
    prevServedRef.current = simulationData.served;
  }, [simulationData.served, page]);

  // Запуск симуляции для телефонной линии
  const startTelephoneSimulation = async () => {
    await fetch("http://localhost:8000/lab_5/telephone_line_simulation/", {
      method: "POST",
    });
    const socket = new WebSocket("ws://localhost:8000/ws/telephone_line_simulation");
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

  // Запуск симуляции для СТО. Отправляем POST с флагом query_limit.
  const startServiceStationSimulation = async () => {
    await fetch("http://localhost:8000/lab_5/service_station_simulation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query_limit: queryLimit ? "true" : "false" }),
    });
    const socket = new WebSocket("ws://localhost:8000/ws/service_station_simulation");
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
    <div style={{ padding: "20px", textAlign: "center" }}>
      {/* Переключатель страниц */}
      <div
        style={{
          width: "250px",
          height: "50px",
          backgroundColor: "#ddd",
          borderRadius: "25px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "5px",
          margin: "0 auto 20px auto",
          position: "relative",
          cursor: "pointer",
          transition: "all 0.3s ease",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
        }}
        onClick={() => setPage(page === 0 ? 1 : 0)}
      >
        {/* Подсветка выбранного элемента */}
        <div
          style={{
            position: "absolute",
            width: "50%",
            height: "100%",
            backgroundColor: "rgba(173, 216, 230, 0.7)",
            borderRadius: "25px",
            transition: "transform 0.3s ease",
            transform: page === 0 ? "translateX(0%)" : "translateX(100%)",
          }}
        ></div>
        <div
          style={{
            width: "50%",
            textAlign: "center",
            fontSize: "18px",
            fontWeight: "bold",
            zIndex: 2,
            color: page === 0 ? "#000" : "#555",
          }}
        >
          📞 Линия
        </div>
        <div
          style={{
            width: "50%",
            textAlign: "center",
            fontSize: "18px",
            fontWeight: "bold",
            zIndex: 2,
            color: page === 1 ? "#000" : "#555",
          }}
        >
          🔧 СТО
        </div>
      </div>

      {page === 0 ? (
        // Страница симуляции телефонной линии
        <>
          <h1>Симуляция телефонной линии</h1>
          <button onClick={startTelephoneSimulation}>Запустить симуляцию</button>
          <div style={{ marginTop: "20px" }}>
            <h2>Счётчики</h2>
            <p>Принято: {simulationData.served}</p>
            <p>Отклонено: {simulationData.lost}</p>
            <p>Всего: {simulationData.total}</p>
          </div>
          {modalVisible && (
            <div
              style={{
                position: "fixed",
                top: "20%",
                left: "50%",
                transform: "translate(-50%, 0)",
                backgroundColor: "#fff",
                padding: "20px",
                border: "1px solid #000",
                boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
              }}
            >
              <h2>Итоговая статистика симуляции телефонной линии</h2>
              <p>Общее число вызовов: {simulationData.total}</p>
              <p>Обслужено: {simulationData.served}</p>
              <p>Отказов: {simulationData.lost}</p>
              <p>Вероятность обслуживания: {simulationData.p_served?.toFixed(4) || 0}</p>
              <p>Вероятность отказа: {simulationData.p_lost?.toFixed(4) || 0}</p>
              <p>
                Отношение обслуженных к отказам:{" "}
                {simulationData.ratio !== null ? simulationData.ratio.toFixed(4) : "N/A"}
              </p>
              <button onClick={closeModal}>Закрыть</button>
            </div>
          )}
          <div>
            <img
              src="https://media1.tenor.com/m/GBf9_tZFfakAAAAC/phone-telephone.gif"
              alt="phone"
            />
          </div>
        </>
      ) : (
        // Страница симуляции СТО
        <>
          <h1>Симуляция СТО</h1>
          <div style={{ marginBottom: "20px" }}>
            <label style={{ fontSize: "16px", marginRight: "10px" }}>
              Ограничить очередь?
            </label>
            <input
              type="checkbox"
              checked={queryLimit}
              onChange={(e) => setQueryLimit(e.target.checked)}
            />
          </div>
          <button onClick={startServiceStationSimulation}>Запустить симуляцию СТО</button>
          <div style={{ marginTop: "20px" }}>
            <h2>Статистика</h2>
            <p>Поступило машин: {simulationData.total}</p>
            <p>Обслужено машин: {simulationData.served}</p>
            <p>Отказов: {simulationData.lost}</p>
            <p>Среднее время ожидания: {simulationData.avg_wait_time}</p>
            <p>Среднее время обслуживания: {simulationData.avg_service_time}</p>
          </div>
          {modalVisible && (
            <div
              style={{
                position: "fixed",
                top: "20%",
                left: "50%",
                transform: "translate(-50%, 0)",
                backgroundColor: "#fff",
                padding: "20px",
                border: "1px solid #000",
                boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
              }}
            >
              <h2>Итоговая статистика симуляции СТО</h2>
              <p>Общее число поступивших машин: {simulationData.total}</p>
              <p>Число обслуженных машин: {simulationData.served}</p>
              <p>Число отказов: {simulationData.lost}</p>
              <p>Среднее время ожидания: {simulationData.avg_wait_time}</p>
              <p>Среднее время обслуживания: {simulationData.avg_service_time}</p>
              <button onClick={closeModal}>Закрыть</button>
            </div>
          )}
          <div>
            <img
              src="https://media.tenor.com/images/2d2e9c1f9a351bb68b9ecfda1f8810a0/tenor.gif"
              alt="service station"
            />
          </div>
        </>
      )}
    </div>
  );
}

export default App;
