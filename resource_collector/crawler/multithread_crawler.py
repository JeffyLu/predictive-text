import threading
from django.db.utils import InternalError
from hashlib import md5
from resource_collector.models import Article, ArticleContent


class MultiThreadCrawler(threading.Thread):

    TASK_TYPE_ARTICLE = 0
    TASK_TYPE_ARCHIVER = 1

    def __init__(self, crawler, task_queue):
        super(MultiThreadCrawler, self).__init__()
        self.task_queue = task_queue
        self.crawler = crawler
        self.error_task = set()

    def save_article(self, url, content):
        url_hash = md5(url.encode('utf-8')).hexdigest()
        try:
            article, _ = Article.objects.get_or_create(
                source_url_hash=url_hash, defaults={'source_url': url})
            ArticleContent.objects.update_or_create(
                article_id=article.pk, defaults={'content': content})
            return True
        except InternalError as e:
            print('db internal error: {}'.format(str(e)))
            if url_hash not in self.error_task:
                self.task_queue.put((url, self.TASK_TYPE_ARTICLE))
                self.error_task.add(url_hash)
            return False

    def run(self):
        while not self.task_queue.empty():
            task, task_type = self.task_queue.get()
            if task_type == self.TASK_TYPE_ARTICLE:
                content = self.crawler.get_article_content_by_url(task)
                if not self.save_article(task, content):
                    continue
            elif task_type == self.TASK_TYPE_ARCHIVER:
                urls = self.crawler.get_archiver_article_urls(task)
                for url in urls:
                    self.task_queue.put((url, self.TASK_TYPE_ARTICLE))

            print('remain: {}, task: {}'.format(self.task_queue.qsize(), task))
