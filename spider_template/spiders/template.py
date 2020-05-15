# -*- coding: utf-8 -*-
import copy
import hashlib
import pickle
import time
from datetime import datetime

import scrapy
from scrapy_redis.spiders import RedisSpider
from spider_template.settings import REDIS_KEY
from spider_template.items import FailedItem, DetailPageItem, FinishIncrementItem
from spider_template.utils.etl.news_etl import NewsETL
from spider_template.utils.template_parse import get_parser


class SpiderTemplate(RedisSpider):
    name = 'spider_template'
    redis_key = REDIS_KEY

    def make_request_from_data(self, data):
        """
        根据redis中读取的分类信息的二进制数据, 构建请求
        :param data: 分类信息的二进制数据
        :return: 根据小分类URL, 构建的请求对象
        """
        # 把分类信息的二进制数据 转换为字典
        template = pickle.loads(data)
        # 根据小分类的URL, 构建列表页的请求
        # 注意: 要使用return来返回一个请求, 不能使用yield
        print('start process start_url')
        return scrapy.Request(template.url, callback=self.nav_parse, meta={'template': template})

    def nav_parse(self, response):
        """
        导航页处理
        :param response:
        :return:
        """
        template = response.meta.get('template')
        code = template.code
        if code != 200:
            yield FailedItem(
                web_site=template.web_site,
                create_time=datetime.now(),
                url=template.url,
                code=template.code,
                msg=template.msg)
        else:
            stage = template.stage
            selector = copy.deepcopy(template.selector[template.stage])
            increment = template.increment
            increment_selector = selector.pop('increment')
            page_type = selector.pop('page_type')
            parser = get_parser(page_type)
            results = parser.parse_nav_page(response, selector)
            for result in results:
                next_url = result.get('infor_url')
                # print(next_url,len(template.selector))
                if next_url and stage != len(template.selector) - 2:
                    # 如果有下一个url,并且下一个不是详情页
                    # 导航页抓取
                    nav_template = copy.deepcopy(template)
                    nav_template.url = response.urljoin(next_url)
                    nav_template.stage = stage + 1
                    yield scrapy.Request(nav_template.url, callback=self.nav_parse, meta={'template': nav_template})
                if stage == len(template.selector) - 2:
                    # 详情页抓取
                    detail_template = copy.deepcopy(template)
                    detail_template.url = response.urljoin(next_url)
                    detail_template.stage = stage + 1
                    result.update({'infor_url': response.urljoin(next_url)})
                    detail_template.default_values.update(result)
                    yield scrapy.Request(detail_template.url, callback=self.detail_parse,
                                         meta={'template': detail_template})
            if increment:
                # 增量数据爬取
                next_page = parser.parse_increment(response, increment_selector)
                if next_page:
                    in_template = copy.deepcopy(response.meta.get('template'))
                    in_template.url = response.urljoin(next_page)
                    print(in_template.url)
                    yield scrapy.Request(in_template.url, callback=self.nav_parse, meta={'template': in_template})
                if not next_page:
                    yield FinishIncrementItem()

    def detail_parse(self, response):
        """
        详情页处理
        :param response:
        :return:
        """
        template = copy.deepcopy(response.meta.get('template'))
        code = template.code
        if code != 200:
            yield FailedItem(
                web_site=template.web_site,
                create_time=datetime.now(),
                url=template.url,
                code=template.code,
                msg=template.msg)
        else:
            stage = template.stage
            selector = copy.deepcopy(template.selector[stage])
            page_type = selector.get('page_type')
            parser = get_parser(page_type)
            detail_selector = selector.get('html_code')
            content = parser.parse_detail_page(response, detail_selector)
            etl = NewsETL()
            html_code = etl.clean_content(content)
            result = template.default_values
            result.update({'file_name': self.get_file_name(template.url),
                           'html_code': html_code})
            yield DetailPageItem(**result)

    def get_file_name(self, url):
        month_day = time.strftime('%Y%m%d', time.localtime(time.time()))
        return month_day + hashlib.md5(url.encode("utf-8")).hexdigest()
