from suoportFunctions import *

app = Flask(__name__)


@app.route('/')
def root():
    global address, order
    return render_template("main.html")


@app.route('/get_info', methods=['POST'])
def get_info():
    return render_template("getInfo.html")


@app.route('/get_topping', methods=['POST'])
def get_topping():
    """
    # call the Bash command to get sample audio files
    bash_command = "wget -c https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-GPXX0E8TEN/labs/data/customer_order.zip"
    os.system(bash_command)
    read_zip_file("customer_order")
    """
    return render_template('getTopping.html')


@app.route('/get_order', methods=['POST'])
def get_order():
    # clean the stop words from audio files
    customer_address = clean_text(address)

    clean_order = clean_text(order)
    order_size, order_topping = get_keywords(clean_order)

    repeat = str("Thank you using Skills Network Pizza App to place your order. I detect you want a " + order_size[0] + " with the following topping: " + " ".join(map(str, order_topping)) + ". " + "The delivery address is: " + customer_address)

    return render_template('getOrder.html', customerAddress=customer_address, orderSize=order_size, orderTopping=order_topping)


@app.route('/get_record', methods=["GET", "POST"])
def get_record():
    if request.method == "POST":
        status = request.form['status']
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        
        if status == "info":
            address = speech_to_text(file)
            print(address)
            return render_template("getInfo.html")
        elif status == "topping":
            order = speech_to_text(file)
            print(order)
            return render_template("getTopping.html")


if __name__ == '__main__':
    app.run()
