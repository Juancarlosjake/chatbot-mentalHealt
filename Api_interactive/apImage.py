from flask import Flask, request, jsonify, url_for,send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'  # Reemplaza con la URL de tu frontend
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó ningún archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Construye la URL completa para acceder a la imagen
        image_url = url_for('uploaded_file', filename=filename, _external=True)
        
        return jsonify({'message': 'Archivo subido exitosamente', 'image_url': image_url}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Ruta para acceder a los archivos subidos
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'ProfileUsersImage'
    app.run(port=5001, debug=True)

