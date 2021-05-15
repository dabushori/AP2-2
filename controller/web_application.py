import os
from flask import Flask, render_template, request, send_file
import sys
import shutil
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from model import anomaly_detection

# clean the uploads folder
uploads_folder='controller\\uploads'
if os.path.isdir(uploads_folder):
    shutil.rmtree(uploads_folder)
os.mkdir(uploads_folder)

template_folder = '..\\view\\templates'
static_folder = '..\\view\\static'
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config['UPLOAD_FOLDER'] = uploads_folder

detector = anomaly_detection.AnomalyDetector('192.168.1.167', 8081)

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

    algorithm = request.form.get('algorithm')
    is_hybrid = False
    if (algorithm == 'hybrid'):
        is_hybrid = True

    print(is_hybrid)
    
    resultsFile = detector.detect_anomalies(learnFile, anomaliesFile, is_hybrid)
    resultsFile = os.path.join('..', resultsFile)

    return send_file(resultsFile)


if __name__ == '__main__':
    app.run(port=8080)