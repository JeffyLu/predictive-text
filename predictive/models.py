from django.db import models


class Vocabulary(models.Model):

    word = models.CharField(max_length=32, unique=True)
    frequency = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.word, self.frequency)


class VocabularyRelation(models.Model):

    vocab_id = models.BigIntegerField(db_index=True)
    next_vocab_id = models.BigIntegerField()
    frequency = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    SHARDING_PIECE = 4

    def __str__(self):
        return '{} {}: {}'.format(self.vocab.word, self.next_vocab.word,
                                  self.frequency)

    class Meta:
        unique_together = ['vocab_id', 'next_vocab_id']
        abstract = True

    @property
    def vocab(self):
        vocab = Vocabulary.objects.filter(pk=self.vocab_id).first()
        return vocab.word if vocab else ''

    @property
    def next_vocab(self):
        vocab = Vocabulary.objects.filter(pk=self.next_vocab_id).first()
        return vocab.word if vocab else ''

    @classmethod
    def get_sharding_model(cls, sharding_key):
        piece = sharding_key % cls.SHARDING_PIECE
        class Meta:
            db_table = 'predictive_vocabularyrelation_{}'.format(piece)
            unique_together = ['vocab_id', 'next_vocab_id']
        attrs = {'__module__': cls.__module__, 'Meta': Meta}
        return type('VocabularyRelation_{}'.format(piece), (cls, ), attrs)


for i in range(VocabularyRelation.SHARDING_PIECE):
    VocabularyRelation.get_sharding_model(i)
