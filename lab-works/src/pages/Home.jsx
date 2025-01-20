import React from "react";
import { Box, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="100vh"
      sx={{ bgcolor: "#f5f5f5" }}
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
  );
};

export default Home;
