# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest
import json
import pymongo
from ..util.common import getDomain, getConfigFromDB, cleanHtmlTag

from ..items import SinglePageItem, OrderlyListItem, DisorderedListItem

from .. import settings
from baseFunction import BaseFunctions



class UniversalProxySpider(scrapy.Spider, BaseFunctions):
    name = 'universalProxySpider'
    allowed_domains = []
    start_urls = []

    settings.COOKIES_ENABLES = False
    settings.DOWNLOAD_DELAY = 2
    # settings.DOWNLOADER_MIDDLEWARES['bigSpider.HttpProxyMiddleware.HttpProxyMiddleware'] = 999

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        '''
        重写父类方法，从配置文件获取连接数据库的参数
        :param crawler: 
        :param args: 
        :param kwargs: 
        :return: 
        '''
        task_no = kwargs.get("taskNo","task")
        crawl_no = kwargs.get('crawlNo', '0')
        if 'config' in kwargs:
            config = kwargs['config']
        else:
            config = getConfigFromDB(crawler, task_no)
        spider = cls(conf=config, crawl_no=crawl_no, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def __init__(self, conf=None, crawl_no=None, name=None, **kwargs):
        super(UniversalProxySpider, self).__init__(name, **kwargs)
        if isinstance(conf, str):
            self.conf = json.loads(conf)
        else:
            self.conf = conf
        self.crawl_no = crawl_no

        domain = getDomain(self.conf.get('start_url',''))
        if domain:
            self.allowed_domains.append(domain)

    def __del__(self):
        pass


    def start_requests(self):
        if 'start_url' in self.conf:
            # yield Request(self.conf.get('start_url'), callback=self.parse_start_url, meta={'change_proxy':True})
            yield SplashRequest(self.conf.get('start_url'), callback=self.parse_start_url)


    def parse_start_url(self, response):
        '''
        解析开始页
        :param response: 开始页内容
        :return:
        '''
        for itr in self.follow_factory(response, 0):
            yield itr


    def parse_single_page(self, response, follow):
        '''
        解析单个网页
        :param response: 爬虫爬取到的网页内容
        :param follow: 流程步骤
        :return: 
        '''
        if 'columns' in follow:
            single_page_item = SinglePageItem()
            single_page_item["crawl_no"] = self.crawl_no
            single_page_item['follow_ord'] = follow.get('ord', -1)
            single_page_item._values['link'] = response.url
            for column in follow.get('columns'):
                xpath = column.get('selector', '')
                item_selector = response.xpath(xpath)
                item_content = item_selector.extract_first()
                if column.get('is_save_image', False):
                    image_urls = item_selector.xpath('descendant::img/@src').extract()
                    if image_urls:
                        single_page_item._values['image_urls'] = [response.urljoin(url) for url in image_urls]
                        single_page_item._values['o_image_urls'] = image_urls

                if column.get('isCleanHtmlTag', False):
                    item_content = cleanHtmlTag(item_content)

                item_name = column.get('name', 'item_name')
                single_page_item._values[item_name] = item_content
                # single_page_item._values['user-agent'] = response.request.headers['User_Agent']
            yield single_page_item

        if follow.get('has_next_page', False):
            for itr in self.follow_factory(response, follow.get('next_page_ord', -1)):
                yield itr


    def parse_orderly_list1(self, response, follow):
        '''
        解析有序列表
        :param response: 
        :param follow: 
        :return: 
        '''
        xpath1 = follow.get('selector1', '')
        xpath2 = follow.get('selector2', '')
        same_xpath = self.get_same_xpath(xpath1, xpath2)
        sel_list = response.xpath(same_xpath) if same_xpath else []
        for sel in sel_list:
            link = None
            enable_open = True
            if 'link_selector' in follow:
                link_xpath = self.get_subitem_xpath(follow.get('link_selector',''), same_xpath)
                if not link_xpath.lower().endswith('/@href'):
                    link_xpath += '/@href'
                link = sel.xpath(link_xpath).extract_first()

            if 'columns' in follow:
                orderly_list_item = OrderlyListItem()
                orderly_list_item["crawl_no"] = self.crawl_no
                orderly_list_item['follow_ord'] = follow.get('ord', -1)
                orderly_list_item._values['link'] = response.url
                orderly_list_item._values['item_link'] = response.urljoin(link)
                for column in follow.get('columns'):
                    item_xpath = self.get_subitem_xpath(column.get('selector',''), same_xpath)
                    item_selector = sel.xpath(item_xpath)
                    item_text = item_selector.xpath('text()').extract_first()
                    if item_text:
                        item_content = item_text
                    else:
                        item_content = item_selector.extract_first()
                    if not item_content:
                        pass
                    item_name = column.get('name','item_name')
                    orderly_list_item._values[item_name] = item_content

                    # 根据判断条件判断是否允许爬取
                    if "condition" in column:
                        enable_open = self.enable_open_sub_page(column.get('condition'), item_content)
                if not enable_open:
                    continue  # 如果根据当前字段判断不能爬取则直接进入下一个

                yield orderly_list_item

            if ('link_selector' in follow) and link:
                yield SplashRequest(response.urljoin(link),
                                    callback=self.common_parse,
                                    meta={'follow_ord': follow.get('next_follow_ord',-1)}
                                    )

        if follow.get('has_next_page', False):
            for itr in self.follow_factory(response, follow.get('next_page_ord', -1)):
                yield itr



    def parse_disordered_list(self, response, follow):
        '''
        解析无序列表
        :param response:
        :param follow:
        :return:
        '''
        if 'list' in follow:
            for single_pattern in follow['list']:
                xpath = single_pattern.get('link_selector', '')
                sel_list = response.xpath(xpath)
                for sel in sel_list:
                    link = None
                    if 'link_selector' in single_pattern:
                        link_xpath = single_pattern.get('link_selector', '')
                        if not link_xpath.lower().endswith('/@href'):
                            link_xpath += '/@href'
                        link = sel.xpath(link_xpath).extract_first()

                    if 'columns' in single_pattern:
                        disordered_list_item = DisorderedListItem()
                        disordered_list_item["crawl_no"] = self.crawl_no
                        disordered_list_item['follow_ord'] = follow.get('ord', -1)
                        disordered_list_item._values['link'] = response.url
                        disordered_list_item._values['item_link'] = response.urljoin(link)
                        for column in single_pattern.get('columns'):
                            item_xpath = column.get('selector', '')
                            item_selector = sel.xpath(item_xpath)
                            item_text = item_selector.xpath('text()').extract_first()
                            if item_text:
                                item_content = item_text
                            else:
                                item_content = item_selector.extract_first()
                            item_name = column.get('name', 'item_name')
                            disordered_list_item._values[item_name] = item_content
                        yield disordered_list_item

                    if ('link_selector' in single_pattern) and link:
                        yield SplashRequest(response.urljoin(link),
                                            callback=self.common_parse,
                                            meta={'follow_ord': single_pattern.get('next_follow_ord', '-1')}
                                            )

        if follow.get('has_next_page', False):
            for itr in self.follow_factory(response, follow.get('next_page_ord', -1)):
                yield itr


    def parse_next_page(self, response, follow):
        '''
        解析下一页
        :param response:
        :param follow:
        :return:
        '''
        if "max_pages" in follow:
            max_pages = follow.get('max_pages', 0)
            if max_pages > 0 and self.page_count >= max_pages:
                return

        if 'link_selector' in follow:
            link_xpath = follow.get('link_selector', '')
            if not link_xpath.lower().endswith('/@href'):
                link_xpath += '/@href'
            link = response.xpath(link_xpath).extract_first()
            if link:
                yield SplashRequest(response.urljoin(link),
                                    callback=self.common_parse,
                                    meta={'follow_ord': follow.get('next_follow_ord',-1)}
                                    )

    def common_parse(self, response):
        '''
        通用解析down下来的网页内容
        :param response: 
        :return: 
        '''
        follow_ord = response.meta['follow_ord']
        for itr in self.follow_factory(response, int(follow_ord)):
            yield itr


    def follow_factory(self, response, index):
        '''
        根据编号获取流程步骤，并根据流程步骤的类型分别进行处理
        :param response: 爬虫down下来的内容
        :param index: 流程步骤编号
        :return: 
        '''
        follow = self.get_follow(index)
        if follow:
            type = follow.get('type', '')
            if type == 'single_page':
                for itr in self.parse_single_page(response, follow):
                    yield itr
            elif type == 'orderly_list':
                for itr in self.parse_orderly_list1(response, follow):
                    yield itr
            elif type == 'disordered_list':
                for itr in self.parse_disordered_list(response, follow):
                    yield itr
            elif type == 'next_page':
                for itr in self.parse_next_page(response, follow):
                    yield itr


    def get_follow(self, index):
        '''
        根据编号从配置中获取流程步骤
        :param index: 配置文件中的流程步骤的编号
        :return: 配置文件中对应编号的流程步骤
        '''
        if 'follows' in self.conf:
            follows = self.conf['follows']
            for follow in follows:
                if int(follow.get('ord', -2)) == index:
                    return follow
        return None


