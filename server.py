#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, flash, send_from_directory, request, redirect, url_for, render_template
from werkzeug import secure_filename
from os import path, environ

pwd = path.abspath(path.dirname(__file__))

UPLOAD_FOLDER = path.join(pwd, "uploads")
ALLOWED_EXTENSIONS = set(['.xml'])

static_url = '/static'


if environ.get("DEV"):
    static_url = 'http://localhost:3000/static/js'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    """
    Checks that filename contains dot and it's extension in allowed extensions
    """
    return path.extsep in filename and \
            path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    fileurl = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
            fileurl = url_for('uploaded_file', filename=filename)

    return render_template('index.html', static_url=static_url, fileurl=fileurl)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    print(static_url)
    app.run()
