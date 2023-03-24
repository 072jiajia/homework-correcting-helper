from flask import Flask, redirect, render_template, request, send_file
from glob import glob

import pickle
import os
import json

from datetime import datetime


comments_file = "comments.pickle"
if os.path.exists(comments_file):
    with open(comments_file, 'rb') as handle:
        data = pickle.load(handle)
    
    os.makedirs("backup", exist_ok=True)
    now = datetime.strftime(datetime.now(),'%Y-%m-%d-%H.%M.%S') 
    with open(f"backup/{now}-{comments_file}", 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(f"backup/{now}-result.json", 'w') as fp:
        json.dump(data, fp)
else:
    data = {}

app = Flask(__name__)


filenames = [
    filename.replace("\\", "/")
    for filename in glob("submissions/*.pdf")
]


@app.route('/', methods=['GET'])
def get_page():
    id = int(request.args.get("id", 0))
    filename = filenames[id]
    comment = ""
    if filename in data:
        comment = data[filename]
    return render_template(
        'main.html',
        id=id,
        total=len(filenames),
        filename=filename,
        comment= comment
    )

@app.route('/submissions/<filename>', methods=['GET'])
def get_submission(filename):
    return send_file("submissions/"+filename)


@app.route('/static/<filename>', methods=['GET'])
def get_js(filename):
    return send_file("static/"+filename)


@app.route('/comment', methods=['POST'])
def comment():
    filename = request.form['filename']
    comment = request.form['comment']
    
    data[filename] = comment

    with open(comments_file, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('result.json', 'w') as fp:
        json.dump(data, fp)
    
    return "success"



if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run("0.0.0.0", 50100)
