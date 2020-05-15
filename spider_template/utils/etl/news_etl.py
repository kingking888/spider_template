# coding=utf-8
import traceback

from spider_template.utils.etl.html_parse_unit import HTMLParseUnit
from spider_template.utils.etl.news_etl_base import *

html_parse_unit = HTMLParseUnit()


class NewsETL(object):

    @staticmethod
    def fill_content(html):
        html_fill = """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                <title>江苏筑优中标新闻</title>
            </head>
            <body>
                {}
            </body>
        </html>
        """
        return html_fill.format(html)

    @staticmethod
    def clean_title(title):
        final_title = cut_title_by_len(title)
        final_title = clean_esc_chart(final_title)
        return final_title

    @staticmethod
    def clean_publish_time(data) -> str:
        publish_time = extract_other_from_str(data["publish_time"])
        if publish_time:
            return publish_time
        ymd_from_url = extract_date_from_url(data["url"])
        ymd_from_date = extract_ymd_from_str(data["publish_time"])
        hms_from_date = extract_hms_from_str(data["publish_time"])
        url_publish_time = f"{ymd_from_url} {hms_from_date}".strip()
        str_publish_time = f"{ymd_from_date} {hms_from_date}".strip()
        try:
            datetime.datetime.strptime(str_publish_time, '%Y-%m-%d %H:%M:%S')
            return str_publish_time
        except Exception as e:
            pass

        try:
            datetime.datetime.strptime(url_publish_time, '%Y-%m-%d %H:%M:%S')
            return url_publish_time
        except Exception as e:
            pass

        md_from_str = extract_md_from_str(data["publish_time"])
        if hms_from_date and md_from_str:
            date = year_align(md_from_str, hms_from_date)
            return date.strftime('%Y-%m-%d %H:%M:%S') if isinstance(date, datetime.datetime) else date
        elif hms_from_date:
            date = day_align(hms_from_date)
            return date.strftime('%Y-%m-%d %H:%M:%S') if isinstance(date, datetime.datetime) else date

        return datetime.datetime(year=1988, month=1, day=1).strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def clean_content(cls, html_str):

        html = html_parse_unit.remove_comments(html_str)
        html = html_parse_unit.remove_enter(html)
        html = html_parse_unit.remove_hide_tag(html)
        html = html_parse_unit.html_unquote(html)
        html = html_parse_unit.remove_useless_tag_property(html, keep=("href", "src", "rowspan", "colspan"))
        html = html_parse_unit.remove_tags_with_content(html,
                                                        ("s", "input", "form", "iframe", "script", "ins", "style"))
        return cls.fill_content(html)
