from suoportFunctions import *


app = Flask(__name__)


@app.route('/')
def root():
    global name, address, topping
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
    # get the file name from the form
    file_name = request.form['fileName']
    # process speech file & get text data
    text = []
    for file in read_zip_file("customer_order"):
        if file_name in file:
            text.append(speech_to_text(file))
    

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
    return render_template('getOrder.html', fileName=file_name, reviews=reviews, results=text)


@app.route('/get_info_record', methods=["GET", "POST"])
def get_info_record():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        
        address = speech_to_text(file)
        print(address)
    
    return render_template("getInfo.html")


if __name__ == '__main__':
    app.run()
