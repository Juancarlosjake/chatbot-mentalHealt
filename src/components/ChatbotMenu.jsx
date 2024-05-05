import React, { useState, useEffect } from 'react';
import './ChatMenu.css';
import userImage from './user.jpg';
import { useNavigate } from 'react-router-dom';

const ChatbotMenu = ({ setUser }) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();
  const apiUrl = process.env.REACT_APP_API_URL;

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const handleSettingsClick = () => {
    navigate('/ajustes-de-perfil');
  };

  const handleInicioClick = () => {
    navigate('/chatbot');
  };

  const handleLogout = async () => {
    try {

      const response = await fetch(`${apiUrl}/logout`, {
        method: 'POST',
      });

      if (response.ok) {
        // Cierre de sesión exitoso
        setUser(null); // Establecer el usuario en null para indicar que no está autenticado
        navigate('/login'); // Redirigir a la página de inicio de sesión después del cierre de sesión
        console.log('Logout successful');
      } else {
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Error occurred during logout:', error);
    }
  };

  return (
    <div className="chatbot-menu">
      <header className="app-header" onClick={toggleMenu}>
        <h1 className="app-title" style={{ userSelect: 'none' }}>MindSooth</h1>
        {menuOpen && (
          <Menu
            handleSettingsClick={handleSettingsClick}
            handleInicioClick={handleInicioClick}
            handleLogout={handleLogout}
          />
        )}
      </header>
    </div>
  );
};

const Menu = ({ handleSettingsClick, handleInicioClick, handleLogout }) => {
  return (
    <div className="menu">
      <ul>
        <li>
          <img src={userImage} alt="User" className="user-image" />
          <div onClick={handleSettingsClick}>Ajustes de perfil</div>
        </li>
        <li>
          <div onClick={handleInicioClick}>Inicio</div>
        </li>
        <li>Notificaciones</li>
        <li>Acerca de</li>
        <li>Información legal y términos de uso</li>
        <li>Configuración de preferencias</li>
        <li>Ayuda y soporte</li>
        <li>
          <div onClick={handleLogout}>Cerrar sesión</div>
        </li>
      </ul>
    </div>
  );
};

export default ChatbotMenu;
