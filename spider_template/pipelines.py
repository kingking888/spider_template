# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from spider_template.db_actions.mongo_action import OriginalData, FailedData
from spider_template.items import DetailPageItem, FailedItem
from spider_template.spiders.template import SpiderTemplate


class SpiderTemplatePipeline:

    def open_spider(self, spider):
        """当爬虫启动的时候执行"""
        if isinstance(spider, SpiderTemplate):
            # open_spider方法中, 链接 MongoDB数据库, 获取要操作的集合
            self.or_data = OriginalData()
            self.failed_data = FailedData()

    def process_item(self, item, spider):
        # process_item 方法中, 向MongoDB中插入数据
        if isinstance(item, DetailPageItem):
            self.or_data.insert_one(dict(item))
        if isinstance(item, FailedItem):
            self.failed_data.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        # close_spider 方法中, 关闭MongoDB的链接
        if isinstance(spider, SpiderTemplate):
            self.or_data.close()
            self.failed_data.close()
