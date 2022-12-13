from flask import Flask, render_template, request
import os
import glob
import json
import requests
import pandas as pd
from zipfile import ZipFile


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


app = Flask(__name__)


@app.route("/")
def front_page():
    return render_template("index.html")


@app.route("/getorder", methods=["POST"])
def getorder():
    # get the file name from the form
    file_name = request.form["fileName"]

    # define and call the Bash command to get audio files from cloud
    bash_command = "wget -c https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-GPXX0E8TEN/labs/data/audio.zip"
    os.system(bash_command)

    # process speech file & get text data
    text = []
    for file in read_zip_file("audio"):
        if file_name in file:
            text.append(get_text_from_speech(file))

    # TODO:
    # Scape the url
    # reviews = scrape(url)

    # TODO:
    # Get the sentiment
    # sentiment = get_sentiment(reviews)

    # results = sentiment

    # Hard code pretend results for now to demonstrate the app
    reviews = ["This is terrible", "This is great", "This is ok"]

    # Return template with data
    return render_template('getorder.html', fileName=file_name, reviews=reviews, results=text)


if __name__ == '__main__':
    app.run()
