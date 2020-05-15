# coding=utf-8
import datetime
import re
from itertools import chain
from spider_template.utils.etl.news_etl_rules import URL_DATE_PATTERNS, COMMON_DATE_PATTERNS, \
    CHINESE_DATE_PATTERNS, ENGLISH_DATE_PATTERNS, HMS_PATTERNS, CHANNEL_PATTERN, AUTHOR, SOURCE, MD_PATTERNS

""" 网站channel标准化 """


def channel_normalize(channel):
    channel = channel.replace("/", " ") \
        .replace(" ", ">") \
        .replace("首页", "")
    channel = re.sub(re.compile(">+"), " ", channel)
    return channel


""" 文章标签标准化 """


def tag_normalize(tag) -> str:
    tags = CHANNEL_PATTERN.searchString(tag)
    return ",".join(map(lambda x: x[0], tags)) or ""


""" 文章作者清洗 """


def clean_author(string) -> str:
    author = AUTHOR.searchString(string)
    return author[0][0] if author else ""


# 作者清洗
def clean_string(string) -> str:
    key = "原创 来源 源于 出处 来自 转载"
    for k in key.split(" "):
        string = string.replace(k, "")
    return string


def clean_source(string) -> str:
    source = SOURCE.searchString(string)
    return source[0][0] if source else ""


""" 发布时间 标准化 """


def year_align(md, hms):
    year = datetime.datetime.now().year
    for it in range(2):
        date = datetime.datetime.strptime(f"{year - it}-{md} {hms}", "%Y-%m-%d %H:%M:%S")
        if date < datetime.datetime.now():
            return date


def day_align(hms):
    now_date = datetime.datetime.now()
    for it in range(2):
        date = datetime.datetime.strptime(f"{now_date.year}-{now_date.month}-{now_date.day} {hms}", "%Y-%m-%d %H:%M:%S")
        if date < datetime.datetime.now():
            return date
        now_date = now_date - datetime.timedelta(days=1)


def extract_md_from_str(string):
    for rule_name, rule in MD_PATTERNS.items():
        item = rule.searchString(string)
        if item:
            return f"{int(item[0].month):02}-{int(item[0].day):02}"


def extract_date_from_url(url) -> str:
    for rule_name, rule in URL_DATE_PATTERNS.items():
        item = rule.searchString(url)
        if item:
            return f"{item[0].year}-{int(item[0].month):02}-{int(item[0].day):02}"


def extract_ymd_from_str(string) -> str:
    for rule_name, rule in chain(COMMON_DATE_PATTERNS.items(),
                                 CHINESE_DATE_PATTERNS.items(),
                                 ENGLISH_DATE_PATTERNS.items()):
        item = rule.searchString(string)
        if item:
            return f"{item[0].year}-{int(item[0].month):02}-{int(item[0].day):02}"


def extract_hms_from_str(string) -> str:
    for rule_name, rule in HMS_PATTERNS.items():
        item = rule.searchString(string)
        if rule_name == "pat:hh:mm:ss" and item:
            return f"{int(item[0].hour):02}:{int(item[0].minute):02}:{int(item[0].second):02}"
        elif rule_name == "pat:hh:mm am or pm" and item:
            return f"{int(item[0].hour) + int(item[0].tbasis):02}:{int(item[0].minute):02}:00"
        elif rule_name == "pat:hh:mm" and item:
            return f"{int(item[0].hour):02}:{int(item[0].minute):02}:00"
    return "00:00:00"


def extract_other_from_str(string):
    def just_now(_str):
        # 特殊表述方式 刚刚
        if _str.find("刚刚") > -1:
            return str(datetime.datetime.now()).split('.')[0]

    def time_ago(_str):
        # 特殊表述方式 几 (秒|分|分钟|小时|天)前
        time_ago_match = re.findall("(\d{1,2})\s?(秒|分|分钟|小时|天)前", _str)

        if not time_ago_match:
            return None
        if "秒" in time_ago_match[0]:
            return str(datetime.datetime.now() - datetime.timedelta(seconds=int(time_ago_match[0][0]))).split('.')[
                0]
        elif "分" in time_ago_match[0] or "分钟" in time_ago_match[0]:
            return str(datetime.datetime.now() - datetime.timedelta(minutes=int(time_ago_match[0][0]))).split('.')[
                0]
        elif "小时" in time_ago_match[0]:
            return str(datetime.datetime.now() - datetime.timedelta(hours=int(time_ago_match[0][0]))).split('.')[0]
        elif "天" in time_ago_match[0]:
            return str(datetime.datetime.now() - datetime.timedelta(days=int(time_ago_match[0][0]))).split('.')[0]

    def today_ro_yesterday(_str):
        # 特殊表述方式 今天、昨天 18：22
        today_ro_yesterday = "([昨今])天"
        today_ro_yesterday_match = re.findall(today_ro_yesterday, _str)
        if not today_ro_yesterday_match:
            return None

        if '今' in today_ro_yesterday_match[0]:
            return "{0} {1}".format(datetime.datetime.now().strftime("%Y-%m-%d"),
                                    extract_hms_from_str(_str))
        elif '昨' in today_ro_yesterday_match[0]:
            return "{0} {1}".format((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                                    extract_hms_from_str(string))

    return just_now(string) or time_ago(string) or today_ro_yesterday(string)


""" title 清洗"""


def cut_title_by_len(title):
    if len(title) > 50:
        cut_title = re.split("[；;。]", title, 1)
        return cut_title[0]
    return title


def clean_esc_chart(ftitle):
    if ftitle.find("&") == -1:
        return ftitle

    return ftitle.replace("&quot;", "\"") \
        .replace("&lt;", "<") \
        .replace("&gt;", ">") \
        .replace("&amp;", "&")


print(extract_other_from_str('今天'))
