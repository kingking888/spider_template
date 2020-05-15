# -*- coding: utf-8 -*-

# Scrapy settings for spider_template project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider_template'

SPIDER_MODULES = ['spider_template.spiders']
NEWSPIDER_MODULE = 'spider_template.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'spider_template.middlewares.CustomDownloadMiddleware': 900,
}

SPIDER_MIDDLEWARES = {
    'spider_template.middlewares.CustomSpiderMiddleware': 543,
}

LOG_LEVEL = "INFO"

ITEM_PIPELINES = {
    'spider_template.pipelines.SpiderTemplatePipeline': 300,
}
# mongo 配置
MONGO_URI = 'mongodb://127.0.0.1:27017'  # mongo 地址
MONGO_DB = "spider_template"  # 库名
MONGO_TEMPLATE = "template_info"  # 模板表
MONGO_ORDATA = "or_data"  # 原始数据表
MONGO_DUPEFILTER = "dupe_filter"  # 过滤表
MONGO_FAILED = "failed_data"  # 爬取失败信息表

# redis 配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PARAMS = {
    'password': 'redis',
}
PASS_WD = 'redis'
REDIS_KEY = "spider_template:template_info"

# 去重容器类: 重写去重，改为mongo去重
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
DUPEFILTER_CLASS = 'spider_template.utils.dupefilter.MFPDupeFilter'

# 调度器: 用于把待爬请求存储到基于Redis的队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 是不进行调度持久化:
# 如果是True, 当程序结束的时候, 会保留Redis中已爬指纹和待爬的请求
# 如果是False, 当程序结束的时候, 会清空Redis中已爬指纹和待爬的请求
# SCHEDULER_PERSIST = False

# 设置重爬
# SCHEDULER_FLUSH_ON_START = True
