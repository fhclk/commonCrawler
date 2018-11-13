#!/usr/bin/env python
#-*-coding:utf-8-*-

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from bigSpider.spiders.universalSpider import UniversalSpider
from bigSpider.spiders.regexSpider import RegexSpider
from bigSpider.spiders.universalLoginedSpider import UniversalLoginedSpider
from bigSpider.spiders.regexLoginedSpider import RegexLoginedSpider
from bigSpider.spiders.universalProxySpider import UniversalProxySpider
from bigSpider.spiders.universalSplashSpider import UniversalSplashSpider
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

# configure_logging({'LOG_FORMAT':'%(levelname)s:%(message)s'})
# runner = CrawlerRunner()
#
# d = runner.crawl(CommonSpider)
# d.addBoth(lambda _: reactor.stop())
# reactor.run()


#conf='{"start_url":"https://www.yidaiyilu.gov.cn/","follows":[{"ord":0,"type":"orderly_list","selector1":"","selector2":"","link_selector":"","columns":[{"selector":"","name":"","disable":""},{"selector":"","name":"","disable":""}]},{"ord":1,"type":"next_page","link_selector":""},{"ord":2,"type":"disordered_list","list":[{"selector1":"","selector2":"","link_selector":"","columns":[{"selector":"","name":"","disable":""},{"selector":"","name":"","disable":""}]}]},{"ord":3,"type":"single_page","columns":[{"selector":"","name":"","disable":""},{"selector":"","name":"","disable":""}]}]}'
#conf1='{"start_url":"https://www.yidaiyilu.gov.cn/","follows":[{"ord":0,"type":"orderly_list","selector1":"","selector2":"","link_selector":"","next_follow_ord":2,"columns":[{"selector":"","name":"","disable":""},{"selector":"","name":"","disable":""}]},{"ord":1,"type":"next_page","next_follow_ord":2,"link_selector":""},{"ord":2,"type":"disordered_list","list":[{"selector":"","next_follow_ord":3,"link_selector":"","columns":[{"selector":"","name":"","disable":""},{"selector":"","name":"","disable":""}]}]},{"ord":3,"type":"single_page","columns":[{"selector":"","name":"","disable":""},{"selector":"","name":"","disable":""}]}]}'
#conf2='{"start_url":"https://www.yidaiyilu.gov.cn/","follows":[{"ord":0,"type":"orderly_list","selector1":"","selector2":"","link_selector":"","next_follow_ord":2,"has_next_page":false,"next_page_ord":0,"columns":[{"selector":"","name":"","disable":""},{"selector":"","name":"","disable":""}]},{"ord":1,"type":"next_page","next_follow_ord":2,"link_selector":""},{"ord":2,"type":"disordered_list","has_next_page":false,"next_page_ord":0,"list":[{"selector":"","next_follow_ord":3,"link_selector":"","columns":[{"selector":"","name":"","disable":""},{"selector":"","name":"","disable":""}]}]},{"ord":3,"type":"single_page","has_next_page":false,"next_page_ord":0,"columns":[{"selector":"","name":"","disable":""},{"selector":"","name":"","disable":""}]}]}'
single_page = """{
    "start_url": "https://www.yidaiyilu.gov.cn/",
    "follows": [
        {
            "ord": 0,
            "type": "single_page",
            "columns": [
                {
                    "selector": "/html/body/div[@class='mainBox1180'][3]/div[@class='main-1 left wtfz']/div[@class='con_wtfz_1']/ul[@class='commonList_dot']/li[4]/a",
                    "name": "test1",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='main-1 left']/div[@class='con_yw_1']/ul[@class='commonList_dot']/li[7]/a",
                    "name": "test2",
                    "disable": ""
                }
            ]
        }
    ]
}"""

