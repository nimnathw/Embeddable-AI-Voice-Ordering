from helperFunctions import *
from flask import Flask, render_template, request, flash, redirect, Response, url_for

app = Flask(__name__)
language, raw_address, customer_address, raw_order, pizza_size, pizza_topping, play_audio = None, None, None, None, None, None, None


@app.route("/")
def root():
    global language, raw_address, customer_address, raw_order, pizza_size, pizza_topping, play_audio
    language, raw_address, customer_address, raw_order, pizza_size, pizza_topping, play_audio = None, None, None, None, None, None, None

    # remove the existing files in the folder
    file = ["intro.wav", "info_record.wav", "intro_repeat.wav", "topping.wav", "topping_record.wav", "topping_repeat.wav"]
    for i in file:
        bash_command = str("find . -path \*/" + i + " -delete")
        os.system(bash_command)
    return render_template("main.html")


@app.route("/get_info", methods=["POST"])
def get_info():
    global language, play_audio
    if not language:
        language = request.form["voice"]
    play_audio = "intro.wav"
    result = "Welcome to La AI Pizza Plaza, how's it going? Where should we send your delicious pizza order to?"
    text_to_speech(result, play_audio, language)
    return render_template("getInfo.html")


@app.route("/get_info_redirect", methods=["GET", "POST"])
def get_info_redirect():
    global customer_address, play_audio
    customer_address = clean_text(raw_address)  # clean the stop words from audio files
    play_audio = "intro_repeat.wav"
    result = "Just want to confirm, did ya ask for the pizza to be dropped off at " + customer_address + \
             "? If not, no worries, just give the recording again button a tap."
    text_to_speech(result, play_audio, language)
    return render_template("getInfoRedirect.html", customerAddress=customer_address)


@app.route("/get_topping", methods=["POST"])
def get_topping():
    global play_audio
    play_audio = "topping.wav"
    result = "What size of pizza are you looking for? We got three options: giant, large, and medium. " \
             "Also, what kind of toppings do you want on your pizza? We have pepperoni, bacon, chicken, anchovies, " \
             "mushroom, onion, black olives, and green pepper."
    text_to_speech(result, play_audio, language)
    return render_template("getTopping.html")


@app.route("/get_topping_redirect", methods=["GET", "POST"])
def get_topping_redirect():
    global pizza_size, pizza_topping, play_audio
    clean_order = clean_text(raw_order)  # clean the stop words from audio files
    pizza_size, pizza_topping = get_keywords(clean_order)

    play_audio = "topping_repeat.wav"
    result = "Just wanted to make sure, did ya order a " + pizza_size[0] + " pizza with: " + " ".join(map(str, pizza_topping)) + \
             " on it? If not, no worries, just give the recording again button another press."
    text_to_speech(result, play_audio, language)
    return render_template("getToppingRedirect.html", pizzaSize=pizza_size[0], pizzaTopping=pizza_topping)


@app.route("/get_order", methods=["POST"])
def get_order():
    global play_audio
    play_audio = "order.wav"
    if not customer_address:
        print("missing address")
    elif not pizza_size:
        print("missing pizza size")
        order_size = ["Not defined"]
    elif not pizza_topping:
        print("missing pizza topping")

    result = str("Thanks for using the La AI Pizza Plaza to place your order. Just wanted to double check that I got it right, ya want a " +
                 pizza_size[0] + " pizza with " + " ".join(map(str, pizza_topping)) + ". And the delivery address is " + customer_address +
                 ", is that correct")
    text_to_speech(result, play_audio, language)
    return render_template("getOrder.html", customerAddress=customer_address, orderSize=pizza_size[0], orderTopping=pizza_topping)


@app.route("/get_info_upload_wav", methods=["POST"])
def get_info_upload_wav():
    global raw_address
    if "info_upload_wav" not in request.files:
        return "No audio file found"
    else:
        file = request.files["info_upload_wav"]
        if file.filename == "":
            return "No audio file selected"
        else:
            raw_address = speech_to_text(file)
            print(raw_address)
    return redirect(url_for("get_info_redirect"))


@app.route("/get_info_record_wav", methods=["POST"])
def get_info_record_wav():
    global raw_address
    if "info_record_wav" not in request.files:
        return "No audio file found"
    else:
        file = request.files["info_record_wav"]
        if file.filename == "":
            return "No audio file selected"
        else:
            raw_address = get_local_audio_text(file, "info_record.wav")
            print(raw_address)
    return render_template("getInfoRedirect.html")


@app.route("/get_topping_upload_wav", methods=["POST"])
def get_topping_upload_wav():
    global raw_order
    if "topping_upload_wav" not in request.files:
        return "No audio file found"
    else:
        file = request.files["topping_upload_wav"]
        if file.filename == "":
            return "No audio file selected"
        else:
            raw_order = speech_to_text(file)
            print(raw_order)
    return render_template("getToppingRedirect.html")


@app.route("/get_topping_record_wav", methods=["POST"])
def get_topping_record_wav():
    global raw_order
    if "topping_record_wav" not in request.files:
        return "No audio file found"
    else:
        file = request.files["topping_record_wav"]
        if file.filename == "":
            return "No audio file selected"
        else:
            raw_order = get_local_audio_text(file, "topping_record.wav")
            print(raw_order)
    return redirect("/get_topping_redirect")


"""
@app.route("/audio_name", methods=["POST"])
def audio_name():
    global audioName
    audioName = request.form["audioName"]
    return render_template("getOrder.html")
"""


@app.route("/play_local_wav")
def play_local_wav():
    return Response(get_local_wav_file(play_audio), mimetype="audio/x-wav")


if __name__ == "__main__":
    app.run(debug=False, use_reloader=True, port=8080, host="0.0.0.0")
