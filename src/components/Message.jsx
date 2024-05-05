import './MessageWithImage.css';
// Componente Message.js
import React from 'react';

const Message = ({ sender, text }) => {
  const imageUrl = './bot.png'; // Ruta fija para la imagen
  const imageFloat = sender === 'user' ? 'right' : 'left';

  return (
    <div className={`message ${sender}`}>
      <div className="message-content">
        <div className="message-text">{text}</div>
      </div>
      <img src={imageUrl} alt={sender} className="sender-image" style={{ float: imageFloat }} />
    </div>
  );
};

export default Message;


