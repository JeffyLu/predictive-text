#coding:utf-8

import os
import manage
import time
import queue
import threading
from collections import Counter
from db.models import Words, Relations, TopRelations
from django.db import transaction
from crawler.crawler import run_crawler


WORD = 0
SENTENCE = 1


def _text_filter(text, _type):
    symbols = ['\n', '\t', '.', '"', '?', '&nbsp;', ',', '&amp;', '(', ')',
               '[', ']', '--', '---', '…', '/', '‘', ';', ':', '$', '%',
               '-', '!', '_']
    if _type == SENTENCE:
        [text.replace(i, '.') for i in ['!', '?', ':']]
        symbols.remove('.')
    for s in symbols:
        text = text.replace(s, ' ')
    return text

def _get_files():
    _dirs = os.listdir(manage.VOA_DIR)
    files = []
    for d in _dirs:
        [files.append(os.path.join(d, n)) for n in os.listdir(
            os.path.join(manage.VOA_DIR, d))]
    return files

@transaction.atomic
def generate_words(init = None):
    with open(manage.WORDS_PATH, 'r') as f:
        cnt = 1
        for word in f:
            word = word.strip()
            if len(word) > 25:
                continue
            if init and word in init:
                Words.objects.create(value = word.strip(), counts = init[word])
            else:
                Words.objects.create(value = word.strip())
            print(cnt, word)
            cnt += 1


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
    files = _get_files()
    counter = Counter()
    cnt = 1
    for fname in files:
        with open(os.path.join(manage.VOA_DIR, fname), 'r') as f:
            print(cnt, 'loading %s...' % fname)
            text = _text_filter(f.read(), WORD)
            counter.update(text.split())
            cnt += 1
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

@transaction.atomic
def stat_relations():
    files = _get_files()
    stat_list = []
    for fname in files[:1]:
        with open(os.path.join(manage.VOA_DIR, fname), 'r') as f:
            text = _text_filter(f.read(), SENTENCE)
            print(text)
        for sentence in text.split('.'):
            words = sentence.split()
            if len(words) < 2:
                continue
            for i, w in enumerate(words[:-1]):
                try:
                    pw = Words.objects.get(value = w)
                    nw = Words.objects.get(value = words[i+1])
                    relation = Relations.objects.get(
                        wid = pw,
                        next_wid = nw,
                    )
                except:
                    if pw and nw:
                        relation = Relations.objects.create(
                        wid = pw,
                        next_wid = nw,
                        )
                    print(relation, pw, nw)
                    continue
                relation.counts += 1
                print(relation, pw, nw)

if __name__ == '__main__':

    #generate_words()
    #run_crawler(4)
    #stat_counts()
    stat_relations()
