from flask import render_template
from json2html import *
import json
import json

def generate_index_page():
    return render_template('index.html')


def genetrate_results_page(resultsFile: str):
    print(json2html.convert(resultsFile))
    data = None
    with open(resultsFile) as json_file:
        data = json.load(json_file)
    return render_template('results.html', data=data)
    # print(data)
    # return json2html.convert(json=data)