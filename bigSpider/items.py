# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BigspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    crawl_no = scrapy.Field()  #任务编号
    pass

class SinglePageItem(BigspiderItem):
    follow_ord = scrapy.Field()
    pass

class OrderlyListItem(BigspiderItem):
    follow_ord = scrapy.Field()
    pass

class DisorderedListItem(BigspiderItem):
    follow_ord = scrapy.Field()
    pass

class RulesGetContentItem(BigspiderItem):
    '''
    用规则爬取内容时，爬取到的内容
    '''
    rule_id = scrapy.Field()   #规则id
    pass

