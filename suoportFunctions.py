import os
import glob
import json
import requests
import yake
import pandas as pd
from zipfile import ZipFile
from flask import Flask, render_template, request


# decompress the zip files
def read_zip_file(zip_name):
    files = str(os.getcwd() + "/" + zip_name + ".zip")
    with ZipFile(files, "r") as zip_object:
        zip_object.extractall()

    path = str(os.getcwd() + "/" + zip_name + "/*.wav")
    folder = glob.glob(path)

    return sorted(folder, reverse=False)


# get the values from the speech data
def speech_to_text(file):
    # speech url, here port defines on basis of kubernetes port forward
    speech_to_text_url = "http://localhost:1081/speech-to-text/api/v1/recognize?"
    # setting up params models
    params = {"model": "en-US_Multimedia", "smart_formatting": "true", "background_audio_suppression": "0.7"}
    headers = {"Content-Type": "audio/wav"}
    result = requests.post(speech_to_text_url, headers=headers, params=params, data=open(file, 'rb'))

    # get transcript from json result
    output = ""
    json_obj = json.loads(result.text)
    results_data = json_obj["results"]
    for r in results_data:
        for transcript in r["alternatives"]:
            output = output + " " + transcript["transcript"]

    return output


def text_to_speech(texts, name):
    # speech url, here port defines on blsasis of kubernetes port forword
    text_to_speech_url = 'http://localhost:1080/text-to-speech/api/v1/synthesize'
    # setting up the headers for post request to service
    headers = {'Content-Type':'application/json', 'Accept':'audio/wav'}
    # etting up params
    params = {'output':'output_text.wav'}
    # creating a data in JSON format to send as a parameter to the service
    words = {"text":texts}
    
    # method to get the Voice data from the text service
    request =requests.post(text_to_speech_url, headers=headers, params=params, data=words)
    print(request.status_code)
    if request.status_code != 200:
        print("TTS Service status:", request.text)
        print("Creating file ---",name)
    with open(name, mode='bx') as f:
        f.write(request.content)



def get_keywords(texts):
    extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=10, features=None)
    keywords = extractor.extract_keywords(texts)

    return keywords

