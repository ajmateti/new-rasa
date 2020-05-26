

## story_1
* greet
   - utter_greet
   - utter_ask_name
* inform{"name":"ajay"}
   - slot{"name":"ajay"}
   - utter_introduction
* ask_for_diagnosis
   - action_ask_symptom
* say_symptoms{"symptom":"fever"}
   - slot{"symptom":"fever"}
   - action_save_symptom
   - action_ask_symptom
* deny
   - action_predict_disease
   - utter_goodbye
   
## story_1_2
* greetings_with_name{"name":"ajay"}
   - slot{"name":"ajay"}
   - utter_introduction
* ask_for_diagnosis
   - action_ask_symptom
* say_symptoms{"symptom":"fever"}
   - slot{"symptom":"fever"}
   - action_save_symptom
   - action_ask_symptom
* deny
   - action_predict_disease
   - utter_goodbye
   
## story_6
* greetings_with_name{"name":"spoorthi"}
   - slot{"name":"spoorthi"}
   - utter_greet
   - utter_introduction
* ask_for_diagnosis
   - action_ask_symptom
* say_symptoms{"symptom":"fever"}
   - slot{"symptom":"fever"}
   - action_save_symptom
   - action_ask_symptom
* deny
   - action_predict_disease
   - utter_goodbye
      

## story_2
* greet
   - utter_greet
   - utter_ask_name
* inform{"name":"aneesh"}
   - slot{"name":"aneesh"}
   - utter_introduction
* ask_for_diagnosis
   - action_ask_symptom
* deny
   - utter_goodbye

## story_5
* greet + inform{"name":"ajay"}
   - slot{"name":"ajay"}
   - utter_greet
   - utter_introduction
* ask_for_diagnosis
   - action_ask_symptom
* deny
   - utter_goodbye


## story_3
* greet
   - utter_greet
   - utter_ask_name
* inform{"name":"ajay"}
   - slot{"name":"ajay"}
   - utter_introduction
* ask_for_diagnosis
   - action_ask_symptom
* say_symptoms{"symptom":"fever"}
   - slot{"symptom":"fever"}
   - action_save_symptom
   - action_ask_symptom
* say_symptoms{"symptom":"headache"}
   - slot{"symptom":"headache"}
   - action_save_symptom
   - action_ask_symptom
* deny
   - action_predict_disease
   - utter_goodbye
   
## story_4
* greet + inform{"name":"aneesh"}
   - slot{"name":"aneesh"}
   - utter_greet
   - utter_introduction
* ask_for_diagnosis
   - action_ask_symptom
* say_symptoms{"symptom":"fever"}
   - slot{"symptom":"fever"}
   - action_save_symptom
   - action_ask_symptom
* say_symptoms{"symptom":"headache"}
   - slot{"symptom":"headache"}
   - action_save_symptom
   - action_ask_symptom
* deny
   - action_predict_disease
   - utter_goodbye