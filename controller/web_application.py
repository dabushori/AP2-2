import os
from flask import Flask, render_template, request
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from model import anomaly_detection

uploads_folder='controller\\uploads'

template_folder = '..\\view\\templates'
app = Flask(__name__, template_folder=template_folder)
app.config['UPLOAD_FOLDER'] = uploads_folder

@app.route('/')
def anomaly_detection_web_app():
    return render_template('index.html')

@app.route("/detect", methods=["POST"])
def detect():
    file = request.files['learnFile']
    learnFile = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(learnFile)

    file = request.files['anomaliesFile']
    anomaliesFile = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(anomaliesFile)

    resultsFile = anomaly_detection.detect_anomalies(learnFile, anomaliesFile)
    print(resultsFile)

    return 'path to learn file: {}<br>path to anomalies file: {}<br>results: {}'.format(learnFile, anomaliesFile, resultsFile)

if __name__ == '__main__':
    app.run(port=8080)