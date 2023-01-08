from suoportFunctions import *

app = Flask(__name__)
address, order, audioName = None, None, "customer.wav"


@app.route("/")
def root():
    return render_template("main.html")


@app.route("/get_info", methods=["POST"])
def get_info():
    return render_template("getInfo.html")


@app.route("/get_info_redirect", methods=["GET", "POST"])
def get_info_redirect():
    return render_template("getInfoRedirect.html")


@app.route("/get_topping", methods=["POST"])
def get_topping():
    """
    # call the Bash command to get sample audio files
    bash_command = "wget -c https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-GPXX0E8TEN/labs/data/customer_order.zip"
    os.system(bash_command)
    read_zip_file("customer_order")
    """
    return render_template("getTopping.html")


@app.route("/get_topping_redirect", methods=["GET", "POST"])
def get_topping_redirect():
    return render_template("getToppingRedirect.html")


@app.route("/get_order", methods=["POST"])
def get_order():
    # clean the stop words from audio files
    customer_address = clean_text(address)
    clean_order = clean_text(order)
    order_size, order_topping = get_keywords(clean_order)

    if not customer_address:
        print("missing address")
    elif not order_size:
        print("missing order size")
        order_size = ["Not defined"]
    elif not order_topping:
        print("missing order topping")

    result = str("Thank you for using the Skills Network Pizza App to place your order. I detected you want a " + order_size[0]
                 + " pizza with the following topping: " + " ".join(map(str, order_topping)) + ". " + "The delivery address is "
                 + customer_address + ".")
    text_to_speech(result, "customer.wav")

    return render_template("getOrder.html", customerAddress=customer_address, orderSize=order_size[0], orderTopping=order_topping)


@app.route("/get_info_upload_wav", methods=["POST"])
def get_info_upload_wav():
    global address
    if "info_upload_wav" not in request.files:
        return "No audio file found"
    else:
        file = request.files["info_upload_wav"]
        if file.filename == "":
            return "No audio file selected"
        else:
            address = speech_to_text(file)
            print(address)

    return redirect("/get_info_redirect")


@app.route("/get_info_record_wav", methods=["POST"])
def get_info_record_wav():
    global address
    if "info_record_wav" not in request.files:
        return "No audio file found"
    else:
        file = request.files["info_record_wav"]
        if file.filename == "":
            return "No audio file selected"
        else:
            address = read_audio_file(file)
            print(address)

    return redirect("/get_info_redirect")


@app.route("/get_topping_upload_wav", methods=["POST"])
def get_topping_upload_wav():
    global order
    if "topping_upload_wav" not in request.files:
        return "No audio file found"
    else:
        file = request.files["topping_upload_wav"]
        if file.filename == "":
            return "No audio file selected"
        else:
            order = speech_to_text(file)
            print(order)

    return redirect("/get_topping_redirect")


@app.route("/get_topping_record_wav", methods=["POST"])
def get_topping_record_wav():
    global order
    if "topping_record_wav" not in request.files:
        return "No audio file found"
    else:
        file = request.files["topping_record_wav"]
        if file.filename == "":
            return "No audio file selected"
        else:
            order = read_audio_file(file)
            print(order)

    return redirect("/get_topping_redirect")


"""
@app.route("/audio_name", methods=["POST"])
def audio_name():
    global audioName
    audioName = request.form["audioName"]
    return render_template("getOrder.html")
"""


@app.route("/play_stream_wav")
def play_stream_wav():
    def generate(name):
        with open(str("./" + name), "rb") as wav:
            data = wav.read(1024)
            while data:
                yield data
                data = wav.read(1024)

    return Response(generate(audioName), mimetype="audio/x-wav")


if __name__ == "__main__":
    app.run()
