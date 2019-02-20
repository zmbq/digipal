from __future__ import print_function
import shutil

import os

from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Precompiles all the LESS and Typescript files"

    def get_project_dir(self):
        return os.path.dirname(settings.PROJECT_ROOT)

    def add_arguments(self, parser):
        parser.add_argument('--output-dir', type=str, help='Output Directory for Precompiled Files',
                            default=settings.PRECOMPILED_STATIC)
        parser.add_argument('--no-less', action='store_true', default=False,
                            help='Do not process less files')
        parser.add_argument('--no-typescript', action='store_true', default=False,
                            help='Do not process Typescript files')
        parser.add_argument('--clear-output', action='store_true', default=False,
                            help='Clear output directory before proceeding')
        parser.add_argument('--project-dir', type=str, default=self.get_project_dir(), help='Project source dir')
        parser.add_argument('--node-bin-dir', type=str, default=os.path.join('standalone', 'node_modules', '.bin'),
                            help='Directory with Node binaries')

    def handle(self, output_dir, no_less, no_typescript, clear_output, project_dir, node_bin_dir, *args, **options):
        if no_less and no_typescript:
            self.stderr.write('--no-less and --no-typescript both specified, nothing to do here')
            return

        self.stdout.write('Precompiling all static files in %s into %s' % (project_dir, output_dir))

        if clear_output:
            self.stdout.write('Clearing output directory')
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.project_dir = project_dir
        self.output_dir = output_dir
        self.run_less = not no_less
        self.run_typescript = not no_typescript
        self.node_bin_dir = node_bin_dir

        self.stdout.write('Processing the digipal app...')
        self.process_app('digipal')

        self.stdout.write('Processing the digipal_text app...')
        self.process_app('digipal_text')

        self.stdout.write('Done')

    def process_app(self, app_name):
        static_root = os.path.join(self.project_dir, app_name, 'static')
        for (root, dirs, files) in os.walk(static_root):
            for file in files:
                absolute_path = os.path.join(root, file)
                relative_path = absolute_path[len(static_root) + 1:]
                _, ext = os.path.splitext(absolute_path)
                if ext == '.less' and self.run_less:
                    self.process_less(absolute_path, relative_path)
                elif ext == '.ts' and self.run_typescript:
                    self.process_typescript(absolute_path, relative_path)

    def process_less(self, absolute_path, relative_path):
        output_path = self.get_output_path(relative_path, '.css')
        self.run_node_command('lessc', absolute_path, output_path)

    def process_typescript(self, absolute_path, relative_path):
        output_dir = self.get_output_dir(relative_path)
        self.run_node_command('tsc', absolute_path, '--outDir', output_dir)

    def get_output_dir(self, relative_path):
        output_path = os.path.join(self.output_dir, relative_path)
        output_dirname = os.path.dirname(output_path)
        if not os.path.exists(output_dirname):
            os.makedirs(output_dirname)
        return output_dirname

    def get_output_path(self, relative_path, output_extension):
        relative_path_no_ext, _ = os.path.splitext(relative_path)
        relative_path_new_ext = relative_path_no_ext + output_extension
        output_path = os.path.join(self.output_dir, relative_path_new_ext)
        output_dirname = os.path.dirname(output_path)
        if not os.path.exists(output_dirname):
            os.makedirs(output_dirname)

        return output_path

    def run_node_command(self, cmd, *args):
        if self.node_bin_dir:
            cmd = os.path.join(self.node_bin_dir, cmd)
        command_string = ' '.join([cmd] + list(args))
        print("Running ", command_string)
        os.system(command_string)
