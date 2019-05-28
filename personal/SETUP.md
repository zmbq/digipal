# Setting up Archaetype - Personal Edition

## Set up the virtual environment
Set up a Python 2.7 virtual environment and activate it.

Install requirements:

    pip install -r build/requirements.txt

## Set up the Django project

The settings for the Personal Edition are located at `personal/personal_settings.py`. You need to copy it (or create a link) to `digipal_project/local_settings.py`

Now you can set up the database. Switch to the project's root directory and run: (note: the following is taken from `build/Dockerfile`)

    python manage.py migrate
    python manage.py loaddata build/data_init.json build/data_char.json build/data_menu.json build/data_test.json
    python manage.py dpsearch index
    python manage.py dpsearch index_facets

Your local SQLite database is now ready

The admin username is `admin`. The password is also `admin`.

## Set up the Frontend

Archaetype: Server Edition uses `tsc` and `lessc` on the fly to handle SCSS And Typescript files. This means NodeJS needs to be installed for the system to run.

We do not want Personal Edition installations to depend on NodeJS, so we precompile these files when building the package.

First, make sure you have Node installed.

Now change directory to `personal/node-utils` and run `npm install` to install all the Node requirements.

Now change back to the project's root and precompile the static files:

    python manage.py precompile-static
