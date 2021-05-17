import os
from flask import Flask, render_template, request, send_file
import sys
import shutil

# add the parent dir to PATH so the model and view modules can be imported
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# import the model module
from model import anomaly_detection
# import the view module
from view import page_generator

# clean the uploads folder
uploads_folder = os.path.join('controller', 'uploads')
if os.path.isdir(uploads_folder):
    shutil.rmtree(uploads_folder)
os.mkdir(uploads_folder)

template_folder = os.path.join('..', os.path.join('view', 'templates'))

app = Flask(__name__, template_folder=template_folder)
app.config['UPLOAD_FOLDER'] = uploads_folder

if (len(sys.argv) != 3):
    print('Arguments need to be "<server_ip> <server_port>"')
    exit(1)
server_ip = sys.argv[1]
server_port = sys.argv[2]
try: 
    server_port = int(server_port)
except ValueError:
    print('Error in the port argument.')
    print('Arguments need to be "<server_ip> <server_port>"')
    exit(1)
if (server_port < 0 or server_port > 65535):
    print('Port must be 0-65535.')
    exit(1)

detector = anomaly_detection.AnomalyDetector(server_ip, server_port)


@app.route('/')
def anomaly_detection_web_app():
    return page_generator.generate_index_page()


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

    resultsFile = detector.detect_anomalies(learnFile, anomaliesFile, is_hybrid)
    if resultsFile == None:
        return '<h1> An error occured </h1>'

    if 'table_view' in request.form:
        return page_generator.genetrate_results_page(resultsFile)
    resultsFile = os.path.join('..', resultsFile)
    return send_file(resultsFile)


if __name__ == '__main__':
    app.run(port=8080)
