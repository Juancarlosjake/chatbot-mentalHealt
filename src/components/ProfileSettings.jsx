import React, { useState } from 'react';
import axios from 'axios';

const ProfileSettings = ({ user, setUser }) => {
  const [newImage, setNewImage] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setNewImage(file);
  };

  const handleImageUpload = async () => {
    try {
      if (!newImage) {
        console.error('No se ha seleccionado ninguna imagen.');
        return;
      }

      const formData = new FormData();
      formData.append('file', newImage);

      const response = await axios.post('http://127.0.0.1:5001/upload', formData);

      if (response.status === 200) {
        // Actualiza el estado del usuario con la nueva URL de la imagen
        setUser((prevUser) => ({
          ...prevUser,
          photoURL: response.data.image_url,
        }));
        alert('Imagen subida con éxito');
      } else {
        throw new Error('Error al subir la imagen');
      }
    } catch (error) {
      console.error(error);
      alert('Hubo un error al subir la imagen');
    }
  };

  return (
    <div className="profile-settings">
      <div className="user-info">
        <img src={user.photoURL} alt={user.displayName} className="user-image" style={{ width: '200px', height: '200px', borderRadius: '50%' }} />
        <h2>{user.displayName}</h2>
      </div>
      <div className="image-upload">
        <input type="file" accept="image/*" onChange={handleImageChange} />
        <button onClick={handleImageUpload}>Subir imagen</button>
      </div>
    </div>
  );
};

export default ProfileSettings;




