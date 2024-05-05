from flask import Flask, request, jsonify
from rasa_sdk import Action, Tracker
from typing import Dict, Any, List, Text
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from IA_models.model import SentimentAnalyzer
import os
import random

app = Flask(__name__)

class ActionDetectEmotion(Action):
    def name(self):
        return "action_detect_emotion"

    def __init__(self):
        try:
            file_path = os.path.abspath('IA_models/trainer_model.pkl')
    
            self.loaded_analyzer = SentimentAnalyzer.load_model(file_path)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en la ruta {file_path}")
        except ModuleNotFoundError:
            print("Error: No se pudo encontrar el módulo necesario")
        except Exception as e:
            print(f"Error al cargar el modelo: {str(e)}")

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        try:
            # Obtén el texto del mensaje directamente del diccionario recibido
            user_message = tracker.get('latest_message', {}).get('text', "")

            # Realiza la predicción de emociones
            predicted_emotion = self.loaded_analyzer.predict_sentiment(user_message)

            # Setear la emoción detectada en Rasa
            #tracker.SlotSet("emoción_actual", predicted_emotion)

            print(f"Predicted Emotion: {predicted_emotion}")

            #Respuestas según las clases de emociones devueltas por el modelo LSTM
            if predicted_emotion == "Felicidad":
                response_text = "¡Me alegra saber que te sientes feliz! ¿Hay algo más en lo que pueda ayudarte?"
            
            elif predicted_emotion == "Ansiedad":

                if random.choice([True, False]):
                     # Lista de ejercicios de calma
                    calm_exercises = [
                        {"name": "Respiración Profunda", "description": "Inhala lentamente por la nariz, cuenta hasta cuatro. Luego, exhala por la boca contando hasta seis. Repite varias veces."},
                        {"name": "Visualización Guiada", "description": "Cierra los ojos e imagina un lugar tranquilo. Detalla los sonidos, olores y sensaciones. Respira profundamente mientras visualizas."},
                        {"name": "Ejercicio de Atención Plena", "description": "Focaliza tu atención en el momento presente. Observa tus pensamientos y emociones sin juzgar. Respira conscientemente."},
                    ]

                    # Construye el mensaje con instrucciones de los ejercicios
                    response_text = "Aquí tienes algunos ejercicios para controlar la ansiedad que puedes probar:\n"
                    for exercise in calm_exercises:
                        response_text += f"\n{exercise['name']}: {exercise['description']}"

                else:
                    response_text = 'Aqui tienes algunos recursos que pueden ayudarte a calmar tu ansiedad:\n'
                    response_text += "[Meditación guiada para calmar la ANSIEDAD - 5 minutos Minfulness] URL: https://www.youtube.com/watch?v=vr7oKogGLeM \n"
                    response_text += "[MÚSICA RELAJANTE ANTI ESTRES PARA CALMAR LA MENTE - MÚSICA PARA REDUCIR LA ANSIEDAD] URL: https://www.youtube.com/watch?v=IvA95ur6how \n"

            elif predicted_emotion == "Tristeza":
                sadness_resources = [
                                    {"name": "Recursos de salud mental", "link": "OPS - https://www.paho.org/es/comunidad-practicas-aps-chile/recursos-sobre-salud-mental"},
                                    {"name": "Terapia en línea", "link": "Plataforma de terapia en línea - https://www.terapify.com/"},
                                    {"name": "Aplicaciones de meditación y mindfulness", "link": "Headspace - https://www.headspace.com/es, Calm - https://www.calm.com/es"},
                                    {"name": "Grupos de apoyo en línea", "link": "Grupo de apoyo en línea - https://www.gob.mx/salud/es/articulos/linea-de-la-vida-ayuda-profesional-para-personas-con-depresion?idiom=es"},
                                    {"name": "Actividades creativas", "link": "Pintura emocional,Escritura terapéutica,Música y composición"},
                                    {"name": "Ejercicio físico", "link": "Actividades físicas para mejorar el estado de ánimo: Caminatas al aire libre,Yoga o pilates,Ejercicios cardiovasculare"},
                                    {"name": "Lecturas recomendadas", "link": "Libros sobre manejo de emociones y bienestar mental: 'El poder del ahora' de Eckhart Tolle, 'Inteligencia emocional' de Daniel Goleman"},
                                ]

                                # Construir el mensaje con la lista de recursos
                response_text = "Aquí tienes algunos recursos que podrían ayudarte a gestionar la tristeza:\n"
                for resource in sadness_resources:
                    response_text += f"\n{resource['name']}: {resource['link']}"

            elif predicted_emotion == "Enojo":
                anger_resources = [
                    {"name": "Técnicas de respiración para controlar la ira", "link": "https://www.verywellmind.com/anger-management-breathing-exercises-4177856"},
                    {"name": "Ejercicios de mindfulness para reducir el enojo", "link": "https://www.psychologytoday.com/us/blog/mindfulness-in-frantic-world/201906/3-mindfulness-exercises-help-you-let-go-anger"},
                    {"name": "Comunicación efectiva en situaciones conflictivas", "link": "https://www.helpguide.org/articles/relationships-communication/healthy-communication.htm"},
                    {"name": "Actividades recreativas para aliviar el estrés", "link": "https://www.healthline.com/health/mental-health/creative-activities-for-stress-relief"},
                    {"name": "Música relajante para calmar la mente", "link": "https://www.healthline.com/health/stress-relief/music-for-stress-relief"},
                    {"name": "Descanso y autocuidado", "link": "https://www.mayoclinic.org/healthy-lifestyle/stress-management/in-depth/stress-relief/art-20044456"},
                    {"name": "Líneas de ayuda y servicios de asesoramiento", "link": "https://www.cdc.gov/mentalhealth/tools-resources/index.htm"},
                ]

                # Construir el mensaje con la lista de recursos
                response_text = "Aquí tienes algunos recursos que podrían ayudarte a gestionar el enojo:\n"
                for resource in anger_resources:
                    response_text += f"\n{resource['name']}: {resource['link']}"
            
            elif predicted_emotion == "Calma":
                calm_resources = [
                        {"name": "Técnicas de respiración para mantener la calma", "link": "https://www.verywellmind.com/relaxation-techniques-breath-control-2584189"},
                        {"name": "Meditación guiada para la calma interior", "link": "https://www.mindful.org/audio-resources-for-mindfulness-meditation/"},
                        {"name": "Ejercicios de visualización para reducir la ansiedad", "link": "https://www.verywellmind.com/how-to-use-guided-visualization-for-stress-reduction-3144606"},
                        {"name": "Consejos para mejorar el sueño y reducir el estrés", "link": "https://www.sleepfoundation.org/"},
                        {"name": "Actividades de autocuidado para el bienestar emocional", "link": "https://www.psychologytoday.com/us/blog/click-here-happiness/201812/self-care-12-ways-take-better-care-yourself"},
                        {"name": "Apoyo emocional a través de líneas de ayuda y terapia en línea", "link": "https://www.betterhelp.com/online-therapy/"},
                    ]

                    # Construir el mensaje con la lista de recursos
                response_text = "Aquí tienes algunos recursos que podrían ayudarte a mantener la calma:\n"
                for resource in calm_resources:
                    response_text += f"\n{resource['name']}: {resource['link']}"

            else:
                response_text = "No estoy seguro de cómo interpretar tu emoción. ¿Podrías explicarme cómo te sientes?"
                
               

            print(f"Response Text: {response_text}")

           
            return {
                "responses": [{"text": response_text}]
            }

        except Exception as e:
            error_message = f"Error al ejecutar la acción: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [{'text': error_message}] 
        
class ActionEmocionAnsiedadRepetida(Action):
    def name(self) -> Text:
        return "action_emocion_ansiedad_repetida"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Acción específica para manejar la repetición de la emoción de ansiedad
        response_text = "¡Parece que estás experimentando ansiedad de nuevo!, Te reproduzco un audio de para relajarte\n"
        response_text += "URL: audios/audio.mp3"
        
        # Devolver una lista de diccionarios con las respuestas
        return {
                "responses": [{"text": response_text}]
            }
    
# Definir una ruta de Flask para manejar solicitudes de acción
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    action_name = data.get("next_action")
    tracker = data.get("tracker")
    # Crear un dispatcher
    dispatcher = CollectingDispatcher()

    if action_name == "action_detect_emotion":
        response = ActionDetectEmotion().run(dispatcher, tracker, None)
    
    elif action_name == "action_emocion_ansiedad_repetida":
        response = ActionEmocionAnsiedadRepetida().run(dispatcher, tracker, None)
    
    else:
        response = {"error": "Accion no reconocida"}

    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5055, debug=True)