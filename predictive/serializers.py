from predictive.models import Vocabulary, VocabularyRelation
from rest_framework.serializers import ModelSerializer


class VocabularySerializer(ModelSerializer):

    class Meta:
        model = Vocabulary
        fields = ['word', 'frequency']


class PhraseSerializer(ModelSerializer):

    class Meta:
        model = VocabularyRelation.get_sharding_model(1)
        fields = ['word', 'next_word', 'frequency']
