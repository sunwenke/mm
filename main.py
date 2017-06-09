from scrapy.cmdline import execute
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))#自动的导入article_spide的路径，不会换台电脑就废了
execute(["scrapy","crawl","jobbole"])#cmd命令中输入scrapy crawl jobbole,启动一个数组的三个字符