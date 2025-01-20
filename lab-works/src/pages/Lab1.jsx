import React, { useState } from "react";
import ModalForm from "../components/ModalForm";
import { Button, Box, Typography, CircularProgress, Modal, Paper } from "@mui/material";

const Lab1 = () => {
  const [openModal1, setOpenModal1] = useState(false);
  const [openModal2, setOpenModal2] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);

  const handleOpenModal1 = () => {
    setOpenModal1(true);
  };

  const handleCloseModal1 = () => {
    setOpenModal1(false);
  };

  const handleOpenModal2 = () => {
    setOpenModal2(true);
  };

  const handleCloseModal2 = () => {
    setOpenModal2(false);
  };

  const handleSubmit = async (formData) => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/lab_1/maximize_profit/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
  
      if (!response.ok) {
        throw new Error("Ошибка при отправке данных");
      }
  
      const result = await response.json();
      setResult(result);
      handleOpenModal1();
    } catch (error) {
      console.error("Ошибка при обработке данных:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) {
      return;
    }
  
    const formData = new FormData();
    formData.append("file", file);
  
    setLoading(true);
  
    try {
      const response = await fetch("http://localhost:8000/lab_1/get_trends/", {
        method: "POST",
        body: formData,
      });
  
      if (!response.ok) {
        throw new Error("Ошибка при отправке файла");
      }
  
      const data = await response.json();
      console.log("Received image data:", data);
  
      if (typeof data.image_url === "object" && data.image_url.image_url) {
        setImageUrl(data.image_url.image_url);
        handleOpenModal2();
      } else {
        console.error("Received image_url is not a valid object or missing image_url:", data.image_url);
      }
    } catch (error) {
      console.error("Ошибка при загрузке файла:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
      <Typography variant="h4" gutterBottom>
        1 Лабораторная работа
      </Typography>

      <Button
        variant="contained"
        color="primary"
        onClick={handleOpenModal1}
        sx={{ marginBottom: 2 }}
      >
        Задание 1
      </Button>

      <ModalForm open={openModal1} onClose={handleCloseModal1} onSubmit={handleSubmit} />

      <Button
        variant="contained"
        color="secondary"
        component="label"
        sx={{ marginBottom: 2 }}
      >
        Задание 2
        <input
          type="file"
          accept=".csv"
          hidden
          onChange={handleFileChange}
        />
      </Button>

      {loading && <CircularProgress sx={{ marginTop: 2 }} />}

      {/* Модальное окно для задачи 1 */}
      <Modal open={!!result} onClose={handleCloseModal1}>
        <Paper sx={{ padding: 2, margin: "auto", maxWidth: 600 }}>
          <Typography variant="h6" gutterBottom>
            Результат задачи 1:
          </Typography>
          <Typography variant="body1">{result && JSON.stringify(result, null, 2)}</Typography>
          <Button onClick={handleCloseModal1} sx={{ marginTop: 2 }} variant="contained">
            Закрыть
          </Button>
        </Paper>
      </Modal>

      {/* Модальное окно для задачи 2 */}
      <Modal open={openModal2} onClose={handleCloseModal2}>
        <Paper sx={{ padding: 2, margin: "auto", maxWidth: 900 }}>
          <Typography variant="h6" gutterBottom>
            Графики трендов (Задание 2):
          </Typography>
          {imageUrl && <img src={imageUrl} alt="Result" style={{ maxWidth: "100%" }} />}
          <Button onClick={handleCloseModal2} sx={{ marginTop: 2 }} variant="contained">
            Закрыть
          </Button>
        </Paper>
      </Modal>
    </Box>
  );
};

export default Lab1;
