import re
import nltk
from django.core.cache import cache
from predictive.cache_keys import key_of_vocabulary, key_of_relation
from collections import Counter
from django.core.management.base import BaseCommand
from resource_collector.models import Article
from predictive.models import Vocabulary, VocabularyRelation


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-a', '--articles', dest='articles', type=int)

    def analyze(self, article_content):
        sents = nltk.sent_tokenize(article_content)
        for sent in sents:
            sent = sent.lower()
            words = re.findall(r'[0-9a-zA-Z\']+', sent)
            relations = [(words[w-1], words[w]) for w in range(1, len(words))]
            yield words, relations

    def handle(self, *args, **options):
        task_num = options.get('articles') or 100
        vocab_counter = Counter()
        vocab_relation_counter = Counter()
        articles = Article.objects.filter(is_used=False)[:task_num]
        for article in articles:
            for words, relations in self.analyze(article.article_content):
                vocab_counter.update(words)
                vocab_relation_counter.update(relations)
            article.is_used = True
            article.save()

        vocab_id_dict = {}
        for k, v in vocab_counter.items():
            key = key_of_vocabulary(k)
            vocab = cache.get(key)
            if not vocab:
                try:
                    vocab = Vocabulary.objects.get(word=k)
                except Vocabulary.DoesNotExist:
                    continue
            vocab.frequency = vocab.frequency + v
            vocab.save()
            cache.set(key, vocab)
            vocab_id_dict[k] = vocab.pk

        for k, v in vocab_relation_counter.items():
            vocab_id = vocab_id_dict.get(k[0])
            next_vocab_id = vocab_id_dict.get(k[1])
            if not all([vocab_id, next_vocab_id]):
                continue
            key = key_of_relation(vocab_id, next_vocab_id)
            relation = cache.get(key)
            if not relation:
                model = VocabularyRelation.get_sharding_model(vocab_id)
                relation, _ = model.objects.update_or_create(
                    vocab_id=vocab_id, next_vocab_id=next_vocab_id,
                    defaults={'frequency': v})
            else:
                relation.frequency = relation.frequency + v
                relation.save()
            cache.set(key, relation)

        print('tasks: {}, vocabs: {}, relations: {}'.format(
            task_num, len(vocab_counter), len(vocab_relation_counter)))
