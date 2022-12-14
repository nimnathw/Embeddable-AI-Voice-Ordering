from suoportFunctions import *

app = Flask(__name__)


@app.route('/')
def cover_page():
    return render_template('cover.html')


@app.route('/get_sample', methods=['POST'])
def get_sample():
    # define and call the Bash command to get audio files from cloud
    bash_command = "wget -c https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-GPXX0E8TEN/labs/data/audio.zip"
    os.system(bash_command)
    return render_template('getSample.html')


@app.route('/get_order', methods=['POST'])
def get_order():
    # get the file name from the form
    file_name = request.form['fileName']
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
    return render_template('getOrder.html', fileName=file_name, reviews=reviews, results=text)


if __name__ == '__main__':
    app.run()
