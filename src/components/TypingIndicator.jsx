import React, { useRef, useEffect, useState } from 'react';
import botImage from './bot.jpg';

const TypingIndicator = () => {
  const [typingIndicatorHeight, setTypingIndicatorHeight] = useState(0);
  const typingIndicatorRef = useRef(null);

  useEffect(() => {
    if (typingIndicatorRef.current) {
      setTypingIndicatorHeight(typingIndicatorRef.current.offsetHeight);
    }
  }, []);

  return (
    <div className="message bot typing-indicator" style={{ marginTop: -typingIndicatorHeight }}>
      <div className="avatar-container">
        <img src={botImage} alt="bot" className="avatar" />
      </div>
      <div className="typing-indicator-content" ref={typingIndicatorRef}>
        <div className="typing-container">
          <span>Escribiendo respuesta</span>
          <div className="typing-animation">
            <span className="dot">.</span>
            <span className="dot">.</span>
            <span className="dot">.</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;


