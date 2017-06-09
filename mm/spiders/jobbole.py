# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request    # 从scrap上让Request工具帮忙进行下载
from urllib import parse  # 利用parse函数把url给join起来
from mm.items import JobBoleArticleItem    #把item给引进来
from mm.untils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains =  ["blog.jobbole.com"]
    start_urls =  ['http://blog.jobbole.com/all-posts/']

    def parse(self,response):


        post_nodes = response.css ( '#archive .floated-thumb .post-thumb a')   # 从网页提取文章的URL,交给scrapy下载，并传递给parse_detail解析
        for post_node in post_nodes:
            image_url= post_node.css("img::attr(src)").extract()[0]
            post_url = post_node.css ( "::attr(href)" ).extract_first ( "" )
            yield Request ( url=parse.urljoin ( response.url, post_url ),  meta={"front_image_url":image_url}, callback=self.parse_detail )
        # callback回调进入datail周期进行循环
        # yield是通过scrapy的Request()下载，并且交给自定义的parse_detail解析
        #不是完整的地址，urljoin有两个参数，主域名自动拼接不完整的域名，并from urllib import parse


        # 提取下一页并交给scrapy进行下载
        # next_url = response.css ( ".next.page-numbers::attr(href)" ).extract_first ( "" )
        # if next_url:
        #     yield Request ( url=parse.urljoin ( response.url, next_url ), callback=self.parse )



    def parse_detail(self, response):
        article_item=JobBoleArticleItem()

        front_image_url = response.meta.get ( "front_image_url", "" )
        title = response.css ( ".entry-header h1::text" ).extract ()[0]
        create_date=response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip()
        praise_nums=response.css(".vote-post-up h10::text").extract()[0]
        fav_nums=response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match ( ".*?(\d+).*", fav_nums )
        if match_re:
            fav_nums = int(match_re.group (1))
        else:
            fav_nums = 0

        comment_nums=response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group (1))
        else:
            comment_nums = 0
        content=response.css ( "div.entry" ).extract ()[0]
        tag_list=response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip ().endswith ( "评论" )]
        tags = ",".join ( tag_list )

        article_item["url_object_id"] = get_md5(response.url)
        article_item["title"] = title
        article_item["url"] = response.url

        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tags
        article_item["content"] = content

        yield article_item

