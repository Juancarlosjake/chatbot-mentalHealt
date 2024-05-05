import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

class SentimentAnalyzer:
    """
    Clase para analizar sentimientos utilizando un modelo de red neuronal LSTM.
    """

    def __init__(self, csv_file_path, max_len=300, embedding_dim=100):
        """
        Inicializa la instancia de la clase.

        Args:
            csv_file_path (str): Ruta del archivo CSV que contiene datos de entrenamiento.
            max_len (int): Longitud máxima de las secuencias de texto.
            embedding_dim (int): Dimensión del espacio de embedding para las palabras.
        """
        self.df = pd.read_csv(csv_file_path)
        self.max_len = max_len
        self.embedding_dim = embedding_dim
        self.tokenizer = Tokenizer(num_words=5000)
        self.model = self._build_lstm_model()
        self.label_encoder = None
        self.is_model_trained = False
        self._prepare_data()
    
    def __new__(cls, *args, **kwargs):
        instance = super(SentimentAnalyzer, cls).__new__(cls)
        return instance

    def _build_lstm_model(self):
        """
        Construye y compila un modelo LSTM utilizando Keras.

        Returns:
            obj: Modelo Keras construido.
        """
        model = Sequential(name='sentiment_sequential')  # Agrega un nombre único
        model.add(Embedding(self.tokenizer.num_words, self.embedding_dim, input_length=self.max_len))
        model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2, return_sequences=True))
        model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
        model.add(Dense(32, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(5, activation="softmax"))
        model.compile(loss="sparse_categorical_crossentropy", optimizer="Adam", metrics=["accuracy"])
        return model

    def _prepare_data(self):
        """
        Prepara los datos de entrenamiento y prueba.

        - Tokeniza las frases.
        - Convierte las secuencias de palabras en secuencias de enteros y rellena para igualar la longitud.
        - Codifica las etiquetas emocionales usando LabelEncoder.
        - Divide los datos en conjuntos de entrenamiento y prueba.
        """
        self.tokenizer.fit_on_texts(self.df["Frase"])
        sequences = pad_sequences(self.tokenizer.texts_to_sequences(self.df["Frase"]), maxlen=self.max_len)
        
        self.label_encoder = LabelEncoder()
        encoded_labels = self.label_encoder.fit_transform(self.df["Emocion"].values.reshape(-1, 1))
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(sequences, encoded_labels, test_size=0.2, random_state=25)

    def train_model(self):
        """
        Entrena el modelo utilizando los datos de entrenamiento y EarlyStopping para prevenir el sobreajuste.
        """
        if not self.is_model_trained:
            early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
            self.model.fit(self.X_train, self.y_train, epochs=20, batch_size=63, validation_split=0.1, callbacks=[early_stopping])
            self.is_model_trained = True  # Marcar el modelo como entrenado al final del entrenamiento

    def evaluate_model(self):
        """
        Evalúa el modelo en el conjunto de prueba y devuelve la precisión y el informe de clasificación.
        También muestra la matriz de confusión.
        
        Returns:
            float: Precisión del modelo.
            str: Informe de clasificación.
        """
        y_pred = self.model.predict(self.X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        accuracy = accuracy_score(self.y_test, y_pred_classes)
        report = classification_report(self.y_test, y_pred_classes)
        
        # Agrega la matriz de confusión
        cm = confusion_matrix(self.y_test, y_pred_classes)
        self.plot_confusion_matrix(cm, classes=self.label_encoder.classes_)

        return accuracy, report

    def predict_sentiment(self, text):
        """
        Predice la emoción asociada con un texto dado.

        Args:
            text (str): Texto para realizar la predicción.

        Returns:
            str: Etiqueta emocional predicha.
        """
        text_sequence = pad_sequences(self.tokenizer.texts_to_sequences([text]), maxlen=self.max_len)
        prediction = self.model.predict(text_sequence)
        predicted_label_index = np.argmax(prediction, axis=1)[0]
        predicted_label = self.label_encoder.classes_[predicted_label_index]
        return predicted_label
    
    def plot_confusion_matrix(self, cm, classes):
        """
        Muestra la matriz de confusión utilizando Seaborn y Matplotlib.

        Args:
            cm (numpy.ndarray): Matriz de confusión.
            classes (list): Lista de clases (etiquetas emocionales).
        """
        plt.figure(figsize=(8, 8))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=classes, yticklabels=classes)
        plt.title('Matriz de Confusión')
        plt.xlabel('Predicho')
        plt.ylabel('Real')
        plt.show()

    def save_model(self, filepath):
        """
        Guarda el modelo en la ruta especificada utilizando Pickle.

        Args:
            filepath (str): Ruta completa donde se guardará el modelo.
        """
        self.model = None  # Eliminar el modelo antes de guardar la instancia
        with open(filepath, 'wb') as model_file:
            pickle.dump(self, model_file)

    @classmethod
    def load_model(cls, filepath):
        with open(filepath, 'rb') as model_file:
            loaded_data = pickle.load(model_file)
        loaded_instance = cls.__new__(cls)
        loaded_instance.__dict__.update(loaded_data.__dict__)
        loaded_instance.model = loaded_instance._build_lstm_model()  # Construir un nuevo modelo al cargar
        return loaded_instance
  
    def train_and_save_model(self, save_filepath):
        """
        Entrena el modelo y guarda la instancia completa en un archivo especificado.

        Args:
            save_filepath (str): Ruta completa donde se guardará el modelo entrenado.
        """
        if not self.is_model_trained:
            early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
            self.model.fit(self.X_train, self.y_train, epochs=20, batch_size=63, validation_split=0.1, callbacks=[early_stopping])
            self.is_model_trained = True  # Marcar el modelo como entrenado al final del entrenamiento

            # Guardar la instancia completa (incluyendo el modelo) en un archivo
            with open(save_filepath, 'wb') as model_file:
                pickle.dump(self, model_file)

    @classmethod
    def load_and_predict(cls, filepath, csv_file_path, text):
        loaded_analyzer = cls.load_model(filepath)
        predicted_label = loaded_analyzer.predict_sentiment(text)
        return predicted_label
    
"""
# Entrenamiento del modelo
sentiment_analyzer = SentimentAnalyzer('IA_models/data/analisis_sentimental.csv') # indicar la ruta de los archivos para entrenar al modelo
sentiment_analyzer.train_model()

# Evaluar el modelo
accuracy, report = sentiment_analyzer.evaluate_model()
print(f'Precisión del modelo: {accuracy}')
print('Informe de clasificación:\n', report)

#guardar el modelo en formato Pkl, indicar la ruta
sentiment_analyzer.save_model('IA_models/sentiment_analyzer.pkl')"""

# Agregar esta condición para evitar la ejecución en scripts donde se cargará el modelo
if __name__ == "__main__":
    analyzer = SentimentAnalyzer(csv_file_path='IA_models/data/analisis_sentimental.csv')  # Reemplaza con la ruta de tu archivo CSV
    analyzer.train_and_save_model('IA_models/trainer_model.pkl')