import React, { useState,useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Chatbot from './components/Chatbot';
import ChatbotMenu from './components/ChatbotMenu';
import AjustesPerfil from './Pages/AjustesPerfil';
import RegisterForm from './Pages/RegisterForm';
import {Formulario}  from './components/Formulario'; 
import './App.css'; 

function App() {
  // Obtener el estado de autenticación del almacenamiento local al cargar la aplicación
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('user');
    return storedUser ? JSON.parse(storedUser) : null;
  });

  // Almacenar el estado de autenticación en el almacenamiento local cuando cambie
  useEffect(() => {
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    } else {
      localStorage.removeItem('user');
    }
  }, [user]);

  return (
    <div className="app-container">
      <Router>
        {user && <ChatbotMenu setUser={setUser} />}
        <Routes>
          <Route path="/login" element={<Formulario setUser={setUser} />} />
          <Route path="/ajustes-de-perfil" element={<AjustesPerfil />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/registro" element={<RegisterForm />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;

  