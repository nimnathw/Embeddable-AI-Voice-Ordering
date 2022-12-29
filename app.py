from suoportFunctions import *

app = Flask(__name__)


@app.route('/')
def root():
    return render_template("main.html")

@app.route('/get_info', methods=['POST'])
def get_info():
    global name, address
    name = request.form['name']
    address = request.form['address']

    return render_template("getInfo.html")


@app.route('/get_topping', methods=['POST'])
def get_topping():
    # call the Bash command to get sample audio files
    bash_command = "wget -c https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-GPXX0E8TEN/labs/data/customer_order.zip"
    os.system(bash_command)
    read_zip_file("customer_order")

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


@app.route('/save-record', methods=['POST'])
def save_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = str(uuid.uuid4()) + ".mp3"
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(full_file_name)
    return '<h1>Success</h1>'


if __name__ == '__main__':
    app.run()
