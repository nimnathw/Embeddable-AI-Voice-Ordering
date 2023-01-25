from python:3.8

COPY . .
RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "app.py"]
