import os
import glob
import json
import requests
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
def get_text_from_speech(file):
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
