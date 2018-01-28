from predictive import utils as u
from predictive import serializers as s
from predictive.models import Vocabulary, VocabularyRelation

from rest_framework import viewsets


class VocabularyViewSet(viewsets.ModelViewSet):

    queryset = Vocabulary.objects.all()
    serializer_class = s.VocabularySerializer

    def list(self, request):
        data = u.get_data(request)
        self.queryset = Vocabulary.objects.filter(
            word__startswith=data.get('prefix', ''))
        return super().list(request)


class PhraseViewSet(viewsets.ModelViewSet):

    serializer_class = s.PhraseSerializer

    def list(self, request):
        data = u.get_data(request)
        vocab = Vocabulary.objects.filter(word=data.get('word')).first()
        if vocab:
            model = VocabularyRelation.get_sharding_model(vocab.pk)
            self.queryset = model.objects.filter(vocab_id=vocab.pk)
        else:
            self.queryset = []
        return super().list(request)
