# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest, HtmlResponse
import json
import pymongo
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest, SplashFormRequest

from ..util.common import getDomain, cleanHtmlTag, getConfigFromDB
from ..items import RulesGetContentItem


from .. import settings


class RegexLoginedSpider(CrawlSpider):
    name = 'regexLoginedSpider'
    allowed_domains = []
    start_urls = []

    settings.COOKIES_ENABLES = True

    post_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
        "Referer": "",
    }

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
        crawl_no = kwargs.get('crawlNo', '0')
        if 'config' in kwargs:
            config = kwargs['config']
        else:
            config = getConfigFromDB(crawler, task_no)
        spider = super(CrawlSpider, cls).from_crawler(crawler, conf=config, crawl_no=crawl_no, *args, **kwargs)
        spider._follow_links = crawler.settings.getbool(
            'CRAWLSPIDER_FOLLOW_LINKS', True)
        return spider

    def __init__(self, conf=None, crawl_no=None, *a, **kw):
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
        super(RegexLoginedSpider, self).__init__(*a, **kw)


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



    def start_requests(self):
        if 'login_url' in self.conf:
            yield Request(self.conf.get('login_url'), meta={'cookiejar': 1}, callback=self.post_login)

    def post_login(self, response):
        '''
        登录
        :param response: 登录页内容
        :return: 
        '''
        form_data = {}
        form_xpath = self.conf.get('form_xpath', '//form')
        forms = response.xpath(form_xpath)
        for form in forms:
            inputs = form.xpath('descendant::input')
            for input in inputs:
                name = input.xpath('@name').extract_first()
                value = input.xpath('@value').extract_first()
                type = input.xpath('@type').extract_first()
                if not name:
                    continue
                if type.lower() == 'text' or type.lower() == 'email':
                    form_data[name] = self.conf.get('login_account', '')
                elif type.lower() == 'password':
                    form_data[name] = self.conf.get('login_password', '')
                else:
                    form_data[name] = value

        url = self.conf.get('login_request_url', '')
        return [FormRequest.from_response(response,
                                          url=url,
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          headers=self.post_headers,
                                          formdata=form_data,
                                          callback=self.after_login,
                                          dont_filter=True,
                                          method='POST',
                                          formxpath=form_xpath
                                          )]


    def after_login(self, response):
        if 'start_url' in self.conf:
            start_urls = self.conf['start_url']
            start_urls = start_urls if isinstance(start_urls, list) else [start_urls]
            for url in start_urls:
                # yield Request(url, meta={'cookiejar': response.meta['cookiejar']})
                yield SplashRequest(url, meta={'cookiejar': response.meta['cookiejar']})


    def _requests_to_follow(self, response):
        """重写加入cookiejar的更新"""
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                # r = Request(url=link.url, callback=self._response_downloaded)
                r = SplashRequest(url=link.url, callback=self._response_downloaded)
                r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])
                yield rule.process_request(r)
