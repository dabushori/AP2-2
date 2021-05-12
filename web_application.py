from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def anomaly_detection_app():
    if request.method == 'GET':
        
    elif request.method == 'POST'


if __name__ == '__main__':
    app.run(port=8080)