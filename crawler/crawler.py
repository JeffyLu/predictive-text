#coding:utf-8

import re
import os
import queue
import random
import requests
import threading
from crawler.user_agent import agents
from manage import VOA_DIR


class VOACrawler:

    def __init__(self):
        self.url_root = "http://www.51voa.com"
        self.url_standard = self.url_root + "/VOA_Standard_%s_archiver.html"

    def _get_response(self, url):
        headers = {
            "User-Agent": random.choice(agents),
        }
        try:
            resp = requests.get(url, headers = headers)
        except:
            try:
                resp = requests.get(url, headers = headers)
            except:
                raise Exception(" * timeout!")
        resp.encoding = "utf-8"
        return resp.text

    def _data_parser(self, resp, _type):
        if _type == 0:
            data = re.findall(
                r'href="(/VOA_Standard_English/[a-zA-Z0-9_-]*?.html)"',
                resp,
                re.S,
            )
        elif _type == 1:
            data = ''.join(re.findall(
                r'<div id="content">(.*?)<div id="Bottom_VOA">',
                resp,
                re.S,
            ))
            data = re.sub(r'<.*?>', ' ', data, flags = re.S)
        else:
            raise Exception(" * unknown task type!")
        return data

    def get_data(self, task, _type):
        if _type == 0:
            url = self.url_standard % task
        elif _type == 1:
            url = self.url_root + task
        else:
            raise Exception(" * unknown task type!")
        resp = self._get_response(url)
        return self._data_parser(resp, _type)


class MultiThreadCrawler(threading.Thread):

    def __init__(self, name, task_queue):
        threading.Thread.__init__(self, name = name)
        self.task_queue = task_queue
        self.crawler = VOACrawler()

    def run(self):
        cnt = 1
        while not self.task_queue.empty():
            task, _type = self.task_queue.get()
            try:
                data = self.crawler.get_data(task, _type)
                self.task_queue.task_done()
            except Exception as e:
                print("[ERROR] %s" % e)
                return False
            if _type == 0:
                [self.task_queue.put((i, 1)) for i in data]
                print("[SUCCESS] t%s: found %s news in page %s" % (
                    self.getName(), len(data), task))
            else:
                _dir = os.path.join(VOA_DIR, self.getName()+str(cnt//1000))
                if not os.path.exists(_dir):
                    os.makedirs(_dir)
                filename = os.path.join(_dir, task.split('/')[-1][:-5])
                with open(filename, 'w+') as f:
                    f.write(data)
                cnt += 1
                print("-"*20, cnt)
                print("[SUCCESS] t%s: saved %s" % (self.getName(), task))


def get_task_queue():
    resp = requests.get("http://www.51voa.com/VOA_Standard_1_archiver.html")
    resp.encoding = 'utf-8'
    page = re.search(r'页次：<b>\d+</b>/<b>(\d+)</b> 每页', resp.text, re.S)
    task_queue = queue.Queue()
    [task_queue.put((i, 0)) for i in range(int(page.groups()[0]))]
    return task_queue

def run_crawler(cpu = 1):
    try:
        task_queue = get_task_queue()
    except:
        raise Exception(" * faild to get tasks!")
    threads = []
    for i in range(cpu):
        t = MultiThreadCrawler(str(i), task_queue)
        t.daemon = True
        t.start()
        threads.append(t)
    for t in threads:
        t.join()



if __name__ == '__main__':

    #crawler = VOACrawler()
    #crawler.get_data(1, 0)
    #get_task_queue()
    print(0)

