// AjustesPerfil.jsx
import { useState } from 'react';
import ProfileSettings from '../components/ProfileSettings';
import userImage from '../components/user.jpg';

const AjustesPerfil = () => {
  const [user, setUser] = useState({
    displayName: 'Juan Carlos Romero Perez',
    photoURL: userImage,
  });

  return (
    <div className="app-container">
      <main className="app-main" id="chatbot-container">
      <ProfileSettings user={user} setUser={setUser} />
      </main>
    </div>
  );
};

export default AjustesPerfil;

