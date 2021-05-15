from flask import render_template
import json

def generate_index_page():
    return render_template('index.html')


def genetrate_results_page(resultsFile: str):
    data = None
    with open(resultsFile) as json_file:
        data = json.load(json_file)
    return render_template('results.html', data=data)
    # print(data)
    # return json2html.convert(json=data)