
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import predict


class ActionAskSymptom(Action):
    def name(self) -> Text:
        return "action_ask_symptom"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        first_symptom = tracker.get_slot("first_symptom")
        if first_symptom:
            dispatcher.utter_message(template="utter_ask_first_symptom")
            return ([SlotSet("first_symptom",False)])
        else:
            dispatcher.utter_message(template="utter_ask_symptoms")

        return ([])

class ActionSaveSymptom(Action):
    def name(self) -> Text:
        return "action_save_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptom = tracker.latest_message['text']
        intent = tracker.latest_message['intent'].get('name')
        if symptom == "/say_symptoms":
            symptom = tracker.events[-2].get("text")
            intent = tracker.events[-2].get("intent").get("name")
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
        disease, overview = self.predict_disease(symptoms)
        overview = "Overview:\n" + overview
        text = "You may have {}".format(disease) + "\n" + overview
        dispatcher.utter_message(text = text)
        return ([SlotSet("disease",disease), SlotSet("symptoms_list",[])])

    def predict_disease(self,symptoms):
        symptoms = ' . '.join(symptoms)
        print(symptoms)
        return predict.predict_disease(symptoms)


class ActionGetInfoTreatment(Action):
    def name(self) -> Text:
        return "action_get_info_treatment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        treatment = self.get_treatment(disease)
        treatment = "Treatment:\n" + treatment
        dispatcher.utter_message(text = treatment)
        return ([SlotSet("disease",disease)])

    def get_treatment(self,disease):
        print(disease)
        return predict.get_treatment(disease)



