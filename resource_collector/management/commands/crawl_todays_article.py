from django.core.management.base import BaseCommand
from resource_collector.crawler.voa import run_crawler


class Command(BaseCommand):

    def handle(self, *args, **options):
        run_crawler(crawl_today=True)
