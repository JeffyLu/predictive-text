from predictive.models import Vocabulary
from django.db import IntegrityError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filename', dest='filename')

    def handle(self, *args, **options):
        filename = options.get('filename', '').strip()
        if not filename:
            print('{} not found')
            return
        with open(filename, 'r') as f:
            imported = 0
            for line in f:
                word = line.strip()
                if not word or len(word) >= 32:
                    continue
                try:
                    Vocabulary.objects.create(word=word)
                    imported += 1
                except IntegrityError:
                    pass
            print('total imported: {}'.format(imported))
