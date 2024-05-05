import "./Formulario.css";
import { useState, useEffect } from "react";
import { useNavigate, Link } from 'react-router-dom';

export function Formulario({ setUser }) {
  const [nombre, setNombre] = useState("");
  const [contraseña, setContraseña] = useState("");
  const [error, setError] = useState(false);
  const [sessionChecked, setSessionChecked] = useState(false); // Nuevo estado para controlar si la sesión ya se ha verificado
  const navigate = useNavigate();

  useEffect(() => {
    const verificarSesion = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/status');
        const data = await response.json();

        if (response.ok && data.logged_in) {
          setUser(data); // Establecer el usuario en el estado global o local
          navigate("/chatbot");
        }
      } catch (error) {
        console.error("Error al verificar la sesión:", error);
      } finally {
        setSessionChecked(true); // Marcar la verificación de sesión como completada
      }
    };

    if (!sessionChecked) {
      verificarSesion(); // Llama a la función solo si la sesión no se ha verificado aún
    }
  }, [navigate, sessionChecked, setUser]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (nombre === "" || contraseña === "") {
      setError(true);
      return;
    }

    setError(false);

    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: nombre, password: contraseña }),
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data);
        navigate("/chatbot");
      } else {
        setError(true);
      }
    } catch (error) {
      console.error("Error al iniciar sesión:", error);
      setError(true);
    }
  };

  return (
    <section>
      <h1 style={{ textAlign: "center", color: "#007bff", fontSize: "2.5rem", textTransform: "uppercase", letterSpacing: "2px", fontWeight: "bold" }}>Login</h1>

      <form className="formulario" onSubmit={handleSubmit}>
        <input
          type="text"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          placeholder="Correo electrónico"
        />
        <input
          type="password"
          value={contraseña}
          onChange={(e) => setContraseña(e.target.value)}
          placeholder="Contraseña"
        />
        <button type="submit">Iniciar Sesión</button>
      </form>

      <p style={{ textAlign: "center", marginTop: "1rem" }}>
        ¿No tienes una cuenta? <Link to="/registro">Regístrate aquí</Link>
      </p>

      {error && <p style={{ color: "red", textAlign: "center" }}>Credenciales inválidas. Por favor, inténtalo de nuevo.</p>}
    </section>
  );
}



  