import re
import nltk
from django.db.models import F
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
            words = re.findall(r'[0-9a-zA-Z\']+', sent)
            relations = [(words[w-1], words[w]) for w in range(1, len(words))]
            yield words, relations

    def handle(self, *args, **options):
        task_num = options.get('articles', 100)
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
            try:
                vocab = Vocabulary.objects.get(word=k)
                vocab.frequency = F('frequency') + v
                vocab.save()
                vocab_id_dict[k] = vocab.pk
            except Vocabulary.DoesNotExist:
                continue
        for k, v in vocab_relation_counter.items():
            vocab_id = vocab_id_dict.get(k[0])
            next_vocab_id = vocab_id_dict.get(k[1])
            if not all([vocab_id, next_vocab_id]):
                continue
            model = VocabularyRelation.get_sharding_model(vocab_id)
            model.objects.update_or_create(
                vocab_id=vocab_id, next_vocab_id=next_vocab_id,
                defaults={'frequency': v})

        print('tasks: {}, vocabs: {}, relations: {}'.format(
            task_num, len(vocab_counter), len(vocab_relation_counter)))

