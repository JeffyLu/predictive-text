#coding: utf-8

import manage
import time
from db.models import Words, Relations

TOP = 5

def auto_complete_word():
    while True:
        alpha = input()
        if alpha.endswith(' '):
            break
        queryset = Words.objects.filter(
            value__startswith = alpha).order_by('-counts')[:TOP]
        print(queryset.query)
        results = ' '.join([q.__str__() for q in queryset])
        print(results)

def auto_predict_word():
    while True:
        word = input()
        if word.endswith('.'):
            break
        start = time.time()
        queryset = Relations.objects.filter(
            wid__value = word,
        ).order_by('-counts')[:TOP]
        print(queryset.query)
        results = ' '.join(['%s:%d' % (q.next_wid.value, q.counts) for q in queryset])
        print(results, time.time() - start)


if __name__ == '__main__':

    #auto_complete_word()
    auto_predict_word()
