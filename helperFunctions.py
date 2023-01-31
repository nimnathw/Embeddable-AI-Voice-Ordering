import os
import glob
import json
import requests
import pandas as pd
from zipfile import ZipFile
from difflib import SequenceMatcher
from nltk.corpus import stopwords
import nltk
# import yake

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


def clean_text(text):
    stop_words = stopwords.words("english")
    stop_words.extend(["gimme", "lemme", "cause", "cuz", "imma", "gonna", "wanna", "please", "the", "and",
                       "gotta", "hafta", "woulda", "coulda", "shoulda", "howdy", "day", "can", "could",
                       "my", "mine", "I" "hey", "yoo", "deliver", "delivery", "delivered", "piece", "want",
                       "send", "sent", "order", "pizza", "piz", "pizze", "address", "addrez", "to", "too"])
    clean_texts = " ".join([word.replace("X", "").replace("/", "") for word in text.split() if word.lower() not in stop_words])
    return clean_texts


def get_keywords(text):
    pizza_size = ["Giant", "Large", "Medium"]
    pizza_topping = ["Pepperoni", "Bacon", "Chicken", "Anchovies", "Mushroom", "Onion", "Black olive", "Green pepper"]
    order_size, order_topping = [], []
    check_size = True

    for word in text.split():
        if check_size:
            for size in pizza_size:
                if SequenceMatcher(None, word, size).ratio() > 0.6:
                    order_size.append(size)
                    check_size = False
        for topping in pizza_topping:
            if SequenceMatcher(None, word, topping).ratio() > 0.6:
                order_topping.append(topping)
                pizza_topping.remove(topping)

    # extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=10, features=None)
    # keywords = extractor.extract_keywords(text)
    return order_size, order_topping


def play_local_wav_file(file_name):
    with open(str("./" + file_name), "rb") as wav:
        data = wav.read(1024)
        while data:
            yield data
            data = wav.read(1024)


def read_zip_file(zip_name):
    files = str(os.getcwd() + "/" + zip_name + ".zip")
    with ZipFile(files, "r") as zip_object:
        zip_object.extractall()

    path = str(os.getcwd() + "/" + zip_name + "/*.wav")
    folder = glob.glob(path)
    return sorted(folder, reverse=False)


def save_audio(file, file_name):
    with open(file_name, "wb") as audio:
        file.save(audio)
        print("file uploaded successfully")

        
def speech_to_text(file_name):
    # speech url
    speech_to_text_url = "https://sn-watson-stt.labs.skills.network/speech-to-text/api/v1/recognize"
    # set up the headers for audio format
    headers = {"Content-Type": "audio/wav"}
    # set up parameters
    params = {"model": "en-US_Multimedia", "smart_formatting": "true", "background_audio_suppression": "0.6"}
    # method to get the Voice data from the text service
    result = requests.post(speech_to_text_url, headers=headers, params=params, data=open(file_name, 'rb'))

    # get transcript from json result
    output = ""
    json_obj = json.loads(result.text)
    results_data = json_obj["results"]
    for r in results_data:
        for transcript in r["alternatives"]:
            output = output + " " + transcript["transcript"]
    return output


def text_to_speech(texts, name, language):
    # remove the existing files in the folder
    bash_command = str("find . -path \*/" + name + " -delete")
    os.system(bash_command)
    
    # text url
    text_to_speech_url = "https://sn-watson-tts.labs.skills.network/text-to-speech/api/v1/synthesize?output=output_text.wav"
    # set up the headers for post request to service
    headers = {"Content-Type": "application/json", "Accept": "audio/wav"}
    # set up parameters
    params = {"rate_percentage": -3, "pitch_percentagequery": 0, "voice":language}
    # create a data in JSON format to send as a parameter to the service
    words = json.dumps({"text": texts})
    # method to get the Voice data from the text service
    request = requests.post(text_to_speech_url, headers=headers, params=params, data=words)
    print(request.status_code)
    if request.status_code != 200:
        print("TTS Service status:", request.text)
        print("Creating file ---", name)
    with open(name, mode="bx") as f:
        f.write(request.content)
