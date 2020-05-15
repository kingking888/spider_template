from pyparsing import Word, nums, oneOf, Literal, Combine, srange, ZeroOrMore, Regex

year = Combine(Word("2", exact=1) + Word("01", exact=1) + Word(nums, exact=1) + Word(nums, exact=1)).setResultsName(
    "year")
month = Combine(Word("01", exact=1) + Word(nums, exact=1) | Word(nums, exact=1)).setResultsName("month")
day = Combine(Word("0123", exact=1) + Word(nums, exact=1)).setResultsName("day")

MD_PATTERNS = {
    "pat:mm/dd": month + Literal("/").suppress() + day,
    "pat:mm-dd": month + Literal("-").suppress() + day
}
URL_DATE_PATTERNS = {
    "pat:yyyy/mm/dd": year + Literal("/").suppress() + month + Literal("/").suppress() + day,
    "pat:yyyy-mm-dd": year + Literal("-").suppress() + month + Literal("-").suppress() + day,
    "pat:yyyymm/dd": year + month + Literal("/").suppress() + day,
    "pat:yyyy/mmdd": year + Literal("/").suppress() + month + day,
    "pat:yyyy-mm/dd": year + Literal("-").suppress() + month + Literal("/").suppress() + day,
    "pat:yyyy/mm-dd": year + Literal("/").suppress() + month + Literal("-").suppress() + day,
    "pat:yyyy-m-d": year + Literal('-').suppress() + Word(nums, min=1, max=2).setResultsName('month') + Literal(
        '-').suppress() + Word(nums, min=1, max=2).setResultsName('day'),
    "pat:yyyy/m/d": year + Literal('/').suppress() + Word(nums, min=1, max=2).setResultsName('month') + Literal(
        '/').suppress() + Word(nums, min=1, max=2).setResultsName('day'),
    "pat:yyyymmdd": year + month + day,
    "pat:mm/dd/yyyy": month + Literal("/").suppress() + day + year,
    "pat:mm-dd-yyyy": month + Literal("-").suppress() + day + Literal("-").suppress() + year,
}

COMMON_DATE_PATTERNS = {
    'pat:mm/dd/yyyy': month.setResultsName('month') + Literal('/').suppress() + day.setResultsName('day') + Literal(
        '/').suppress() + year.setResultsName('year'),
    'pat:yyyy/m/d': Word(nums, exact=4).setResultsName('year') + '/' + Word(nums, min=1, max=2).setResultsName(
        'month') + '/' + Word(nums, min=1, max=2).setResultsName('day'),
    'pat:d/m/yyyy': Word(nums, min=1, max=2).setResultsName('day') + Literal('/').suppress() + Word(nums, min=1,
                                                                                                    max=2).setResultsName(
        'month') + Literal('/').suppress() + Word(nums, exact=4).setResultsName('year'),
    'pat:m/d/yy': Word(nums, min=1, max=2).setResultsName('month') + Literal('/').suppress() + Word(nums, min=1,
                                                                                                    max=2).setResultsName(
        'day') + Literal('/').suppress() + Word(nums, exact=2).setResultsName('year'),
    'pat:d/m/yy': Word(nums, min=1, max=2).setResultsName('day') + Literal('/').suppress() + Word(nums, min=1,
                                                                                                  max=2).setResultsName(
        'month') + Literal('/').suppress() + Word(nums, exact=2).setResultsName('year'),
    'pat:yyyy-m-d': Word(nums, exact=4).setResultsName('year') + Literal('-').suppress() + Word(nums, min=1,
                                                                                                max=2).setResultsName(
        'month') + Literal('-').suppress() + Word(nums, min=1, max=2).setResultsName('day'),
    'pat:d-m-yyyy': Word(nums, min=1, max=2).setResultsName('day') + Literal('-').suppress() + Word(nums, min=1,
                                                                                                    max=2).setResultsName(
        'month') + Literal('-').suppress() + Word(nums, exact=4).setResultsName('year'),
    'pat:d-m-yy': Word(nums, min=1, max=2).setResultsName('day') + Literal('-').suppress() + Word(nums, min=1,
                                                                                                  max=2).setResultsName(
        'month') + Literal('-').suppress() + Word(nums, exact=2, max=2).setResultsName('year'),
    'pat:yyyy.m.d': Word(nums, exact=4).setResultsName('year') + Literal('.').suppress() + Word(nums, min=1,
                                                                                                max=2).setResultsName(
        'month') + Literal('.').suppress() + Word(nums, min=1, max=2).setResultsName('day'),
    'pat:d.m.yyyy': Word(nums, min=1, max=2).setResultsName('day') + Literal('.').suppress() + Word(nums, min=1,
                                                                                                    max=2).setResultsName(
        'month') + Literal('.').suppress() + Word(nums, exact=4).setResultsName('year'),
    'pat:d.m.yy': Word(nums, min=1, max=2).setResultsName('day') + Literal('.').suppress() + Word(nums, min=1,
                                                                                                  max=2).setResultsName(
        'month') + Literal('.').suppress() + Word(nums, exact=2).setResultsName('year'),
    'pat:yyyymmdd': Word(nums, exact=4).setResultsName('year') + Word(nums, exact=2).setResultsName('month') + Word(
        nums, exact=2).setResultsName('day'),
    'pat:ddmmyyyy': Word(nums, exact=2).setResultsName('day') + Word(nums, exact=2).setResultsName('month') + Word(nums,
                                                                                                                   exact=4).setResultsName(
        'year'),
}

