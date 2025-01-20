import React, { useState } from "react";
import { Modal, Box, Typography, TextField, Button, Stack } from "@mui/material";

const ModalForm = ({ open, onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    profit: "",
    time_matrix_1: "",
    time_matrix_2: "",
    time_matrix_3: "",
    time_matrix_4: "",
    time_limits: "",
    processes: "",
    products: "",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = () => {
    const formattedData = {
      profit: formData.profit.split(",").map(Number),
      time_matrix: [
        formData.time_matrix_1.split(",").map(Number),
        formData.time_matrix_2.split(",").map(Number),
        formData.time_matrix_3.split(",").map(Number),
        formData.time_matrix_4.split(",").map(Number),
      ],
      time_limits: formData.time_limits.split(",").map(Number),
      processes: formData.processes.split(","),
      products: formData.products.split(","),
    };

    console.log("Данные формы:", formattedData);

    onSubmit(formattedData);
    onClose();
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          bgcolor: "white",
          p: 4,
          borderRadius: 2,
          maxWidth: 600,
          mx: "auto",
          mt: "20vh",
        }}
      >
        <Typography variant="h6" mb={2}>
          Введите данные для задания 1
        </Typography>
        <Stack spacing={2}>
          <TextField
            name="profit"
            label="Прибыль (через запятую)"
            value={formData.profit}
            onChange={handleInputChange}
            fullWidth
            placeholder="10, 14, 12"
          />
          <TextField
            name="time_matrix_1"
            label="Время на операции для Фрезерного станка (через запятую)"
            value={formData.time_matrix_1}
            onChange={handleInputChange}
            fullWidth
            placeholder="2, 4, 5"
          />
          <TextField
            name="time_matrix_2"
            label="Время на операции для Токарного станка (через запятую)"
            value={formData.time_matrix_2}
            onChange={handleInputChange}
            fullWidth
            placeholder="1, 8, 6"
          />
          <TextField
            name="time_matrix_3"
            label="Время на операции для Сварочного станка (через запятую)"
            value={formData.time_matrix_3}
            onChange={handleInputChange}
            fullWidth
            placeholder="7, 4, 5"
          />
          <TextField
            name="time_matrix_4"
            label="Время на операции для Шлифовального станка (через запятую)"
            value={formData.time_matrix_4}
            onChange={handleInputChange}
            fullWidth
            placeholder="4, 6, 7"
          />
          <TextField
            name="time_limits"
            label="Ограничения по времени (через запятую)"
            value={formData.time_limits}
            onChange={handleInputChange}
            fullWidth
            placeholder="120, 280, 240, 360"
          />
          <TextField
            name="processes"
            label="Процессы (через запятую)"
            value={formData.processes}
            onChange={handleInputChange}
            fullWidth
            placeholder="Фрезерное, Токарное, Сварочное, Шлифовальное"
          />
          <TextField
            name="products"
            label="Продукты (через запятую)"
            value={formData.products}
            onChange={handleInputChange}
            fullWidth
            placeholder="x1, x2, x3"
          />
          <Button variant="contained" onClick={handleSubmit}>
            Отправить данные
          </Button>
        </Stack>
      </Box>
    </Modal>
  );
};

export default ModalForm;
