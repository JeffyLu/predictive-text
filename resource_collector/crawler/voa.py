import re
import queue
import random
import requests
import threading
from resource_collector.crawler.utils import user_agents, get_html
from resource_collector.crawler.multithread_crawler import MultiThreadCrawler


class VOACrawler:

    url_root = 'http://www.51voa.com'
    url_standard = url_root + "/VOA_Standard_{}_archiver.html"

    def __init__(self, retry=3, encoding='utf-8'):
        self.retry = retry
        self.encoding = encoding

    @property
    def headers(self):
        return {'User-Agent': random.choice(user_agents)}

    @property
    def standard_archiver_pages_task_queue(self):
        url = self.url_standard.format(1)
        html = get_html(url, retry=self.retry, headers=self.headers,
                        encoding=self.encoding)
        page = re.search(r'页次：<b>\d+</b>/<b>(\d+)</b> 每页',
                         html, re.S)
        task_queue = queue.Queue()
        [task_queue.put((i, MultiThreadCrawler.TASK_TYPE_ARCHIVER))
         for i in range(int(page.groups()[0]))]
        return task_queue

    @property
    def update_todays_article_queue(self):
        html = get_html(self.url_root, retry=self.retry, headers=self.headers,
                        encoding=self.encoding)
        urls = re.findall(
            r'href="(/VOA_Standard_English/[a-zA-Z0-9_-]*?.html)"', html, re.S)
        task_queue = queue.Queue()
        for url in urls:
            task_queue.put(
                (self.url_root + url, MultiThreadCrawler.TASK_TYPE_ARTICLE)
            )
        return task_queue

    def get_archiver_article_urls(self, page):
        url = self.url_standard.format(page)
        html = get_html(url, retry=self.retry, headers=self.headers,
                        encoding=self.encoding)
        urls = re.findall(
            r'href="(/VOA_Standard_English/[a-zA-Z0-9_-]*?.html)"', html, re.S)
        return [self.url_root + u for u in urls]

    def get_article_content_by_url(self, url):
        html = get_html(url, retry=self.retry, headers=self.headers,
                        encoding=self.encoding)
        contents = re.findall(r'<div id="content">(.*?)<div id="Bottom_VOA">',
                              html, re.S)
        return re.sub(r'<.*?>', ' ', ''.join(contents), flags=re.S)


def run_crawler(cpu=1, crawl_today=False):
    crawler = VOACrawler()
    if crawl_today:
        task_queue = crawler.update_todays_article_queue
    else:
        task_queue = crawler.standard_archiver_pages_task_queue
    threads = []
    for i in range(cpu):
        t = MultiThreadCrawler(crawler, task_queue)
        t.daemon = True
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