month_mapping = {"一": "1", "二": "2", "三": "3",
                 "四": "4", "五": "5", "六": "6",
                 "七": "7", "八": "8", "九": "9",
                 "十": "10", "十一": "11", "十二": "12"}

chinese_month = oneOf("一 二 三 四 五 六 七 八 九 十 十一 十二").setResultsName("month").setParseAction(
    lambda _month: month_mapping[_month[0]])

CHINESE_DATE_PATTERNS = {
    "pat:yyyy年xx月xx日": Word(nums, exact=4).setResultsName('year') + Literal("年").suppress() + Word(nums, min=1,
                                                                                                   max=2).setResultsName(
        'month') + Literal("月").suppress() + Word(nums, min=1, max=2).setResultsName('day') + Literal("日").suppress(),
    "pat:xx月xx日yyyy": chinese_month + Literal("月").suppress() + Word(nums, min=1, max=2).setResultsName(
        'day') + Literal(",") + Word(nums, exact=4).setResultsName('year')
}

ENG_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
eng_month = oneOf(ENG_MONTHS).setParseAction(lambda t: en_mname2mon[t[0]])
ENG_MONTHS_LC = ['january', 'february', 'march', 'april', 'may', 'june', 'jule', 'august', 'september', 'october',
                 'november', 'december']
eng_month_lc = oneOf(ENG_MONTHS_LC).setParseAction(lambda t: enlc_mname2mon[t[0]])
ENG_MONTHS_SHORT = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
eng_month_short = oneOf(ENG_MONTHS_SHORT, caseless=True).setParseAction(lambda t: ensh_mname2mon[t[0].lower()])
en_mname2mon = dict((m, i + 1) for i, m in enumerate(ENG_MONTHS))
ensh_mname2mon = dict((m, i + 1) for i, m in enumerate(ENG_MONTHS_SHORT))
enlc_mname2mon = dict((m, i + 1) for i, m in enumerate(ENG_MONTHS_LC))

