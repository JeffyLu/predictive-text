from django.core.cache import cache
from predictive import cache_keys
from predictive import utils as u
from predictive import serializers as s
from predictive.models import Vocabulary, VocabularyRelation

from rest_framework import viewsets, status
from rest_framework.response import Response


class VocabularyViewSet(viewsets.ModelViewSet):

    serializer_class = s.VocabularySerializer

    def list(self, request):
        data = u.get_data(request)
        prefix = data.get('prefix', '')
        _word_process_method = u.get_word_process_method(prefix)
        key = cache_keys.key_of_vocabulary_queryset(prefix)
        self.queryset = cache.get(key)
        if not self.queryset:
            self.queryset = list(Vocabulary.objects.filter(
                word__startswith=prefix.lower())[:u.MAX_SIZE_OF_QUERYSET])
            cache.set(key, self.queryset)

        if not data.get('user_mode') == '1':
            resp = super().list(request)
            if _word_process_method:
                for obj in resp.data['objects']:
                    obj['word'] = _word_process_method(obj['word'])
            return resp

        user_vocab_key = cache_keys.key_of_user_vocabulary(u.get_ip(request))
        self.queryset = u.sort_queryset_by_lru_cache(self.queryset,
                                                     user_vocab_key)
        resp = super().list(request)
        if _word_process_method:
            for obj in resp.data['objects']:
                obj['word'] = _word_process_method(obj['word'])
        return resp

    def update(self, request, pk):
        pk = int(pk)
        vocab = Vocabulary.objects.filter(pk=pk).first()
        if not vocab:
            return Response(data={'detail': 'not found'},
                            status=status.HTTP_404_NOT_FOUND)
        ip = u.get_ip(request)
        key = cache_keys.key_of_user_vocabulary(ip)
        user_vocabs = cache.get(key, [])
        if pk in user_vocabs:
            user_vocabs.remove(pk)
        user_vocabs.append(pk)
        cache.set(key, user_vocabs[-100:])
        vocab.frequency = vocab.frequency + 5
        vocab.save()
        return Response(self.get_serializer(vocab).data)


class PhraseViewSet(viewsets.ModelViewSet):

    serializer_class = s.PhraseSerializer

    def list(self, request):
        data = u.get_data(request)
        word = data.get('word')
        self.queryset = u.get_phrase_queryset(word)
        if not data.get('user_mode') == '1':
            return super().list(request)

        user_relation_key = cache_keys.key_of_user_relation(u.get_ip(request))
        self.queryset = u.sort_queryset_by_lru_cache(self.queryset,
                                                     user_relation_key)
        return super().list(request)

    def update(self, request, pk):
        pk = int(pk)
        try:
            vocab_id = int(u.get_data(request).get('vocab_id'))
        except (TypeError, ValueError):
            return Response(data={'detail': 'invalid vocab_id'})

        model = VocabularyRelation.get_sharding_model(vocab_id)
        relation = model.objects.filter(pk=pk).first()
        if not relation:
            return Response(data={'detail': 'not found'},
                            status=status.HTTP_404_NOT_FOUND)
        ip = u.get_ip(request)
        key = cache_keys.key_of_user_relation(ip)
        user_relations = cache.get(key, [])
        if pk in user_relations:
            user_relations.remove(pk)
        user_relations.append(pk)
        cache.set(key, user_relations[-100:])
        relation.frequency = relation.frequency + 5
        relation.save()
        return Response(self.get_serializer(relation).data)
