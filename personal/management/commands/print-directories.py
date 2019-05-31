from __future__ import print_function
import os
from django.core.management import BaseCommand, CommandError
from mezzanine.conf import settings

class Command(BaseCommand):
    help = "Prints all the paths of all the important directories and files of this installation"
    # No command line arguments necessary

    def handle(self, *args, **options):
        if not settings.PERSONAL_EDITION:
            raise CommandError('This command only works with Archetype: Personal Edition')

        self.stdout.write('Here are all the important directories and files for this installation of Archetype: Personal Edition')
        self.stdout.write('')

        self.stdout.write('Root project directory: %s' % settings.BASE_DIR)
        self.stdout.write('Database file: %s' % settings.DATABASES['default']['NAME'])
        self.stdout.write('Customisation directory: %s' % settings.CUSTOM_STATIC_PATH)
        self.stdout.write('Image directory: %s' % settings.IMAGE_SERVER_ROOT)

