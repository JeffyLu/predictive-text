#coding:utf-8

import os
import gc
import manage
import time
import queue
import threading
from collections import Counter
from db.models import Words, Relations
from django.db import transaction
from crawler.crawler import run_crawler


WORD = 0
SENTENCE = 1
THREAD = 4

def _text_filter(text, _type):
    symbols = ['\n', '\t', '.', '"', '?', '&nbsp;', ',', '&amp;', '(', ')',
               '[', ']', '--', '---', '…', '/', '‘', ';', ':', '$', '%',
               '-', '!', '_']
    if _type == SENTENCE:
        [text.replace(i, '.') for i in ['!', '?', ':']]
        symbols.remove('.')
    for s in symbols:
        text = text.replace(s, ' ')
    return text.split() if _type == WORD else text.split('.')

def _get_files():
    _dirs = os.listdir(manage.VOA_DIR)
    files = []
    for d in _dirs:
        [files.append(os.path.join(d, n)) for n in os.listdir(
            os.path.join(manage.VOA_DIR, d))]
    return files

def _text_generator(_type):
    files = _get_files()
    fcnt = 0
    for fname in files:
        fcnt += 1
        print(fcnt, fname)
        with open(os.path.join(manage.VOA_DIR, fname), 'r') as f:
            text = _text_filter(f.read(), _type)
            yield fcnt, text

def _get_words_set():
    with open(manage.WORDS_PATH, 'r') as f:
        words = set(word.strip() for word in f)
        return words


@transaction.atomic
def generate_words(init = None):
    with open(manage.WORDS_PATH, 'r') as f:
        word_list = []
        words = set(word.strip() for word in f)
        print(' * generate words!')
        for word in words:
            if len(word) > 25 or len(word) < 1:
                continue
            if init and word in init:
                word_list.append(
                    Words(value = word.strip(), counts = init[word])
                )
                #Words.objects.create(value = word.strip(), counts = init[word])
            else:
                word_list.append(
                    Words(value = word.strip())
                )
                #Words.objects.create(value = word.strip())
        print(' * insert into database!')
        Words.objects.bulk_create(word_list)
        print(' * done!')


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


def stat_counts(init = False):
    counter = Counter()
    for fcnt, text in _text_generator(WORD):
        counter.update(text)
    if init:
        generate_words(counter)
        return
    task_queue = queue.Queue()
    words = _get_words_set()
    for k, v in counter.items():
        if k in words:
            task_queue.put((k, v))
    threads = []
    for i in range(THREAD):
        t = MultiThreadUpdate(str(i), task_queue)
        t.daemon = True
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


@transaction.atomic
def stat_relations():
    stat_list = []
    for fcnt, text in _text_generator(SENTENCE):
        for sentence in text:
            words = sentence.split()
            if len(words) < 1:
                continue
            for i, w in enumerate(words[:-1]):
                stat_list.append((w, words[i+1]))
    counter = Counter(stat_list)
    del stat_list
    ccnt = 1
    words = _get_words_set()
    for k, v in counter.items():
        if k[0] in words and k[1] in words:
            try:
                wid = Words.objects.get(value = k[0])
                next_wid = Words.objects.get(value = k[1])
                Relations.objects.create(
                    wid = wid,
                    next_wid = next_wid,
                    counts = v,
                )
            except:
                pass
        if ccnt % 10000 == 0:
            print(ccnt, len(counter))
        ccnt += 1
    del counter
    print('done')

if __name__ == '__main__':

    #generate_words()
    run_crawler(4)
    stat_counts()
    stat_relations()