orderly_list = """{
    "start_url": "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10149",
    "follows": [
        {
            "ord": 0,
            "type": "orderly_list",
            "next_follow_ord": 1,
            "selector1": "/html/body/div[@class='mainBox1180'][2]/div[@class='list_out wtfz_list_out']/div[@class='list_right left']/ul[@class='commonList_dot']/li[1]",
            "selector2": "/html/body/div[@class='mainBox1180'][2]/div[@class='list_out wtfz_list_out']/div[@class='list_right left']/ul[@class='commonList_dot']/li[2]",
            "link_selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='list_out wtfz_list_out']/div[@class='list_right left']/ul[@class='commonList_dot']/li[1]/a",
            "columns": [
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='list_out wtfz_list_out']/div[@class='list_right left']/ul[@class='commonList_dot']/li[1]/a",
                    "name": "test1",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='list_out wtfz_list_out']/div[@class='list_right left']/ul[@class='commonList_dot']/li[1]/span",
                    "name": "test2",
                    "disable": ""
                }
            ]
        },
        
        {
            "ord": 1,
            "type": "single_page",
            "columns": [
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@id='zoom']/h1[@class='main_content_title']",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@id='zoom']/div[1]/div[@class='szty']/span[@class='main_content_date'][2]",
                    "name": "from",
                    "disable": ""
                }
            ]
        }
    ]
}
"""

disordered_list = """
{
    "start_url": "https://www.yidaiyilu.gov.cn/",
    "follows": [
        {
            "ord": 0,
            "type": "disordered_list",
            "list": [
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='main-1 left']/div[@class='con_yw_1']/ul[@class='commonList_dot']/li[4]",
                    "next_follow_ord": 1,
                    "link_selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='main-1 left']/div[@class='con_yw_1']/ul[@class='commonList_dot']/li[4]/a",
                    "columns": [
                        {
                            "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='main-1 left']/div[@class='con_yw_1']/ul[@class='commonList_dot']/li[4]/a",
                            "name": "title",
                            "disable": ""
                        },
                        {
                            "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='main-1 left']/div[@class='con_yw_1']/ul[@class='commonList_dot']/li[4]/span",
                            "name": "date",
                            "disable": ""
                        }
                    ]
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180'][3]/div[@class='main-1 left wtfz']/div[@class='con_wtfz_4']/ul[@class='commonList_dot']/li[4]",
                    "next_follow_ord": 1,
                    "link_selector": "/html/body/div[@class='mainBox1180'][3]/div[@class='main-1 left wtfz']/div[@class='con_wtfz_4']/ul[@class='commonList_dot']/li[4]/a",
                    "columns": [
                        {
                            "selector": "/html/body/div[@class='mainBox1180'][3]/div[@class='main-1 left wtfz']/div[@class='con_wtfz_4']/ul[@class='commonList_dot']/li[4]/a",
                            "name": "title",
                            "disable": ""
                        }
                    ]
                }
            ]
        },
        {
            "ord": 1,
            "type": "single_page",
            "columns": [
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@id='zoom']/h1[@class='main_content_title']",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@id='zoom']/div[1]/div[@class=' szty']/span[@class='main_content_date szty2']",
                    "name": "from",
                    "disable": ""
                }
            ]
        }
    ]
}
"""


