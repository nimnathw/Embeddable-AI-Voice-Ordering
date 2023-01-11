import os
import uuid
import glob
import json
import requests
import yake
import pandas as pd
from zipfile import ZipFile
from flask import Flask, render_template, request, flash, redirect, Response, url_for
from difflib import SequenceMatcher
from nltk.corpus import stopwords
import nltk
nltk.download("stopwords")


def read_zip_file(zip_name):
    files = str(os.getcwd() + "/" + zip_name + ".zip")
    with ZipFile(files, "r") as zip_object:
        zip_object.extractall()

    path = str(os.getcwd() + "/" + zip_name + "/*.wav")
    folder = glob.glob(path)
    return sorted(folder, reverse=False)


def speech_to_text(file):
    # speech url, here port defines on basis of kubernetes port forward
    speech_to_text_url = "http://localhost:1081/speech-to-text/api/v1/recognize?"
    # setting up params models
    params = {"model": "en-US_Multimedia", "smart_formatting": "true", "background_audio_suppression": "0.6"}
    headers = {"Content-Type": "audio/wav"}
    result = requests.post(speech_to_text_url, headers=headers, params=params, data=file)  # data=open(file, "rb")

    # get transcript from json result
    output = ""
    json_obj = json.loads(result.text)
    results_data = json_obj["results"]
    for r in results_data:
        for transcript in r["alternatives"]:
            output = output + " " + transcript["transcript"]
    return output


def text_to_speech(texts, name):
    # remove the existing files in the folder
    bash_command = str("find . -path \*/" + name + " -delete")
    os.system(bash_command)

    # speech url, here port defines on blsasis of kubernetes port forword
    text_to_speech_url = "http://localhost:1080/text-to-speech/api/v1/synthesize"
    # setting up the headers for post request to service
    headers = {"Content-Type": "application/json", "Accept": "audio/wav"}
    # setting up params
    params = {"output": "output_text.wav", "rate_percentage": -3, "pitch_percentagequery": 0}
    # creating a data in JSON format to send as a parameter to the service
    words = json.dumps({"text": texts})
    # method to get the Voice data from the text service
    request = requests.post(text_to_speech_url, headers=headers, params=params, data=words)
    print(request.status_code)
    if request.status_code != 200:
        print("TTS Service status:", request.text)
        print("Creating file ---", name)
    with open(name, mode="bx") as f:
        f.write(request.content)


def get_keywords(text):
    pizza_size = ["large", "medium", "small"]
    pizza_topping = ["pepperoni", "bacon", "chicken", "anchovies", "mushroom", "onion", "black olive", "green pepper"]
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


def clean_text(text):
    stop_words = stopwords.words("english")
    stop_words.extend(["gimme", "lemme", "cause", "cuz", "imma", "gonna", "wanna", "please",
                       "gotta", "hafta", "woulda", "coulda", "shoulda", "howdy", "day",
                       "hey", "yoo", "deliver", "delivery", "delivered", "piece", "want", "order"])
    clean_text = " ".join([word.replace("X", "").replace("/", "") for word in text.split() if word.lower() not in stop_words])
    return clean_text


def get_local_audio_text(file, file_name):
    with open(file_name, "wb") as audio:
        file.save(audio)
        print("file uploaded successfully")
    with open(file_name, "rb") as audio:
        text = speech_to_text(audio)
    return text


def get_local_wav_file(file_name):
    with open(str("./" + file_name), "rb") as wav:
        data = wav.read(1024)
        while data:
            yield data
            data = wav.read(1024)
