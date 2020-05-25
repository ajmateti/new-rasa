# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionDiagnose(Action):
    def name(self) -> Text:
        return "action_diagnose"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptoms = []
        dispatcher.utter_message(template="utter_ask_first_symptom")
        symptom = tracker.get_slot("symptom")
        symptoms.append(symptom)
        i = 0
        while i<5:
            dispatcher.utter_message(template="utter_ask_symptoms")
            symptom = tracker.get_slot("symptom")
            symptoms.append(symptom)
            i+=1
        disease = self.get_disease(symptoms)
        text = "You may have {}".format(disease)
        dispatcher.utter_message(text=text)
    def get_disease(self,symptoms):
        print(symptoms)
        return "Covid19"