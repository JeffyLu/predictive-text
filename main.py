#coding:utf-8

import os
import manage
import time
import queue
import threading
from collections import Counter
from db.models import Words
from django.db import transaction
from crawler.crawler import run_crawler

@transaction.atomic
def generate_words(init = None):
    with open(manage.WORDS_PATH, 'r') as f:
        cnt = 1
        for word in f:
            word = word.strip()
            if init and word in init:
                Words.objects.create(value = word.strip(), counts = init[word])
            else:
                Words.objects.create(value = word.strip())
            print(cnt)
            cnt += 1

def _text_filter(text):
    symbols = ['\n', '\t', '.', '"', '?', '&nbsp;', ',', '&amp;', '(', ')',
               '[', ']', '--', '---', '…', '/', '‘', ';', ':', '$', '%',
               '-', '!']
    for s in symbols:
        text = text.replace(s, ' ')
    return text


class MultiThreadUpdate(threading.Thread):

    def __init__(self, name, task_queue):
        threading.Thread.__init__(self, name = name)
        self.task_queue = task_queue

    @transaction.atomic
    def run(self):
        while not self.task_queue.empty():
            v, cnt = self.task_queue.get()
            try:
                w = Words.objects.get(value = v)
                w.counts += cnt
            except:
                print("'%s' is not in database!" % v)
                continue
            print("[SUCCESS] t%s: %d left." % (
                self.getName(), self.task_queue.qsize()))
            self.task_queue.task_done()

def stat_counts():
    _dirs = os.listdir(manage.VOA_DIR)
    files = []
    for d in _dirs:
        [files.append(os.path.join(d, n)) for n in os.listdir(
            os.path.join(manage.VOA_DIR, d))]
    counter = Counter()
    for fname in files:
        with open(os.path.join(manage.VOA_DIR, fname), 'r') as f:
            text = _text_filter(f.read())
            counter.update(text.split())
    generate_words(counter)
#    task_queue = queue.Queue()
#    with open(manage.WORDS_PATH, 'r') as f:
#        words = ''.join(f)
#        for k, v in counter.items():
#            if k in words:
#                task_queue.put((k, v))
#    threads = []
#    for i in range(4):
#        t = MultiThreadUpdate(str(i), task_queue)
#        t.daemon = True
#        t.start()
#        threads.append(t)
#    for t in threads:
#        t.join()
#



if __name__ == '__main__':

    #generate_words()
    #run_crawler(4)
    stat_counts()
