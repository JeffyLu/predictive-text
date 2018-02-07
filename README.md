# predictive-text

- - -

##### 环境依赖
- MySQL
- Redis
- Python3


##### 使用方法
在[settings.py](predictive_text/settings.py)中修改数据库和缓存的配置信息，然后装pip包。
```
$ pip3 install -r requirements.txt
```

下载英文词汇[words.txt](https://github.com/dwyl/english-words/blob/master/words.txt)并初始化数据。
```
$ python3 manage.py migrate
$ python3 manage.py init_data -c [num of cup]
$ python3 manage.py import_vocabulary -f [path to words.txt]
```

注册定时任务，两个任务分别用来更新每日新闻和分析一定数量的文章，从而提高补全或提示的准确性。
```
$ python3 manage.py crontab add
```

运行。
```
$ python3 manage.py runserver
```


##### API文档
[文档](api.apib)是基于APIBlueprint语法写的，可以使用[aglio](https://github.com/danielgtaylor/aglio)来渲染。
```
$ aglio -i api.apib -s
```
访问```localhost:3000```效果如下：
![效果](https://user-images.githubusercontent.com/16357973/35916588-d39062ee-0c45-11e8-9d1c-1d87936e73be.png)


##### TODO
- [ ] 增加前端界面