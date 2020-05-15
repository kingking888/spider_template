from scrapy.http import Response


class HtmlParse(object):

    @classmethod
    def parse_nav_page(cls, response: Response, selector: dict):
        items = list()
        for k, v in selector.items():
            data = []
            values = response.xpath(v).extract()
            for value in values:
                data.append({k: value})
            items.append(data)
        for item in zip(*items):
            temp_d = dict()
            for i in item:
                temp_d.update(i)
            yield temp_d

    @classmethod
    def parse_detail_page(cls, response: Response, selector: str):
        # items = dict()
        # for k, v in selector.items():
        #     values = response.xpath(v).extract_first()
        #     items[k] = values.strip() if values else ''
        # return items
        return response.xpath(selector).extract_first()

    @classmethod
    def parse_increment(cls, response: Response, selector: str):
        return response.xpath(selector).extract_first()

    # # def content_selector(self, dom, nav_task:NavTask):
    # #     field_list = self.selector_parse.vague_extract(dom, nav_task.content_item)
    # #     for field in self.block_property_union(field_list, base_url=dom.base_url):
    # #         yield field
    #
    # def list_selector(self, dom, nav_task: NavTask):
    #     field_list = self.selector_parse.vague_extract(dom, nav_task.list_selectors)
    #     for field in self.block_property_union(field_list, base_url=dom.base_url):
    #         yield field
    #
    # def content_selectors(self, dom, detail_task: DetailTask):
    #     for content_selector in detail_task.content_item:
    #         field_list = self.selector_parse.accurate_extract(dom, content_selector.content_selectors)
    #         nav_data = detail_task.nav_value
    #         for data in self.single_property_union(field_list):
    #             nav_data.update(data)
    #             yield nav_data
    #
    # def block_property_union(self, field_chain, **kwargs):
    #     keys, field_list = fields_spread(field_chain)
    #     for f in zip(*field_list):
    #         data = dict(zip(keys, [self.localizer_parse.extract(v[0], v[1]) for v in f]))
    #         data["url"] = urljoin(kwargs["base_url"], data["url"])
    #         yield data
    #
    # def single_property_union(self, fields):
    #     def union(field):
    #         elem = [params_exp(sf) for sf in field]
    #         return " ".join([self.localizer_parse.extract(v[0], v[1]) for v in elem])
    #
    #     item = {}
    #     for name, field in fields.items():
    #         item[name] = union(field)
    #     yield item
    #


class JsonParse(object):

    def __init__(self, response: Response, selector: dict):
        self.response = response
        self.selector = selector

    def parse_nav_page(self):
        items = list()
        for k, v in self.selector.items():
            data = []
            values = self.response.xpath(v).extract()
            for value in values:
                data.append({k: value})
            items.append(data)
        for item in zip(*items):
            temp_d = dict()
            for i in item:
                temp_d.update(i)
            yield temp_d

    def parse_detail_page(self):
        items = dict()
        for k, v in self.selector.items():
            values = self.response.xpath(v).extract_first()
            items[k] = values.strip() if values else ''
        return items


def get_parser(page_type):
    if page_type == "html":
        return HtmlParse
    elif page_type == "json":
        return JsonParse
    else:
        raise Exception('页面类型错误')
