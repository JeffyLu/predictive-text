# predictive-text
###### 作者：[JeffyLu](https://jeffylu.github.io/)

- - -
##### 简介
&emsp;&emsp;基于概率的输入预测系统，可满足单词补全，词组预测等功能。
&emsp;&emsp;直接运行```main.py```，系统会先启动爬虫，爬取近十年的VOA新闻，接着生成词汇表和关系表。```test.py```是对两张表的简单应用，可根据需求自己定制功能。

##### 环境依赖
- requests
- django 1.10
- python 3
- mysql


* * *
###### 词汇表：[words350k.txt](https://github.com/dwyl/english-words/)