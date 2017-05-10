#coding:utf-8

import manage
import time
from db.models import Words
from django.db import transaction
from crawler.crawler import run_crawler

@transaction.atomic
def generate_words():
    with open(manage.WORDS_PATH, 'r') as f:
        for word in f:
            Words.objects.create(value = word.strip())


if __name__ == '__main__':

    #generate_words()
    run_crawler(4)
