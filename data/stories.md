

## story_1
* greet
   - utter_greet
   - utter_ask_name
* inform{"name":"ajay"}
   - utter_introduction
* ask_for_diagnosis
   - action_diagnose
   - utter_goodbye
   
## story_2
* greetings_with_name{"name":"ajay"}
   - utter_greet
   - utter_introduction
* ask_for_diagnosis
   - action_diagnose
   - utter_goodbye
