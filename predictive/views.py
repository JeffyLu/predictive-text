from django.core.cache import cache
from predictive.cache_keys import (key_of_phrase_queryset,
                                   key_of_vocabulary_queryset)
from predictive import utils as u
from predictive import serializers as s
from predictive.models import Vocabulary, VocabularyRelation

from rest_framework import viewsets


class VocabularyViewSet(viewsets.ModelViewSet):

    queryset = Vocabulary.objects.all()
    serializer_class = s.VocabularySerializer

    def list(self, request):
        data = u.get_data(request)
        prefix = data.get('prefix', '')
        key = key_of_vocabulary_queryset(prefix)
        self.queryset = cache.get(key)
        if not self.queryset:
            self.queryset = Vocabulary.objects.filter(
                word__startswith=prefix)
            cache.set(key, self.queryset[:u.MAX_SIZE_OF_QUERYSET])
        return super().list(request)


class PhraseViewSet(viewsets.ModelViewSet):

    serializer_class = s.PhraseSerializer

    def list(self, request):
        data = u.get_data(request)
        word = data.get('word')
        key = key_of_phrase_queryset(word)
        self.queryset = cache.get(key)
        if self.queryset:
            return super().list(request)

        vocab = Vocabulary.objects.filter(word=word).first()
        if vocab:
            model = VocabularyRelation.get_sharding_model(vocab.pk)
            self.queryset = list(model.objects.filter(vocab_id=vocab.pk))
        else:
            self.queryset = []

        cache.set(key, self.queryset[:u.MAX_SIZE_OF_QUERYSET])
        return super().list(request)
