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

    def __str__(self):
        return '{} {}: {}'.format(self.vocab.word, self.next_vocab.word,
                                  self.frequency)

    @property
    def vocab(self):
        vocab = Vocabulary.objects.filter(pk=self.vocab_id).first()
        return vocab.word if vocab else ''

    @property
    def next_vocab(self):
        vocab = Vocabulary.objects.filter(pk=self.next_vocab_id).first()
        return vocab.word if vocab else ''
