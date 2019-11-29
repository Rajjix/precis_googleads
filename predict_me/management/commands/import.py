import os
from django.core.management.base import BaseCommand
from predict_me.utils import populate_db_with_csv_data


class Command(BaseCommand):
    help = 'update our models and data'

    objects = {
        'data': 'import_data',
        'update': 'update_data',  # useless for now
    }

    def add_arguments(self, parser):
        parser.add_argument('option',)
        parser.add_argument('file_path',
                            help='csv file path')

    def handle(self, *args, **options):
        obj, file_path = options['option'], options['file_path']
        file_path = file_path if file_path.startswith(
            "/") else f"{os.getcwd()}/{file_path}"
        return getattr(self, self.objects[obj])(file_path)

    def import_data(self, file_path):
        """ Delete old data and insert new data """
        populate_db_with_csv_data(file_path)
        return "Done!!"
