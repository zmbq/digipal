# This management command prepares everything for the distribution of Archetype: Personal Edition
# Important! This command resets the database. If you have something important, do not run it!
import os
import shutil

from django.core.management import BaseCommand, call_command
from mezzanine.conf import settings


class Command(BaseCommand):
    help = "Prepares everything for packaging as a PyPI package"
    def add_arguments(self, parser):
        parser.add_argument('--no-input', default=False, action='store_true', help='Skip asking the user for confirmation')

    def get_confirmation(self):
        self.stdout.write('Careful! This command deletes the current database and customisations!')
        response = raw_input('Are you sure you want to proceed? (type "yes" to proceed) ')

        return response == 'yes'

    def handle(self, no_input, *args, **options):
        self.stdout.write('Prepare Archetype: Personal Edition for Packaging')
        self.stdout.write('')

        if not no_input:
            if not self.get_confirmation():
                self.stdout.write('Command aborted by user')
                return

        self.delete_files()
        self.create_static_files()
        self.create_database()

        self.stdout.write('Archetype: Personal is ready for packaging.')

    def delete_files(self):
        def del_file(what, filename):
            self.stdout.write('Deleting %s...' % what, ending='')
            self.stdout.flush()
            if os.path.isfile(filename):
                os.remove(filename)
            self.stdout.write('deleted')

        def del_dir(what, dirname):
            self.stdout.write('Deleting %s...' % what, ending='')
            self.stdout.flush()
            if os.path.isdir(dirname):
                shutil.rmtree(dirname)
            self.stdout.write('deleted')

        del_dir('static files', settings.STATIC_ROOT)
        del_dir('precompiled static files', settings.PRECOMPILED_STATIC_ROOT)
        del_file('database file', settings.DATABASES['default']['NAME'])
        del_dir('customisations', settings.CUSTOM_STATIC_PATH)

    def create_database(self):
        self.stdout.write('Creating database...')
        call_command('migrate')

        fixture_path = os.path.join(settings.BASE_DIR, 'build')
        fixtures = ['data_init.json', 'data_char.json', 'data_menu.json', 'data_test.json']
        self.stdout.write('Loading fixtures...')
        for fixture in fixtures:
            call_command('loaddata', os.path.join(fixture_path, fixture))

        self.stdout.write('Preparing indices')
        call_command('dpsearch', 'index')
        call_command('dpsearch', 'index_facets')

    def create_static_files(self):
        self.stdout.write('Installing node dependencies')
        curdir = os.curdir
        try:
            os.chdir(os.path.join(settings.BASE_DIR, 'personal', 'node-utils'))
            os.system('npm install')
        finally:
            os.chdir(curdir)

        self.stdout.write('Precompiling static files')
        call_command('precompile-static')

        self.stdout.write('Collecting static files')
        if not os.path.isdir(settings.CUSTOM_STATIC_PATH):
            os.makedirs(settings.CUSTOM_STATIC_PATH)
        call_command('collectstatic', '--noinput')
