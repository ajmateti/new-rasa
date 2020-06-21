# pip install -q pyyaml h5py

import pandas as pd
import numpy as np
import re
import tensorflow as tf
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords
from tensorflow.keras.utils import to_categorical
import tensorflow as tf
import difflib
import os
import tensorflow_hub as hub
import pickle


model, df, disease2id, id2disease = None,None,None,None

def preprocess(sentence):
    sentence = sentence.lower().strip()
    split = sentence.split(",")[2:]
    filtered = []
    for i in split:
        if len(i) < 40:
            filtered.append(i)
    sentence = ".".join(filtered)
    sentence = re.sub(r'[,?\"\[\]()]', " ", sentence)
    sentence = re.sub(r'[" "]+', " ", sentence)
    sentence = re.sub(r"[^a-z.]+", " ", sentence)
    sentence = re.sub(r"\b\d+\b", "", sentence)
    s = set(stopwords.words('english'))
    s.update(
        ["symptoms", "signs", "may", "include", "doctor", "usually", "people", "cause", "see", "might", "often", "one",
         "medical", "disease", "common", "make", "also", "seek", "occur", "time", "vary", "sometimes", "type", "notice",
         "especially", "within", "even", "person", "including"])
    filtered_text = filter(lambda w: not w in s, sentence.split())
    return " ".join(filtered_text)


def preprocess_user_input(sentence):
  sentence = sentence.lower().strip()
  sentence = re.sub(r'[,?\"\[\]()]'," ",sentence)
  sentence = re.sub(r'[" "]+', " ", sentence)
  sentence = re.sub(r"[^a-z.]+", " ", sentence)
  sentence = re.sub(r"\b\d+\b", "", sentence)
  s=set(stopwords.words('english'))
  s.update(["symptoms","signs","may","include","doctor","usually","people","cause","see","might","often","one","medical","disease","common","make","also","seek","occur","time","vary","sometimes","type","notice","especially","within","even","person","including"])
  filtered_text = filter(lambda w: not w in s,sentence.split())
  return " ".join(filtered_text)


def load_model():
    global model
    if model is not None:
        return model
    model_link = "https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1"
    hub_layer = hub.KerasLayer(model_link, output_shape=[20], input_shape=[],
                               dtype=tf.string, trainable=True)
    model = tf.keras.Sequential()
    model.add(hub_layer)
    model.add(tf.keras.layers.Dense(256,activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(64,activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(736,activation="sigmoid"))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    path = os.getcwd()+'/estimators/Model2/weights.h5'
    model.load_weights(path)
    return model

def load_df():
    global df
    if df is not None:
        return df
    with open(os.getcwd()+'/estimators/Model2/dataframe.pkl','rb') as f :
        df = pickle.load(f)
    return df

def load_disease2id():
    global disease2id
    if disease2id is not None:
        return disease2id
    with open(os.getcwd()+'/estimators/Model2/disease2id.pkl','rb') as f :
        disease2id = pickle.load(f)
    return disease2id

def load_id2disease():
    global id2disease
    if id2disease is not None:
        return id2disease
    with open(os.getcwd()+'/estimators/Model2/id2disease.pkl','rb') as f :
        id2disease = pickle.load(f)
    return id2disease

def predict_disease(my_input):
    print(my_input)
    model = load_model()
    df = load_df()
    id2disease = load_id2disease()
    disease2id = load_disease2id()
    my_input = preprocess_user_input(my_input)
    model_preds = model.predict([my_input])
    preds = np.argsort(model_preds)[0][::-1]
    pred_vals = np.sort(model_preds)[0][::-1]
    for i, j in zip(preds[:3], pred_vals[:3]):
        print(i, id2disease[i], j)
    # print(df.describe)
    # print(len(disease2id))
    disease = id2disease[preds[0]]
    return [disease,get_overview(disease)]

def get_treatment(disease):
    print("Disease in get_treatment: ")
    print(disease)
    diseaseId = disease2id[disease]
    df = load_df()
    text = df.iloc[diseaseId]['treatment']
    text = re.sub(r'\'s', "s", text)
    text = re.sub(r'\'t', "t", text)
    text = re.sub(r'[,\[\]\"\']', " ", text)
    text = text.split(".")
    text = [sentence.strip() for sentence in text]
    text= ".\n".join(text[:2])
    return text

def get_overview(disease):
    diseaseId = disease2id[disease]
    df = load_df()
    text = df.iloc[diseaseId]['overview']
    text = re.sub(r'\'s', "s", text)
    text = re.sub(r'\'t', "t", text)
    text = re.sub(r'[,\[\]\"\']', " ", text)
    text = text.split(".")
    text = [sentence.strip() for sentence in text]
    text= ".\n".join(text[:5])
    return text

def load_values():
    load_disease2id()
    load_df()
    load_id2disease()
    load_model()

if __name__=="__main__":
   # load_model()
   disease = predict_disease("i have seizures. I have hypermetabolism. I have tremors. I am unresponsive")
   print(get_treatment(disease))