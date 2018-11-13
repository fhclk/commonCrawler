# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import SinglePageItem, OrderlyListItem, DisorderedListItem, RulesGetContentItem

import pymongo

from bs4 import BeautifulSoup
import os.path

class BigspiderPipeline(object):

    single_page_collection_name = "single_page"
    orderly_list_collection_name = "orderly_list"
    disordered_list_collection_name = "disordered_list"
    rules_content_collection_name = "rules_content"

    def __init__(self, mongo_uri, mongo_port, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        pass


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        upload = spider.conf.get('upload_image', False)
        if upload:
            request_url = upload.get('request_url','')
            params = upload.get('params',{})
            self.upload_image(request_url, params)
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, SinglePageItem):
            replace_img_src = spider.conf.get('replace_img_src', False)
            if replace_img_src:
                base_server_path = replace_img_src.get('base_server_path','')
                self.replace_img_src_of_server_path(item, base_server_path, crawl_no=spider.crawl_no)
            else:
                self.replace_img_src(item)
            self.db[self.single_page_collection_name].insert(dict(item))
        if isinstance(item, OrderlyListItem):
            self.db[self.orderly_list_collection_name].insert(dict(item))
        if isinstance(item, DisorderedListItem):
            self.db[self.disordered_list_collection_name].insert(dict(item))
        if isinstance(item, RulesGetContentItem):
            self.db[self.rules_content_collection_name].insert(dict(item))
        return item

    def replace_img_src(self, item):
        '''
        替换content中img标签的src属性值，替换成原待爬取网站的完整路径
        :param item: 
        :return: 
        '''
        if 'content' in item:
            item_content = item['content']
            item_select = BeautifulSoup(item_content)
            img_selects = item_select.find_all('img')
            image_urls = item._values.get('image_urls',[])
            o_image_urls = item._values.get('o_image_urls',[])
            if len(image_urls) > 0:
                for img_sel in img_selects:
                    if img_sel['src'] in o_image_urls:
                        index = o_image_urls.index(img_sel['src'])
                        if index > -1 and index < len(image_urls):
                            img_sel['src'] = image_urls[index]
                item._values['content'] = str(item_select)

    def replace_img_src_of_server_path(self, item, base_server_path, crawl_no):
        '''
        替换content中img标签的src属性值，替换成服务器上的相对路径
        :param item: 存储爬取内容的item
        :param base_server_path: 服务器上存放
        :param crawl_no: 
        :return: 
        '''
        if 'content' in item:
            item_content = item['content']
            item_select = BeautifulSoup(item_content)
            img_selects = item_select.find_all('img')
            image_urls = item._values.get('image_urls',[])
            o_image_urls = item._values.get('o_image_urls',[])
            if len(image_urls) > 0 and len(image_urls) == len(o_image_urls):
                for img_sel in img_selects:
                    if img_sel['src'] in o_image_urls:
                        index = o_image_urls.index(img_sel['src'])
                        download_imge = self.db['download_images'].find_one(
                            {'url': image_urls[index],'crawl_no':crawl_no})
                        path = download_imge.get('path', '')
                        if path:
                            img_sel['src'] = os.path.join(base_server_path, path.split('/')[-1])
                item._values['content'] = str(item_select)

    def upload_image(self, request_url, params):
        '''
        上传图片
        :param request_url: 接口url
        :param params: 接口参数
        :return: 
        '''
        pass




import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from copy import deepcopy

class ImageDownloadPipeline(ImagesPipeline):
    client = None
    db = None
    server_image_path = None
    download_image_collection_name = "download_images"

    def __init__(self, store_uri, download_func=None, settings=None):
        super(ImageDownloadPipeline, self).__init__(store_uri, settings=settings,
                                             download_func=download_func)

    def __del__(self):
        if self.client:
            self.client.close()

    def get_media_requests(self, item, info):
        if isinstance(item, SinglePageItem):
            for image_url in item.get('image_urls', []):
                yield scrapy.Request(image_url)
        pass

    def item_completed(self, results, item, info):
        if isinstance(item, SinglePageItem) and 'image_urls' in item:
            image_paths = [x['path'] for ok, x in results if ok]
            if self.IMAGES_RESULT_FIELD in item.fields:
                if not image_paths:
                    raise DropItem("Item contains no images")
            for ok, x in results:
                if ok:
                    item_dict = deepcopy(x)
                    item_dict['crawl_no'] = item.get('crawl_no', '')
                    self.db[self.download_image_collection_name].insert(item_dict)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        try:
            pipe = cls.from_settings(crawler.settings)
        except AttributeError:
            pipe = cls()
        pipe.crawler = crawler

        mongo_uri = crawler.settings.get('MONGO_URI'),
        mongo_port = crawler.settings.get('MONGO_PORT', 27017),
        mongo_db = crawler.settings.get('MONGO_DATABASE', 'items')
        mongo_port = mongo_port[0] if isinstance(mongo_port, tuple) else mongo_port

        pipe.client = pymongo.MongoClient(mongo_uri, mongo_port)
        pipe.db = pipe.client[mongo_db]
        return pipe