test1 = """
{
    "start_url": "https://www.yidaiyilu.gov.cn/",
    "follows": [
        {
            "ord": 0,
            "type": "disordered_list",
            "list": [
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='main-1 left']/div[@class='title']/span[@class='title_name']/a[@class='yw3']",
                    "next_follow_ord": 1,
                    "link_selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='main-1 left']/div[@class='title']/span[@class='title_name']/a[@class='yw3']",
                    "columns": [
                        {
                            "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='main-1 left']/div[@class='title']/span[@class='title_name']/a[@class='yw3']",
                            "name": "title",
                            "disable": ""
                        }
                    ]
                },
{
                    "selector": "/html/body/div[@class='mainBox1180'][3]/div[@class='main-1 left wtfz']/ul[@class='wtfz_ul']/a[2]",
                    "next_follow_ord": 4,
                    "link_selector": "/html/body/div[@class='mainBox1180'][3]/div[@class='main-1 left wtfz']/ul[@class='wtfz_ul']/a[2]",
                    "columns": [
                        {
                            "selector": "/html/body/div[@class='mainBox1180'][3]/div[@class='main-1 left wtfz']/ul[@class='wtfz_ul']/a[2]/li[@class='wtfz2']",
                            "name": "title",
                            "disable": ""
                        }
                    ]
                }
            ]
        },
        {
            "ord": 1,
            "type": "next_page",
            "next_follow_ord": 2,
            "link_selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/div[@class='page']/span[8]/a"
        },
        {
            "ord": 2,
            "type": "orderly_list",
            "selector1": "/html/body/div[@class='mainBox1180'][2]/div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[1]",
            "selector2": "/html/body/div[@class='mainBox1180'][2]/div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[2]",
            "link_selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[1]/div[@class='left_content left']/a",
            "next_follow_ord": 2,
            "columns": [
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[1]/div[@class='left_content left']/a[1]/h1",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[1]/div[@class='left_content left']/a[2]/p[@class='lineHeight180']",
                    "name": "abstract",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[1]/div[@class='left_content left']/span",
                    "name": "date",
                    "disable": ""
                }
            ]
        },
        {
            "ord": 3,
            "type": "single_page",
            "columns": [
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@id='zoom']/h1[@class='main_content_title']",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@id='zoom']/div[1]/div[@class='szty']/span[@class='main_content_date szty1 ']",
                    "name": "date",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@id='zoom']/div[1]/div[@class='szty']/span[@class='main_content_date szty2']",
                    "name": "from",
                    "disable": ""
                }
            ]
        },
        {
            "ord": 4,
            "type": "orderly_list",
            "selector1": "/html/body/div[@class='mainBox1180']/div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][1]",
            "selector2": "/html/body/div[@class='mainBox1180']/div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][2]",
            "link_selector": "/html/body/div[@class='mainBox1180']/div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][1]/a",
            "next_follow_ord": 3,
            "columns": [
                {
                    "selector": "/html/body/div[@class='mainBox1180']/div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][1]/a/h1[@class='f16px']",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180']/div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][1]/p[1]",
                    "name": "abstract",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180']/div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][1]/p[@class='right']",
                    "name": "date",
                    "disable": ""
                }
            ]
        }
    ]
}"""


test2 = """{
    "start_url": "https://www.yidaiyilu.gov.cn/",
    "follows": [
        {
            "ord": 0,
            "type": "disordered_list",
            "list": [
                {
                    "selector": "//div[@class='main-1 left']/div[@class='title']/span[@class='title_name']/a[@class='yw3']",
                    "next_follow_ord": 2,
                    "link_selector": "//div[@class='main-1 left']/div[@class='title']/span[@class='title_name']/a[@class='yw3']",
                    "columns": [
                        {
                            "selector": "//div[@class='main-1 left']/div[@class='title']/span[@class='title_name']/a[@class='yw3']",
                            "name": "title",
                            "disable": ""
                        }
                    ]
                },
                {
                    "selector": "//div[@class='main-1 left wtfz']/ul[@class='wtfz_ul']/a[2]",
                    "next_follow_ord": 4,
                    "link_selector": "//div[@class='main-1 left wtfz']/ul[@class='wtfz_ul']/a[2]",
                    "columns": [
                        {
                            "selector": "//div[@class='main-1 left wtfz']/ul[@class='wtfz_ul']/a[2]/li[@class='wtfz2']",
                            "name": "title",
                            "disable": ""
                        }
                    ]
                }
            ]
        },
        {
            "ord": 1,
            "type": "next_page",
            "next_follow_ord": 2,
            "link_selector": "//div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/div[@class='page']/span/a"
        },
        {
            "ord": 2,
            "type": "orderly_list",
            "has_next_page": true,
            "next_page_ord": 1,
            "selector1": "//div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[1]",
            "selector2": "//div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[2]",
            "link_selector": "//div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li/div[@class='left_content left']/a",
            "next_follow_ord": 3,
            "columns": [
                {
                    "selector": "//div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[1]/div[@class='left_content left']/a[1]/h1",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "//div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[1]/div[@class='left_content left']/a[2]/p[@class='lineHeight180']",
                    "name": "abstract",
                    "disable": ""
                },
                {
                    "selector": "//div[@class='wtfz_list_out']/div[@class='wtfz_list_right left']/ul/li[1]/div[@class='left_content left']/span",
                    "name": "date",
                    "disable": ""
                }
            ]
        },
        {
            "ord": 3,
            "type": "single_page",
            "columns": [
                {
                    "selector": "//div[@id='zoom']/h1[@class='main_content_title']",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "//div[@id='zoom']/div/div[@class=' szty']/span[@class='main_content_date szty1 ']",
                    "name": "date",
                    "disable": ""
                },
                {
                    "selector": "//div[@id='zoom']/div/div[@class=' szty']/span[@class='main_content_date szty2']",
                    "name": "from",
                    "disable": ""
                }
            ]
        },
        {
            "ord": 4,
            "type": "orderly_list",
            "has_next_page": false,
            "next_page_ord": 0,
            "selector1": "//div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][1]",
            "selector2": "//div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][2]",
            "link_selector": "//div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][1]/a",
            "next_follow_ord": 3,
            "columns": [
                {
                    "selector": "//div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][1]/a/h1[@class='f16px']",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "//div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][1]/p[1]",
                    "name": "abstract",
                    "disable": ""
                },
                {
                    "selector": "//div[@class='main-1 left wtfz']/div[@class='con_wtfzx_2']/div[@class='right hwksl_pic_wtfz'][1]/p[@class='right']",
                    "name": "date",
                    "disable": ""
                }
            ]
        }
    ]
}
"""

