# Scripts that are run from the command line after installation as a package
# They basically just delegate everything to management commands
import os

def get_top_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This file is always in /personal, ==


def print_directories():
    current_dir = os.path.abspath(os.curdir)
    try:
        os.chdir(get_top_dir())
        os.system('python manage.py print-directories')
    finally:
        os.chdir(current_dir)

def run_server():
    current_dir = os.path.abspath(os.curdir)
    try:
        os.chdir(get_top_dir())
        # TODO: Switch to gunicorn or a Windows comparable
        os.system('python manage.py runserver --no-banner')
    finally:
        os.chdir(current_dir)