ENGLISH_DATE_PATTERNS = {
    "pat:dd.mm.yyyy": Word(nums, min=1, max=2).setResultsName('day') + oneOf(
        ". ,").suppress() + eng_month.setResultsName('month') + Literal('.').suppress() + Word(nums,
                                                                                               exact=4).setResultsName(
        'year'),
    "pat:dd.mm_lower.yyyy": Word(nums, min=1, max=2).setResultsName('day') + oneOf(
        ". ,").suppress() + eng_month_lc.setResultsName('month') + oneOf(". ,").suppress() + Word(nums,
                                                                                                  exact=4).setResultsName(
        'year'),
    "pat:dd.mm_short.yyyy": Word(nums, min=1, max=2).setResultsName('day') + oneOf(
        ". ,").suppress() + eng_month_short.setResultsName('month') + oneOf(". ,").suppress() + Word(nums,
                                                                                                     exact=4).setResultsName(
        'year'),
    "pat:mm,dd,yyyy": eng_month.setResultsName('month') + oneOf(". ,").suppress() + Word(nums, min=1,
                                                                                         max=2).setResultsName(
        'day') + oneOf(". ,").suppress() + Word(nums, exact=4).setResultsName('year'),
    "pat:mm dd,yyyy": eng_month.setResultsName('month') + Word(nums, min=1, max=2).setResultsName('day') + oneOf(
        ". ,").suppress() + Word(nums, exact=4).setResultsName('year'),
    "pat:mm_lower,dd,yyyy": eng_month_lc.setResultsName('month') + oneOf(". ,").suppress() + Word(nums, min=1,
                                                                                                  max=2).setResultsName(
        'day') + oneOf(". ,").suppress() + Word(nums, exact=4).setResultsName('year'),
    "pat:mm_short,dd,yyyy": eng_month_short.setResultsName('month') + oneOf(". ,").suppress() + Word(nums, min=1,
                                                                                                     max=2).setResultsName(
        'day') + oneOf(". ,").suppress() + Word(nums, exact=4).setResultsName('year'),
    "pat:dd mm yyyy": Word(nums, min=1, max=2).setResultsName('day') + eng_month.setResultsName('month') + Word(nums,
                                                                                                                exact=4).setResultsName(
        'year'),
}

hms_basis = {
    "p": 12,
    "a": 0
}
HMS_PATTERNS = {
    "pat:hh:mm:ss": Word(nums, min=1, max=2).setResultsName('hour') + Literal(':').suppress() + Word(nums,
                                                                                                     exact=2).setResultsName(
        'minute') + Literal(':').suppress() + Word(nums, exact=2).setResultsName("second"),
    "pat:hh:mm am or pm": Word(nums, min=1, max=2).setResultsName('hour') + Literal(':').suppress() + Word(nums,
                                                                                                           exact=2).setResultsName(
        'minute') + Word("AaMPpm", exact=2).setResultsName('tbasis').setParseAction(
        lambda tk: hms_basis[tk[0].lower()[0]]),
    "pat:hh:mm": Word(nums, min=1, max=2).setResultsName('hour') + Literal(':').suppress() + Word(nums,
                                                                                                  exact=2).setResultsName(
        'minute')
}

edit_title = Combine(oneOf("编辑 责任编辑 作者 记者 研究员 机构 分析員 责编 原创") + ZeroOrMore(oneOf(": ："))).suppress()
edit_name = Word(srange("[0-9A-Za-z\u4E00-\u9FA5]")).ignore(Regex(r"[\(\)(\xa0\u3000\r\n（）,/|丨]"))
AUTHOR = (edit_title + edit_name).setParseAction(lambda author: author[0])

CHANNEL_PATTERN = Word(srange("[0-9A-Za-z\u4E00-\u9FA5]"))

source_str = Combine(oneOf("原创 来源 源于 出处 来自 转载 发布") + ZeroOrMore(oneOf(": ："))).suppress()
source_name = Word(srange("[0-9A-Za-z\u4E00-\u9FA5]")).ignore(Regex(r"[\(\)(\xa0\u3000\r\n（）,/|丨]"))
SOURCE = (source_str + source_name).setParseAction(lambda source: source[0])

# 规则
