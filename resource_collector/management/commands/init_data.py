from django.core.management.base import BaseCommand
from resource_collector.crawler.voa import run_crawler


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-c', '--cpu', dest='cpu', type=int)

    def handle(self, *args, **options):
        cpu = options.get('cpu') or 4
        run_crawler(cpu=cpu)
