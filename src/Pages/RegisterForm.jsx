// Pagina para realizar el formulario de registro de usuario
import React,{useState} from "react";
import "./RegisterForm.css";

const RegisterForm = () =>{
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try{
            const response = await registerUser(name, email, password, age, gender);

            if(response.success) {
                setSuccessMessage('Usuario Registrado exitosamente');
                setErrorMessage('');

                //Resetear los campos despues del registro exitoso
                setName('');
                setEmail('');
                setPassword('');
                setAge('');
                setGender('');
            } else{
                setErrorMessage('ocurrio un error durante el registro');
                setSuccessMessage('');
            }
        } catch(error){
            setErrorMessage('ocurrio un error durante el registro: ' + error);
            setSuccessMessage('');
        }
    };

    const registerUser = async (name, email, password, age, gender) =>{
        try{
            const response = await fetch('http://127.0.0.1:5000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({name, email, password, age, gender})
            });
            if (response.ok){
                const data  = await response.son();
                return {success: true, user: data.user};
            } else{
                const error = await response.json();
                return {success: false, user: error.message};
            }
        } catch(error){
            return{ succes:false, error: error.message};
        }
    };
    
    return(
        <div className="register-form-container">
            <h2>Registro de usuario</h2>
            <form onSubmit={handleSubmit}>
                <div className="inputName">
                    <label htmlFor="name">Nombre:</label>
                    <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    />
                </div>
                <div className="inputMail">
                    <label htmlFor="email">Correo Electrónico:</label>
                    <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div className="inputPassword">
                    <label htmlFor="password">Contraseña:</label>
                    <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <div className="inputEdad">
                    <label htmlFor="age">Edad:</label>
                    <input
                    type="number"
                    id="age"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    />
                </div>
                <div className="inputGender">
                    <label htmlFor="gender">Género:</label>
                    <select
                    id="gender"
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    >
                        <option value="">Selecciona un Género</option>
                        <option value="male">Masculino</option>
                        <option value="female">Femenino</option>
                        <option value="other">Otro</option>
                    </select>
                </div>
                <div className="submit-button">
                    <button type="submit">Registrar</button>
                </div>
            </form>
            {successMessage && <div className="succes">{successMessage}</div>}
            {errorMessage && <div className="error">{errorMessage}</div>}
        </div>
    );
};

export default RegisterForm;