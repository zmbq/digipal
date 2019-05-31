# Scripts that are run from the command line after installation as a package
# They basically just delegate everything to management commands
import os
import sys


def get_top_dir():
    import digipal_project
    project_dir = os.path.abspath(digipal_project.__path__[0])
    return os.path.dirname(project_dir)


def run_management_command(*args):
    curdir = os.curdir
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digipal_project.settings")
    from django.core.management import execute_from_command_line
    try:
        os.chdir(get_top_dir())
        execute_from_command_line(['scripts.py'] + list(args))
    finally:
        os.chdir(curdir)


def print_directories():
    run_management_command('print-directories')


def run_server():
    # Use waitress-serve on Windows, and gunicorn on all other platforms
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digipal_project.settings")
    if os.name == 'nt':
        os.system('waitress-serve --listen=127.0.0.1:8000 --threads 8 personal.wsgi:application')
    else:
        os.system('gunicorn --workers 4 --bind 127.0.0.1:8000 personal.wsgi')

if __name__ == '__main__':
    run_server()
