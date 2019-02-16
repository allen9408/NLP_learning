# https://www.jianshu.com/p/f8516eb9913f
import requests
from bs4 import BeautifulSoup
import re
import pdb
# from nltk import clean_html
from bs4 import BeautifulStoneSoup
from lxml.html.clean import Cleaner

def sanitize(dirty_html):
    cleaner = Cleaner(page_structure=True,
                  meta=True,
                  embedded=True,
                  links=True,
                  style=True,
                  processing_instructions=True,
                  inline_style=True,
                  scripts=True,
                  javascript=True,
                  comments=True,
                  frames=True,
                  forms=True,
                  annoying_tags=True,
                  remove_unknown_tags=True,
                  safe_attrs_only=True,
                  safe_attrs=frozenset([]),
                  remove_tags=('span', 'font', 'div', 'p','td', 'li', 'img', 'a', 'tr', 'br','table','ul', 'strong','body', 'b', 'tbody', 'hr')
                  )

    return cleaner.clean_html(dirty_html)

def clean_html(html):
    """
    Copied from NLTK package.
    Remove HTML markup from the given string.

    :param html: the HTML string to be cleaned
    :type html: str
    :rtype: str
    """

    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()


def cleanHtml(html):
    if html == "": return ""
    # return BeautifulStoneSoup(clean_html(html),
    #     convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]
    return BeautifulStoneSoup(clean_html(html)).contents[0]
        # convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]
# 请求的首部信息
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}
all_titles = []
all_news = []
news_text = []

for i in range(1, 74, 1):
    # 例子的url
    url = 'http://www.cmbchina.com/cmbinfo/news/?PageNo=' + str(i)
    # 利用requests对象的get方法，对指定的url发起请求
    # 该方法会返回一个Response对象
    res = requests.get(url, headers=headers)
    # 通过Response对象的text方法获取网页的文本信息
    # print(res.content.decode('utf-8'))
    res = res.content.decode('utf-8')
    soup = BeautifulSoup(res, 'lxml')

    news_list = soup.find_all('span', {'class':'c_title'})

    new_titles = []
    url_list = []
    for new in news_list:
        # print(new)
        try:
            title = new.find('a').get('title').strip()
            url = new.find('a').get('href')
            new_titles.append(title)
            url_list.append(url)
            # print('title:', title)
            # print('url:', url)
        except AttributeError as e:
            continue
    for idx, news_url in enumerate(url_list):
        try:
            full_url = 'http://www.cmbchina.com/cmbinfo/news/' + news_url
            print('page:', i, 'index', idx, 'url:', full_url)
            res = requests.get(full_url, headers=headers)
            soup = BeautifulSoup(res.content, 'lxml')
            text = sanitize(res.text)
            text = text.replace('\n', '')
            text = text.replace('\t', '')
            text = text.replace('\r', '')
            text = text.replace('\xa0', '')
            text = text.replace(' ', '')
            news_text.append(text)
            with open('log.txt', 'a') as f:
                f.write(text+'\n')
        except:
            continue
        # print()
with open('cmb.txt', 'w') as f:
    for t in news_text:
        f.write(t+'\n')