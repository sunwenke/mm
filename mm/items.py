# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field ()
    create_date = scrapy.Field ()
    url = scrapy.Field ()
    url_object_id = scrapy.Field ()  # 让url的长度变成固定的长度
    front_image_url = scrapy.Field ()
    front_image_path = scrapy.Field ()  # 封面在本地存放的路径
    praise_nums = scrapy.Field ()
    comment_nums = scrapy.Field ()
    fav_nums = scrapy.Field ()
    tags = scrapy.Field ()
    content = scrapy.Field ()
    
