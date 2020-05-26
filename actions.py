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

# class ActionDiagnose(Action):
#     def name(self) -> Text:
#         return "action_diagnose"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         self.dispatcher = dispatcher
#         self.tracker = tracker
#         i = 0
#         self.ask_symptom(first=True)
#         while i<5:
#             self.ask_symptom()
#             i+=1
#         disease = self.get_disease()
#         text = "You may have {}".format(disease)
#         dispatcher.utter_message(text=text)
#
#     def ask_symptom(self,first=False):
#         if first:
#             self.dispatcher.utter_message(template="utter_ask_first_symptom")
#         else:
#             self.dispatcher.utter_message(template="utter_ask_symptoms")
#         symptom = self.tracker.get_latest_entity_values("my_entity_name")
#         self.symptoms.append(symptom)
#         return ([SlotSet("symptom",None)])
#
#     def get_disease(self):
#         print(self.symptoms)
#         return "Covid19"


class ActionAskSymptom(Action):
    def name(self) -> Text:
        return "action_ask_symptom"
    first = True
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if self.first:
            dispatcher.utter_message(template="utter_ask_first_symptom")
            self.first= False
        else:
            dispatcher.utter_message(template="utter_ask_symptoms")

class ActionSaveSymptom(Action):
    def name(self) -> Text:
        return "action_save_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptom = tracker.latest_message['text']
        intent = tracker.latest_message['intent'].get('name')
        if symptom == "/say_symptoms":
            symptom = tracker.events[-3].get("text")
            intent = tracker.events[-3].get("intent").get("name")
        print(symptom)
        print(intent)

        if intent != "say_symptoms":
            return ([])
        symptoms = tracker.get_slot("symptoms_list")
        if not symptoms:
            symptoms = []
        symptoms.append(symptom)
        print(symptoms)
        return ([SlotSet("symptoms_list",symptoms)])

class ActionPredictDisease(Action):
    def name(self) -> Text:
        return "action_predict_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptoms = tracker.get_slot("symptoms_list")
        disease = self.predict_disease(symptoms)
        text = "You may have {}".format(disease)
        dispatcher.utter_message(text = text)
        return ([])

    def predict_disease(self,symptoms):
        print(symptoms)
        return "Covid19"