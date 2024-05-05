import React, { useState, useEffect, useRef } from 'react';
import { sendMessageToRasa } from './rasaApi'; 
import './Chatbot.css'; // Importar estilos CSS
import TypingIndicator from './TypingIndicator';
import botImage from './bot.jpg'; // Ruta de la imagen del bot
import userImage from './user.jpg'; // Ruta de la imagen del usuario

const Chatbot = () => {
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null); // Referencia al campo de entrada
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  useEffect(() => {
    messagesEndRef.current.scrollTop = messagesEndRef.current.scrollHeight;
  }, [messages]);  

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); 
    try {
      await sendMessageToRasa(inputText, setMessages, setIsTyping, setInputText);
    } catch (error) {
      setError(error.message); 
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Ajustar la altura del campo de entrada según el contenido
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = inputRef.current.scrollHeight + 'px';
    }
  }, [inputText]);

  
  return (
    <div className="chatbot-container">
      <div className="chatbot-messages" ref={messagesEndRef}>
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            <div className="avatar-container">
              <img src={message.sender === 'bot' ? botImage : userImage} alt={message.sender} className="avatar" />
            </div>
            <div className={`message-text ${message.sender}`}>
              {message.text}
            </div>
          </div>
        ))}
        {isTyping && <TypingIndicator />}
      </div>
      
      <form onSubmit={handleSubmit} className="form-wrapper">
        <div className="input-button-container">
          {/* Utiliza un elemento textarea para el campo de entrada */}
          <textarea
            ref={inputRef}
            value={inputText}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Escribe un mensaje..."
            className="input-field"
          ></textarea>
          <button type="submit" className="send-button">Enviar</button>
        </div>
      </form>
    </div>
  );
};

export default Chatbot;