test3 = """
{
    "start_url": "http://www.creditchina.gov.cn/channel_news/1/1",
    "follows": [
        {
            "ord": 1,
            "type": "next_page",
            "next_follow_ord": 0,
            "link_selector": "//ul[@id='pagination']/li/a[@class='page-link next']"
        },
        {
            "ord": 0,
            "type": "orderly_list",
            "has_next_page": true,
            "next_page_ord": 1,
            "selector1": "/html/body/div[@class='wrapper']/div[@class='mod-page mod-page-dongtai clearfix']/div[@class='channel-page-left']/div[@class='main-channel clearfix']/div[@class='main-channel-left']/div[@class='select-box clearfix']/div[@class='dom-box selected-dom clear']/ul/li[1]",
            "selector2": "/html/body/div[@class='wrapper']/div[@class='mod-page mod-page-dongtai clearfix']/div[@class='channel-page-left']/div[@class='main-channel clearfix']/div[@class='main-channel-left']/div[@class='select-box clearfix']/div[@class='dom-box selected-dom clear']/ul/li[2]",
            "link_selector": "/html/body/div[@class='wrapper']/div[@class='mod-page mod-page-dongtai clearfix']/div[@class='channel-page-left']/div[@class='main-channel clearfix']/div[@class='main-channel-left']/div[@class='select-box clearfix']/div[@class='dom-box selected-dom clear']/ul/li[2]/span[@class='dom-title']/a[@class='ellipsistext']",
            "next_follow_ord": 2,
            "columns": [
                {
                    "selector": "/html/body/div[@class='wrapper']/div[@class='mod-page mod-page-dongtai clearfix']/div[@class='channel-page-left']/div[@class='main-channel clearfix']/div[@class='main-channel-left']/div[@class='select-box clearfix']/div[@class='dom-box selected-dom clear']/ul/li[2]/span[@class='dom-title']/a[@class='ellipsistext']",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='wrapper']/div[@class='mod-page mod-page-dongtai clearfix']/div[@class='channel-page-left']/div[@class='main-channel clearfix']/div[@class='main-channel-left']/div[@class='select-box clearfix']/div[@class='dom-box selected-dom clear']/ul/li[2]/span[@class='dom-time']",
                    "name": "abstract",
                    "disable": ""
                }
            ]
        },
        {
            "ord": 2,
            "type": "single_page",
            "columns": [
                {
                    "selector": "/html/body/div[@class='wrapper']/div[@class='mod-page article-detail clearfix']/div[@class='article-page-left']/div[@class='article-state-top']/p[@class='article-page-title ']",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='wrapper']/div[@class='mod-page article-detail clearfix']/div[@class='article-page-left']/div[@class='article-state-top']/div[@class='article-top-share']/div[@class='soucrces']/span[@class='article-source ellipsistext']",
                    "name": "from",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='wrapper']/div[@class='mod-page article-detail clearfix']/div[@class='article-page-left']/div[@class='article-state-top']/div[@class='article-top-share']/div[@class='soucrces']/span[@class='time-source']",
                    "name": "date",
                    "disable": ""
                }
            ]
        }
    ]
}
"""


