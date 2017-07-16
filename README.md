# predictive-text
###### 作者：[JeffyLu](https://jeffylu.github.io/)

- - -

##### 环境依赖
- requests
- django 1.10
- python 3
- mysql

##### 说明
&emsp;&emsp;利用爬虫爬取英文文章，经过分析处理后将生成词汇表和关系表用于实现单词补全，单词输入预测等功能。         
&emsp;&emsp;直接运行```main.py```，系统会先启动爬虫，接着经过一段时间的分析处理生成词汇表和关系表。```test.py```是对两张表的简单应用，可根据需求自己定制功能。           
&emsp;&emsp;朋友基于这两张表用java写了个简单的写作助手，可参考[这里](demo)。    


* * *
###### 词汇来源：[words350k.txt](https://github.com/dwyl/english-words/)
