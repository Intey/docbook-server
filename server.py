#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import shutil

from flask import Flask, flash, send_from_directory, request, redirect, url_for, render_template
from werkzeug import secure_filename

from utils import allowed_file, file_ext, run_in_dir, generate_pdf

pwd = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(pwd, "uploads")
BUILD_DIR = os.path.join(pwd, "build")

static_url = '/static'

FILES_KEY='files[]'

# in dev use webpack
if os.environ.get("DEV"):
    static_url = 'http://localhost:3000/static/js'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def log_error(*args):
    print("ERROR:", *args, file=sys.stderr)


def save_file(file):
    filename = secure_filename(file.filename)
    filepath= os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath


def make_error(title, body):
    return {"title": title, "body": body}


def process_post(request):
    if FILES_KEY not in request.files:
        flash('No file part')
        return redirect(request.url)

    uploaded_files = request.files.getlist(FILES_KEY)
    if len(uploaded_files) == 0:
        flash('No selected file')
        return redirect(request.url)

    all_files_allowed = True
    not_allowed_files = []
    for filename in map(lambda x: x.filename, uploaded_files):
        if not allowed_file(filename):
            all_files_allowed = False
            not_allowed_files.append(filename)

    if all_files_allowed:
        if len(uploaded_files) == 1:
            file = uploaded_files[0]
            uploaded_file = save_file(file)
            generated_filename, errors = generate_pdf(uploaded_file)

            if generated_filename is not None:
                generated_filepath = os.path.join(BUILD_DIR, generated_filename)
                try:
                    shutil.copy(generated_filepath, UPLOAD_FOLDER)
                    fileurl = url_for('uploaded_file', filename=os.path.basename(generated_filepath))
                except Exception as e:
                    log_error(e)
                    error = make_error("Make url for file", e)
            else:
                log_error(errors)
                error = make_error("can't generate pdf", "\n".join(errors))
    else:
        error = make_error("Wrong files", "files (%s) not allowed" % ', '.join(not_allowed_files))


@app.route('/', methods=['GET'])
def upload_file():
    error = None
    return render_template('index.html', static_url=static_url)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/from-file', methods=['POST'])
def from_file():
    process_post(request)
    return render_template('index.html', static_url=static_url, fileurl=fileurl, error=error)


@app.route('/from-form', methods=['POST'])
def from_form():
    process_post(request)
    return render_template('index.html', static_url=static_url, fileurl=fileurl, error=error)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(host="0.0.0.0", port=8000)
