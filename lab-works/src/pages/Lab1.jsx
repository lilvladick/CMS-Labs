import React, { useState } from "react";
import ModalForm from "../components/ModalForm";
import { Button, Box, Typography, CircularProgress } from "@mui/material";

const Lab1 = () => {
  const [openModal, setOpenModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState(null);

  const handleOpenModal = () => {
    setOpenModal(true);
  };

  const handleCloseModal = () => {
    setOpenModal(false);
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
      window.alert(`Результат: ${JSON.stringify(result)}`);
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
      setImageUrl(data.image_url);
    } catch (error) {
      console.error("Ошибка при загрузке файла:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        1 Лабораторная работа
      </Typography>

      <Button
        variant="contained"
        color="primary"
        onClick={handleOpenModal}
        sx={{ marginBottom: 2 }}
      >
        Задание 1
      </Button>

      <ModalForm open={openModal} onClose={handleCloseModal} onSubmit={handleSubmit} />

      <Button
        variant="contained"
        color="secondary"
        component="label"
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

      {imageUrl && <img src={imageUrl} alt="Result" style={{ marginTop: 20, maxWidth: "100%" }} />}
    </Box>
  );
};

export default Lab1;