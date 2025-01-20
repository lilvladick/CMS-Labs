import React from "react";
import { Box, Button, Typography } from "@mui/material";
import axios from "axios";

const FileUpload = () => {
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    axios
      .post("http://localhost:8000/lab_1/get_trends/", formData)
      .then((response) => {
        console.log("Ответ сервера:", response.data);
      })
      .catch((error) => {
        console.error("Ошибка загрузки файла:", error);
      });
  };

  return (
    <Box mt={3}>
      <Typography variant="h6" mb={2}>
        Загрузите CSV-файл для задания 2:
      </Typography>
      <Button component="label" variant="outlined">
        Загрузить файл
        <input type="file" hidden onChange={handleFileUpload} />
      </Button>
    </Box>
  );
};

export default FileUpload;
