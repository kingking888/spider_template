import re
import chardet
from urllib.parse import unquote
from w3lib.html import remove_tags, remove_tags_with_content, remove_comments


CHARSETS = {
    'big5': 'big5hkscs',
    'gb2312': 'gb18030',
    'ascii': 'utf-8',
    'maccyrillic': 'cp1251',
    'win1251': 'cp1251',
    'win-1251': 'cp1251',
    'windows-1251': 'cp1251',
}

def fix_charset(encoding):
    """Overrides encoding when charset declaration
       or charset determination is a subset of a larger
       charset.  Created because of issues with Chinese websites"""
    encoding = encoding.lower()
    return CHARSETS.get(encoding, encoding)


class HTMLParseUnit(object):

    def remove_comments(self, html):
        return remove_comments(html)

    def remove_tags_with_content(self, text, which_ones=(), encoding=None):
        html = remove_tags_with_content(text, which_ones, encoding)
        html = remove_tags(html, which_ones, encoding=encoding)
        return html

    def dom_remove_tags_with_content(self, dom, nodes=()):
        for tag in nodes:
            dom(tag).remove()
        return dom

    def remove_hide_tag(self, html):
        hide_pattern = re.compile(r"(<[^>]+(?:(?<!: )hidden|display:\s*none)[^>]+>[^>]+>)", re.S | re.I)
        return hide_pattern.sub("", html)

    def remove_enter(self, html):
        html = html.replace("\n", "")
        html = html.replace("\r", "")
        html = html.replace("\t", "")
        return html

    def remove_useless_tag_property(self, html, keep):
        """
        移除keep之外的所有属性
        :param html: html
        :param keep: (href, src, )
        :return: html
        bad case before
            <a suda-uatrack="key=finance_stock_hotcol&value=5"> </a>
        """
        # html = html.replace("data-original", "src") 要放在前面否则会被data-条件替换,破坏替换条件
        html = html.replace("data-original", "src")
        html = html.replace("data-src", "src")
        keep_tag = "=|".join(keep)
        partten = re.compile(r'\b(?!(?:{}=))[\w]+=(["\']).*?\1\s?'.format(keep_tag), re.I)
        html = html.replace(" >", ">")
        return partten.sub('', html)

    def bytes_to_unicode(self, content, header_encoding: str="utf-8"):
        """
        :param text: 原始文本
        :return: 转码后的文本
        """
        if header_encoding.upper() == "ISO-8859-1":

            charset_re = re.compile(b'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I)
            pragma_re = re.compile(b'r<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I)
            xml_re = re.compile(b'^<\?xml.*?encoding=["\']*(.+?)["\'>]')
            encode = (charset_re.findall(content) +
                      pragma_re.findall(content) +
                      xml_re.findall(content))
            if not encode:
                encode = chardet.detect(content)['encoding']
            else:
                encode = encode[0]
        else:
            encode = header_encoding
        try:
            if isinstance(encode, bytes):
                text = str(content, fix_charset(encode.decode()), errors='replace')
            else:
                text = str(content, fix_charset(encode), errors='replace')
        except (LookupError, TypeError) as e:
            text = str(content, errors='replace')

        return text

    def delete_xmlns(self, html):
        pattern = re.compile("xmlns=\".*?\"")
        return re.sub(pattern, "", html)

    def clean_html(self, html, encode):
        html = self.bytes_to_unicode(html, encode)
        html = self.delete_xmlns(html)
        return html

    def html_unquote(self, html):
        return unquote(html)