#regex
testr1 = r"""
{
    "task_no":"ab124",
    "start_url": "https://www.yidaiyilu.gov.cn/",
    "url_rules": [
        {"ord":0,
            "allow": ["\\d*\\.html?"],
            "deny": [],
"need_parse":true,
            "columns": [
                {
                    "selector": "/html/body/div[@class='mainBox1180'][3]/div[@class='main-1 left wtfz']/div[@class='con_wtfz_1']/ul[@class='commonList_dot']/li[4]/a",
                    "name": "test1",
                    "disable": ""
                },
                {
                    "selector": "/html/body/div[@class='mainBox1180'][2]/div[@class='main-1 left']/div[@class='con_yw_1']/ul[@class='commonList_dot']/li[7]/a",
                    "name": "test2",
                    "disable": ""
                }
            ]
        }
    ]
}
"""


logined_universal = """
{
"task_no":"ab126",
"login_url":"",
"login_account":"",
"login_password":"",
    "start_url": "http://www.creditchina.gov.cn/channel_news/1/1",
    "follows": [
        {
            "ord": 1,
            "type": "next_page",
            "next_follow_ord": 0,
            "link_selector": ""
        },
        {
            "ord": 0,
            "type": "orderly_list",
            "has_next_page": true,
            "next_page_ord": 1,
            "selector1": "",
            "selector2": "",
            "link_selector": "",
            "next_follow_ord": 2,
            "columns": [
                {
                    "selector": "",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "",
                    "name": "abstract",
                    "disable": ""
                }
            ]
        },
        {
            "ord": 2,
            "type": "single_page",
            "columns": [
                {
                    "selector": "",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "",
                    "name": "from",
                    "disable": ""
                },
                {
                    "selector": "",
                    "name": "date",
                    "disable": ""
                }
            ]
        }
    ]
}"""

logined_u1 = """
{
"task_no":"ab126",
"login_request_url":"http://www.tuicool.com/login",
"login_url":"http://www.tuicool.com/login",
"login_account":"f565869090@126.com",
"login_password":"flk565869090",
"form_xpath":"//form[@class='form-horizontal']",
    "start_url": "http://www.tuicool.com/articles/weekly",
    "follows": [
        {
            "ord": 1,
            "type": "next_page",
            "next_follow_ord": 0,
            "link_selector": "//div[@class='weekly']/div[@class='week_right']/a[@class='right']"
        },
        {
            "ord": 0,
            "type": "orderly_list",
            "has_next_page": true,
            "next_page_ord": 1,
            "selector1": "//div[@class='weekly']/div[@class='week_content']/ol[@class='timeline clearfix']/li[@class='left'][1]/div[@class='unit']",
            "selector2": "//div[@class='weekly']/div[@class='week_content']/ol[@class='timeline clearfix']/li[@class='left'][2]/div[@class='unit']",
            "link_selector": "//div[@class='weekly']/div[@class='week_content']/ol[@class='timeline clearfix']/li[@class='left'][2]/div[@class='unit']/div[@class='span9']/h4/a[@class='title']",
            "next_follow_ord": 2,
            "columns": [
                {
                    "selector": "//div[@class='weekly']/div[@class='week_content']/ol[@class='timeline clearfix']/li[@class='left'][2]/div[@class='unit']/div[@class='span9']/h4/a[@class='title']",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "//div[@class='weekly']/div[@class='week_content']/ol[@class='timeline clearfix']/li[@class='left'][2]/div[@class='unit']/div[@class='span9']/span[@class='line-break']",
                    "name": "from",
                    "disable": ""
                }
            ]
        },
        {
            "ord": 2,
            "type": "single_page",
            "columns": [
                {
                    "selector": "//div[@class='container-fluid']/div[@class='row-fluid article_row_fluid']/div[@class='span8 contant article_detail_bg']/h1",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "//div[@id='nei']",
                    "name": "content",
                    "disable": ""
                },
                {
                    "selector": "//div[@class='article_meta']/div[1]/span[@class='timestamp']",
                    "name": "date",
                    "disable": ""
                }
            ]
        }
    ]
}"""

