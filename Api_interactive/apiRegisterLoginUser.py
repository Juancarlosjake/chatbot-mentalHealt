from flask import Flask, request, jsonify,session
from flask_session import Session #biblioteca para manejar las sesiones
from flask_cors import CORS
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv 

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY']= os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'  
Session(app)

# Configuración de la base de datos MySQL
db_config = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE')
}

# Ruta para verificar el estado de la sesión
@app.route('/status', methods=['GET'])
def check_status():
    print(session.get('logged_in'))
    if session.get('logged_in'):
        return jsonify({'logged_in': True}), 200
    else:
        return jsonify({'logged_in': False}), 200

# Ruta para registrar un nuevo usuario
@app.route('/register', methods=['POST'])
def register_user():
    # Obtener los datos del usuario desde la solicitud JSON
    data = request.get_json()

    # Extraer los campos del formulario
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    age = data.get('age')
    gender = data.get('gender')

    # Validar que todos los campos necesarios estén presentes
    if not all([name, email, password, age, gender]):
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    try:
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Establecer conexión a la base de datos
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Insertar el nuevo usuario en la base de datos
        sql = "INSERT INTO usuarios (nombre, email, password, edad, genero) VALUES (%s, %s, %s, %s, %s)"
        values = (name, email, hashed_password, age, gender)
        cursor.execute(sql, values)
        db.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        db.close()

        # Devolver una respuesta exitosa
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except mysql.connector.Error as error:
        return jsonify({'error': 'Error al registrar usuario'}), 500

# Ruta para realizar el login
@app.route('/login', methods=['POST'])
def login_user():
    # Obtener los datos del usuario desde la solicitud JSON
    data = request.get_json()

    # Extraer el email y la contraseña del formulario
    email = data.get('email')
    password = data.get('password')

    # Validar que el email y la contraseña estén presentes
    if not email or not password:
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400

    try:
        # Establecer conexión a la base de datos
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Consultar la contraseña almacenada en la base de datos por email
        sql = "SELECT password FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()

        if result:
            hashed_password = result[0]
            # Verificar la contraseña utilizando bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                session['usuario'] = email
                return jsonify({'message': 'Inicio de sesión exitoso'}), 200
            else:
                return jsonify({'error': 'Credenciales inválidas'}), 401
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404

    except mysql.connector.Error as error:
        return jsonify({'error': 'Error al iniciar sesión'}), 500
    finally:
        # Cerrar la conexión a la base de datos
        cursor.close()
        db.close()

# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    print(session)
    return jsonify({'message': 'Logout successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)
