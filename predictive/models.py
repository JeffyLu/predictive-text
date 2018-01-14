from django.db import models


class Vocabulary(models.Model):

    word = models.CharField(max_length=32, unique=True)
    frequency = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.word, self.frequency)

    class Meta:
        ordering = ['-frequency', 'word']


class VocabularyRelation(models.Model):

    vocab_id = models.BigIntegerField()
    next_vocab_id = models.BigIntegerField()
    frequency = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    SHARDING_PIECE = 4
    SHARDING_MODEL = {}

    def __str__(self):
        return '{} {}: {}'.format(self.vocab, self.next_vocab, self.frequency)

    class Meta:
        unique_together = ['vocab_id', 'next_vocab_id']
        ordering = ['-frequency']
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
            ordering = ['-frequency']
        attrs = {'__module__': cls.__module__, 'Meta': Meta}
        class_name = 'VocabularyRelation_{}'.format(piece)
        if class_name not in cls.SHARDING_MODEL:
            cls.SHARDING_MODEL[class_name] = type(class_name, (cls, ), attrs)
        return cls.SHARDING_MODEL[class_name]


for i in range(VocabularyRelation.SHARDING_PIECE):
    VocabularyRelation.get_sharding_model(i)
