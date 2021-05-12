import os
from flask import Flask, render_template, request

uploads_folder='controller\\uploads'

template_folder = '..\\view\\templates'
app = Flask(__name__, template_folder=template_folder)
app.config['UPLOAD_FOLDER'] = uploads_folder

@app.route('/')
def anomaly_detection_web_app():
    return render_template('index.html')

@app.route("/detect", methods=["POST"])
def detect_anomalies():
    file = request.files['myfile']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'sent ' + file.filename

if __name__ == '__main__':
    app.run(port=8080)