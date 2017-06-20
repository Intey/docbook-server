#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, flash, send_from_directory, request, redirect, url_for, render_template
from werkzeug import secure_filename
from os import path, environ

from functools import reduce
pwd = path.abspath(path.dirname(__file__))

UPLOAD_FOLDER = path.join(pwd, "uploads")
ALLOWED_EXTENSIONS = set(['.xml'])

static_url = '/static'

single_mode = True

if environ.get("DEV"):
    static_url = 'http://localhost:3000/static/js'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def save_file(file):
    filename = secure_filename(file.filename)
    filepath= path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath

def allowed_file(filename):
    """
    Checks that filename contains dot and it's extension in allowed extensions
    """
    return path.extsep in filename and \
            path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

FILES_KEY='files[]'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    fileurl = None
    error = None
    if request.method == 'POST':
        if FILES_KEY not in request.files:
            flash('No file part')
            return redirect(request.url)

        uploaded_files = request.files.getlist(FILES_KEY)
        if len(uploaded_files) == 0:
            flash('No selected file')
            return redirect(request.url)

        allFilesAllowed = reduce(lambda acc, file: acc and allowed_file(file.filename),
                                 uploaded_files)
        if allFilesAllowed:
            if len(uploaded_files) == 1:
                file = uploaded_files[0]
                filepath = save_file(file)
                print("after save:", filepath)
                fileurl = url_for('uploaded_file', filename=file.filename)
            else:
                for file in uploaded_files:
                    filepath = save_file(file)
                    error = {
                            "title": "Not implemented yet.",
                            "body": "many files support. Upload single."
                            }

                    #TODO generate docbook from many files

    return render_template('index.html', static_url=static_url, fileurl=fileurl, error=error)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    print(static_url)
    app.run(host="0.0.0.0")
