from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from predictive import cache_keys
from predictive.models import Vocabulary, VocabularyRelation
from collections import OrderedDict
from django.core.cache import cache


class PageNumberPaginationExt(PageNumberPagination):

    max_page_size = 20
    max_page = 20
    page_size_query_param = 'ipp'

    def paginate_queryset(self, queryset, request, view=None):
        queryset = queryset[:self.max_page_size * self.max_page]
        return super().paginate_queryset(queryset, request, view=None)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('ipp', self.get_page_size(self.request)),
            ('page', self.page.number),
            ('total', self.page.paginator.count),
            ('objects', data)
        ]))


MAX_SIZE_OF_QUERYSET = (PageNumberPaginationExt.max_page *
                        PageNumberPaginationExt.max_page_size)


def get_data(request):
    if request.method == 'GET':
        data = request.GET
    else:
        try:
            data = request.data
        except AttributeError:
            data = {}
    try:
        return data.dict()
    except AttributeError:
        return data


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_word_process_method(string):
    if not string:
        return None

    if string.istitle():
        _word_process_method = str.title
    elif string.isupper():
        _word_process_method = str.upper
    elif string[0].isupper():
        _word_process_method = str.title
    else:
        _word_process_method = None
    return _word_process_method


def get_phrase_queryset(word):
    if not word:
        return []
    key = cache_keys.key_of_phrase_queryset(word)
    queryset = cache.get(key)
    if not queryset:
        vocab = get_vocab_by_word(word)
        if vocab:
            model = VocabularyRelation.get_sharding_model(vocab.pk)
            queryset = list(model.objects.filter(vocab_id=vocab.pk))
        else:
            queryset = []
        cache.set(key, queryset[:MAX_SIZE_OF_QUERYSET])
    return queryset


def get_vocab_by_word(word):
    word = word.lower()
    key = cache_keys.key_of_vocabulary(word)
    vocab = cache.get(key)
    if not vocab:
        vocab = Vocabulary.objects.filter(word=word).first()
    return vocab