logined_u2 = """
{
"task_no":"ab127",
"login_request_url":"https://www.jianshu.com/sessions",
"login_url":"https://www.jianshu.com/sign_in",
"login_account":"f565869090@126.com",
"login_password":"flk565869090",
"form_xpath":"//form[@class='form-horizontal']",
    "start_url": "http://www.tuicool.com/ah/101000000?lang=1",
    "follows": [
        {
            "ord": 1,
            "type": "next_page",
            "max_pages":5,
            "next_follow_ord": 0,
            "link_selector": "//div[@class='pagination']/ul/li[@class='next']/a"
        },
        {
            "ord": 0,
            "type": "orderly_list",
            "has_next_page": true,
            "next_page_ord": 1,
            "selector1": "//div[@id='list_article']/div[@class='list_article_item'][2]/div[@class='aricle_item_info']/div[@class='title']",
            "selector2": "//div[@id='list_article']/div[@class='list_article_item'][3]/div[@class='aricle_item_info']/div[@class='title']",
            "link_selector": "//div[@id='list_article']/div[@class='list_article_item'][2]/div[@class='aricle_item_info']/div[@class='title']/a",
            "next_follow_ord": 2,
            "columns": [
                {
                    "selector": "//div[@id='list_article']/div[@class='list_article_item'][2]/div[@class='aricle_item_info']/div[@class='title']/a",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "//div[@id='list_article']/div[@class='list_article_item'][2]/div[@class='aricle_item_info']/div[@class='tip']/span[1]",
                    "name": "from",
                    "disable": ""
                }
            ]
        },
        {
            "ord": 2,
            "type": "single_page",
            "columns": [
                {
                    "selector": "//div[@class='container-fluid']/div[@class='article_row_fluid']/div[@class='article_detail_bg']/h1",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "//div[@id='nei']",
                    "name": "content",
                    "disable": ""
                },
                {
                    "selector": "//div[@class='container-fluid']/div[@class='article_row_fluid']/div[@class='article_detail_bg']/div[@class='article_meta']/div[1]/span[@class='timestamp']",
                    "name": "date",
                    "disable": ""
                }
            ]
        }
    ]
}"""


logined_r1=r'''
{
    "task_no": "ab129",
    "login_request_url": "https://passport.csdn.net/account/login?ref=toolbar",
    "login_url": "https://passport.csdn.net/account/login",
    "login_account": "fhclk",
    "login_password": "flk565869090",
    "form_xpath": "//*[@id='fm1']",
    "start_url": "http://my.csdn.net/my/mycsdn",
    "url_rules": [
        {
            "ord": 0,
            "allow": [
                "^https?://\\w+\\.csdn\\.net"
            ],
            "deny": [],
            "need_parse": true,
            "columns": [
                {
                    "selector": "//div[@class='questions_detail_con']/dl/dt",
                    "name": "title",
                    "disable": ""
                },
                {
                    "selector": "//div[@class='questions_detail_con']/dl/dd/p",
                    "name": "question",
                    "disable": ""
                }
            ]
        }
    ]
}
'''

process = CrawlerProcess(get_project_settings())

import uuid
# 'followall' is the name of one of the spiders of the project.
# process.crawl('common', config=single_page)
# process.crawl('common', config=orderly_list)
# process.crawl('common', config=disordered_list)
# process.crawl('universalSpider', config=test3, crawlNo=str(uuid.uuid1()))
# process.crawl('regexSpider', config=testr1)
# process.crawl('universalSpider', taskNo="ziguangge", crawlNo=str(uuid.uuid1()))
# process.crawl('universalSplashSpider', taskNo="ziguangge", crawlNo=str(uuid.uuid1()))
# process.crawl('universalProxySpider', taskNo="ziguangge", crawlNo=str(uuid.uuid1()))
process.crawl('regexSpider', taskNo="ab124")

# process.crawl('universalLoginedSpider', config=logined_u1, crawlNo=str(uuid.uuid1()))
# process.crawl('regexLoginedSpider', config=logined_r1, crawlNo=str(uuid.uuid1()))
# process.crawl('universalLoginedSpider', taskNo="ab123")
# process.crawl('regexLoginedSpider', taskNo="ab124")
process.start()
