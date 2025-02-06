import React, { useState, useEffect, useRef } from "react";
import { Box, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const randomValue = (min, max) => Math.random() * (max - min) + min;

const getRandomPosition = () => ({
  top: Math.floor(randomValue(0, 90)) + "%",
  left: Math.floor(randomValue(0, 90)) + "%" 
});

const createRandomKeyframes = () => {
  const animationName = `runAround-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
  const p0 = `0% { transform: translate(0, 0) rotate(0deg); }`;
  const p20 = `20% { transform: translate(${randomValue(-300, 300)}px, ${randomValue(-300, 300)}px) rotate(${randomValue(0, 360)}deg); }`;
  const p40 = `40% { transform: translate(${randomValue(-300, 300)}px, ${randomValue(-300, 300)}px) rotate(${randomValue(0, 360)}deg); }`;
  const p60 = `60% { transform: translate(${randomValue(-300, 300)}px, ${randomValue(-300, 300)}px) rotate(${randomValue(0, 360)}deg); }`;
  const p80 = `80% { transform: translate(${randomValue(-300, 300)}px, ${randomValue(-300, 300)}px) rotate(${randomValue(0, 360)}deg); }`;
  const p100 = `100% { transform: translate(0, 0) rotate(360deg); }`;

  const keyframes = `
    @keyframes ${animationName} {
      ${p0}
      ${p20}
      ${p40}
      ${p60}
      ${p80}
      ${p100}
    }
  `;
  return { animationName, keyframes };
};

const Home = () => {
  const navigate = useNavigate();
  const [gifs, setGifs] = useState([]);
  const [isSpawning, setIsSpawning] = useState(false);
  const spawnIntervalRef = useRef(null);

  const spawnGif = () => {
    const id = Date.now() + Math.random();
    const randomPosition = getRandomPosition();

    const { animationName, keyframes } = createRandomKeyframes();
    const styleElement = document.createElement("style");
    styleElement.innerHTML = keyframes;
    document.head.appendChild(styleElement);

    const newGif = {
      id,
      src: "https://media.tenor.com/VRmdB5VAoWkAAAAi/bouncing-kirby-kirby.gif",
      style: {
        position: "absolute",
        ...randomPosition,
        width: "150px",
        height: "100px",
        pointerEvents: "none",
        animation: `${animationName} 3s linear`
      },
      styleElement,
    };

    setGifs((prev) => [...prev, newGif]);

    setTimeout(() => {
      setGifs((prev) => prev.filter((gif) => gif.id !== id));
      if (newGif.styleElement && newGif.styleElement.parentNode) {
        newGif.styleElement.parentNode.removeChild(newGif.styleElement);
      }
    }, 3000);
  };

  useEffect(() => {
    if (isSpawning) {
      spawnIntervalRef.current = setInterval(() => {
        for (let i = 0; i < 5; i++) {
          spawnGif();
        }
      }, 500);
    } else {
      if (spawnIntervalRef.current) {
        clearInterval(spawnIntervalRef.current);
        spawnIntervalRef.current = null;
      }
    }

    return () => {
      if (spawnIntervalRef.current) {
        clearInterval(spawnIntervalRef.current);
      }
    };
  }, [isSpawning]);

  const toggleSpawning = () => {
    setIsSpawning((prev) => !prev);
  };

  return (
    <Box position="relative" minHeight="100vh" sx={{ bgcolor: "#f5f5f5" }}>
      {/* Кнопка для переключения режима спауна GIF в верхней части экрана */}
      <Box
        position="absolute"
        top={10}
        left="50%"
        sx={{ transform: "translateX(-50%)", zIndex: 10 }}
      >
        <Button variant="outlined" onClick={toggleSpawning}>
          {isSpawning ? "Стоп прикольчик" : "Прикольчик"}
        </Button>
      </Box>

      {/* Основной контент страницы */}
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        minHeight="100vh"
      >
        <Typography variant="h3" mb={5} textAlign="center">
          Лабораторные работы по предмету "Компьютерные системы моделирования"
        </Typography>
        <Box display="flex" gap={2}>
          {[1, 2, 3, 4, 5, 6].map((lab) => (
            <Button
              key={lab}
              variant="contained"
              onClick={() => navigate(`/lab${lab}`)}
              sx={{ fontSize: "18px", padding: "10px 20px" }}
            >
              Лабораторная {lab}
            </Button>
          ))}
        </Box>
      </Box>

      {/* Рендерим спауненные GIF поверх страницы */}
      {gifs.map((gif) => (
        <img key={gif.id} src={gif.src} alt="gif" style={gif.style} />
      ))}
    </Box>
  );
};

export default Home;
