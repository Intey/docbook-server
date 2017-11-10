from subprocess import check_output, CalledProcessError, STDOUT
import os
import shutil

ALLOWED_EXTENSIONS = set([
    'xml', 
    'yaml'
])


def allowed_file(filename):
    """ Checks that filename contains dot and it's extension in allowed
    extensions """
    hasExtension = os.path.extsep in filename
    return hasExtension and file_ext(filename) in ALLOWED_EXTENSIONS


def file_ext(filename):
    """ returns filename and extension """
    return os.path.splitext(os.path.basename(filename))[1].lower()[1:]


def run_in_dir(dir):
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


def generate_pdf(filepath):
    dest_dir = os.path.join(pwd, 'build')
    ext = file_ext(filepath) # for make target name by ext
    target = ext.strip(os.path.extsep)

    filename = os.path.basename(filepath)  # name + ext

    dest_file = os.path.join(dest_dir, filename)
    os.makedirs(dest_dir, exist_ok=True)
    try:
        print("copy", filepath, dest_file)
        shutil.copy(filepath, dest_file)
    except Exception as e:
        return None,"Error when prepare build: %s" % e

    @run_in_dir(dest_dir)
    def make(target):
        resultfile = None
        errors = None
        try:
            output = check_output(['make', target], stderr=STDOUT).decode('utf-8')
            # last rule(Makefile: where fop called) echoing it's name - pdf name
            print(output)
            resultfile = output.splitlines()[-1]
            print("pdf succesfully generated", resultfile)
        except CalledProcessError as e:
            errors = e.stdout.decode('utf-8').splitlines()
        finally:
            return resultfile, errors

    return make(target)

