import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Lab1 from "./pages/Lab1";
import Lab2 from "./pages/Lab2";

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/lab1" element={<Lab1 />} />
          <Route path="/lab2" element={<Lab2 />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
