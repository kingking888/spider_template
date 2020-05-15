import hashlib
import logging
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from spider_template.db_actions.mongo_action import DupeFilter

# from scrapy_redis.dupefilter.RFPDupeFilter
logger = logging.getLogger(__name__)


class UrlOperator(object):

    @staticmethod
    def clean_anchor(url):
        return url.split("#")[0]

    @staticmethod
    def clean_param(url):
        return url.split("?")[0]

    @staticmethod
    def url_md5(url):
        return hashlib.md5(url.encode()).hexdigest()


class MFPDupeFilter(BaseDupeFilter):
    logger = logger

    def __init__(self, server, key, debug=False):
        self.debug = debug
        self.mongo = DupeFilter()
        # self.url_clean = UrlOperator
        self.logdupes = True

    @classmethod
    def from_settings(cls, settings):
        """
        1、创建对象
        :param settings:
        :return:
        """
        server = DupeFilter()
        key = ''
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(server, key, debug=debug)

    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.

        Parameters
        ----------
        crawler : scrapy.crawler.Crawler

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """
        检查是否已经访问过
        :param request:
        :return:
        """
        template = request.meta.get('template')
        if template.stage != len(template.selector)-1:
            return False
        data = template.default_values
        fp = self.request_fingerprint(request)
        record = {
            '_id': fp,
            'web_site': template.web_site,
            'title': data['title'],
            'url': template.url
        }
        data = self.mongo.find_one({"_id": record['_id']})
        if not data:
            try:
                self.mongo.update({"_id": record['_id']}, record, upsert=True)
            except Exception as e:
                print(e)
                # 解决多线程调用问题，1.mongo不支持单个事物操作，2.加锁会造成资源浪费
                return True
            return False
        return True

    @staticmethod
    def request_fingerprint(request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)

    def open(self):  # can return deferred
        """
        3、开始爬取
        :return:
        """
        print('open')
        pass

    def clear(self):
        """Clears fingerprints data."""
        pass

    def close(self, reason):  # can return a deferred
        self.mongo.close()

    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False
