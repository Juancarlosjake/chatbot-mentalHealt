from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionEjerciciosAnsiedad(Action):
    def name(self) -> Text:
        return "action_perform_calm_exercises"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Aquí tienes algunos ejercicios que pueden ayudarte a manejar la ansiedad: [Ejercicio 1], [Ejercicio 2], [Ejercicio 3]")
        return []
