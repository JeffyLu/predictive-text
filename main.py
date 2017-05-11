#coding:utf-8

import os
import manage
import time
from collections import Counter
from db.models import Words
from django.db import transaction
from crawler.crawler import run_crawler

@transaction.atomic
def generate_words():
    with open(manage.WORDS_PATH, 'r') as f:
        for word in f:
            Words.objects.create(value = word.strip())

def _text_filter(text):
    symbols = ['\n', '\t', '.', '"', '?', '&nbsp;', ',', '&amp;', '(', ')',
               '[', ']', '--', '---', '…', '/', '‘', ';', "'"]
    for s in symbols:
        text = text.replace(s, ' ')
    return text

@transaction.atomic
def stat_counts():
    files = os.listdir(manage.VOA_DIR)
    counter = Counter()
    for fname in files:
        with open(os.path.join(manage.VOA_DIR, fname), 'r') as f:
            text = _text_filter(f.read())
            counter.update(text.split())
    i = 1
    for k, v in counter.items():
        try:
            w = Words.objects.get(value = k)
            w.counts += v
            w.save()
        except:
            print("'%s' is not in database!" % k)
            i += 1
            continue
        print("success %d/%d" % (i, len(counter)))
        i += 1


if __name__ == '__main__':

    generate_words()
    #run_crawler(4)
    stat_counts()
