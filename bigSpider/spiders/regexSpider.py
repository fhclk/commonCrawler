# -*- coding: utf-8 -*-
import scrapy
import json
import pymongo
from scrapy.spiders import CrawlSpider, Rule
from  scrapy.linkextractors import LinkExtractor

from ..util.common import getDomain, getConfigFromDB, cleanHtmlTag
from ..items import RulesGetContentItem

from .. import settings


class RegexSpider(CrawlSpider):
    name = 'regexSpider'
    allowed_domains = []
    start_urls = []

    settings.COOKIES_ENABLES = False

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        '''
        重写父类方法，从配置文件获取连接数据库的参数
        :param crawler: 
        :param args: 
        :param kwargs: 
        :return: 
        '''
        task_no = kwargs.get("taskNo", "task")
        crawl_no = kwargs.get("crawlNo", '0')
        if 'config' in kwargs:
            config = kwargs['config']
        else:
            config = getConfigFromDB(crawler, task_no)
        spider = super(CrawlSpider, cls).from_crawler(crawler, conf=config, crawl_no=crawl_no, *args, **kwargs)
        spider._follow_links = crawler.settings.getbool(
            'CRAWLSPIDER_FOLLOW_LINKS', True)
        return spider

    def __init__(self, conf=None, crawl_no=None,*a, **kw):
        if isinstance(conf, str):
            self.conf = json.loads(conf)
        else:
            self.conf = conf
        self.crawl_no = crawl_no

        self.start_urls.append(self.conf.get('start_url',''))
        domain = getDomain(self.conf.get('start_url',''))
        if domain:
            self.allowed_domains.append(domain)

        rules = []
        if 'url_rules' in self.conf:
            for item in self.conf.get('url_rules', []):
                allows = None
                denys = None
                callBack = None
                if 'allow' in item:
                    allows = item.get('allow')
                    # allows = ["[0-9]*\.html?"]
                if 'deny' in item:
                    denys = item.get('deny')
                if 'need_parse' in item:
                    callBack = self.parse_item

                allows = tuple(allows) if allows and len(allows) > 0 else None
                denys = tuple(denys) if denys and len(denys) > 0 else None
                rule = Rule(LinkExtractor(allow=allows, deny=denys),
                            callback=callBack,
                            cb_kwargs={"columns":item.get('columns', None),"ord":item.get('ord',-1)}
                            )
                rules.append(rule)

        self.rules = tuple(rules)
        super(RegexSpider, self).__init__(*a, **kw)


    def parse_item(self, response, **cb_kwargs):
        '''
        回调方法，解析具体爬取到的网页内容
        :param response: 爬取到的网页内容
        :param cb_kwargs: 附带参数
        :return: 
        '''
        columns = cb_kwargs.get("columns", {})
        rules_item = RulesGetContentItem()
        rules_item["crawl_no"] = self.crawl_no
        rules_item["rule_id"] = cb_kwargs.get("ord", -1)
        rules_item._values['link'] = response.url
        for column in columns:
            xpath = column.get('selector', '')
            item_selector = response.xpath(xpath)

            item_content = item_selector.extract_first()
            if column.get('is_save_image', False):
                image_urls = item_selector.xpath('descendant::img/@src').extract()
                if image_urls:
                    rules_item._values['image_urls'] = [response.urljoin(url) for url in image_urls]
                    rules_item._values['o_image_urls'] = image_urls

            if column.get('isCleanHtmlTag', False):
                item_content = cleanHtmlTag(item_content)

            item_name = column.get('name', 'item_name')
            rules_item._values[item_name] = item_content
        return rules_item
