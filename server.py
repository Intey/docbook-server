#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import check_output, CalledProcessError, STDOUT
from functools import reduce
import shutil

from flask import Flask, flash, send_from_directory, request, redirect, url_for, render_template
from werkzeug import secure_filename

pwd = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(pwd, "uploads")
ALLOWED_EXTENSIONS = set(['.xml'])
BUILD_DIR = os.path.join(pwd, "build")

static_url = '/static'

FILES_KEY='files[]'

if os.environ.get("DEV"):
    static_url = 'http://localhost:3000/static/js'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def indir(dir):
    """decorator for run some function in specific directory 'dir'. after
    decorate, before run this target function, os change dir to 'dir' and after
    exit from it"""
    def real_dec(func):
        def wrapper(*args):
            pwd = os.path.abspath(os.path.curdir)
            os.chdir(dir)
            try:
                result = func(*args)
            except Exception as e:
                os.chdir(pwd)
                raise e
            return result
        return wrapper
    return real_dec


def log_error(*args):
    print("ERROR:", *args, file=sys.stderr)


def save_file(file):
    filename = secure_filename(file.filename)
    filepath= os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath


def allowed_file(filename):
    """
    Checks that filename contains dot and it's extension in allowed extensions
    """
    return os.path.extsep in filename and \
            os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


def make_error(title, body):
    return {"title": title, "body": body}

def generate_pdf(filepaths):
    # FIXME: single file mode
    if len(filepaths) > 1:
        return None, "Can't generate pdf from many files. Wait later version"
    if len(filepaths) == 0:
        return None, "Can't generate pdf from void"

    filepath = filepaths[0]
    dest_dir = os.path.join(pwd, 'build')
    dest_file = os.path.join(dest_dir, 'data.xml')
    os.makedirs(dest_dir, exist_ok=True)
    try:
        print("copy", filepath, dest_file)
        shutil.copy(filepath, dest_file)
    except Exception as e:
        return None,"Error when prepare build: %s" % e

    @indir(dest_dir)
    def make():
        resultfile = None
        errors = None
        try:
            output = check_output(['make'], stderr=STDOUT).decode('utf-8')
            # last rule(Makefile: where fop called) echoing it's name - pdf name
            print(output)
            resultfile = output.splitlines()[-1]
            print("pdf succesfully generated", resultfile)
        except CalledProcessError as e:
            errors = e.stdout.decode('utf-8').splitlines()
        finally:
            return resultfile, errors

    return make()


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
                generated_filename, errors = generate_pdf([uploaded_file])

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

    return render_template('index.html', static_url=static_url, fileurl=fileurl, error=error)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
