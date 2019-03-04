import requests
from bs4 import BeautifulSoup
import re
import bs4
import pdb
import random
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Cookie': '_lxsdk_cuid=168e5236e74c8-0db44206d0460a-133b6850-13c680-168e5236e7442; _lxsdk=168e5236e74c8-0db44206d0460a-133b6850-13c680-168e5236e7442; _hc.v=2225c4f0-6bd4-94b0-009f-b35460c64bf0.1550032532; cy=1; cye=shanghai; s_ViewType=10; ua=WeiXin_2162697619; ctu=d8939db80866d9543f092d50ec75d2fa808dc726b9f0c88b13d7398ad1a09628; dper=1ad2812285324f0ea68c0c581b08c942b8736bc0efd38cb226cb447402f97cd01beef05e8c0a9d35a5876ad015dbdd0ca0682ffd09398bc78f4dea7a73aec8ee39a108073201259cdf21d814f24601bb5f9d961edfcc561a41d3f8dfb021f7e2; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _lxsdk_s=1690966ca2a-064-c26-dc7%7C%7C579'
}
headers_no_cookie = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}

def get_word_from_dict(ids, positions, text_lines, pos):
    row_idx = 0
    for i, n in enumerate(positions):
        if abs(pos[1]) <= n:
            break
        row_idx += 1
    col_idx = int(abs(pos[0]) // 14)
#     print(row_idx, col_idx)
    return text_lines[row_idx][col_idx]

def code2text(css_pos_dict, ids, positions, text_lines, code):
    pos = css_pos_dict[code]
    return get_word_from_dict(ids, positions, text_lines, pos)

def get_comments_from_url(url):
    comments_list = []
    res = requests.get(url, headers = headers)
    res = res.content.decode('utf-8')
    # get css link
    soup = BeautifulSoup(res, 'lxml')
    css_text_urls = soup.find_all('link', {'rel':'stylesheet'})
    # pdb.set_trace()
    if len(css_text_urls) < 2:
        return comments_list
    css_text_url = css_text_urls[1].get('href')
    
    # get css: code->position dictionary
    css_dict_res = requests.get('https:'+css_text_url, headers=headers)
    css_dicts = css_dict_res.content.split(b'background-image: url')
    results = re.findall(b'\((.*?)\)',css_dict_res.content)
    text_books = []
    for idx, text_url in enumerate(results):
        text_res = requests.get('https:'+text_url.decode(), headers=headers)
        text_books.append(text_res.content)
    
    # code -> position dictionary
    css_list = re.findall('(.*){background:(.+)px (.+)px;', '\n'.join(css_dict_res.text.split('}')))
    css_pos_dict = {}
    for code, x, y in css_list:
        css_pos_dict[code[1:]] = (float(x), float(y))

    # get textbook
    comment_textbook = text_books[0]
    # analyze textbook
    soup_comment_tb = BeautifulSoup(comment_textbook.decode('utf-8'), 'lxml')
    row_list = soup_comment_tb.find_all('path')
    ids, positions = [], []
    for row in row_list:
        _id = row.get('id')
        ids.append(_id)
        _pos = row.get('d')
        positions.append(int(_pos[3:-5]))
    text_rows = soup_comment_tb.find_all('textpath')
    text_lines = []
    for row in text_rows:
        text_lines.append(row.get_text())

    # get user comments
    # user_comments_list = soup.find_all('p', {'class':'desc J-desc'})
    user_comments_list = soup.find_all('div', {'class':'review-words Hide'})
    # pdb.set_trace()
    for user_comments in user_comments_list:
        comment_decoded = []
        for e in user_comments:
            if type(e) == bs4.element.NavigableString:
                comment_decoded.append(e.string)
            elif type(e) == bs4.element.Tag:
                try:
                    code = e.get('class')[0]
                    comment_decoded.append(code2text(css_pos_dict, ids, positions, text_lines,code))
                except:
                    continue
            else:
                print('Warning: unknown type: ', type(e))
        comment_final = ''.join(comment_decoded)
        comment_final = comment_final.replace('\xa0', ' ')
        comments_list.append(comment_final)
        # comment_decoded
    return comments_list

def get_comments_from_shop(shop_url):
    all_comments = []
    _res = requests.get(shop_url, headers=headers)
    _res = _res.content.decode('utf-8')
    soup = BeautifulSoup(_res, 'lxml')
    # pdb.set_trace()
    print('shop: ', shop_url)
    shop_name = soup.find('h1').contents[0]

    base_url = shop_url + '/review_all'
    
    review_urls = [base_url]
    review_page_number = 10
    for i in range(2, review_page_number+1):
        review_urls.append(base_url + '/p' + str(i))

    for url in review_urls:
        sleep_seconds = random.randint(5, 30)
        print('sleep ', sleep_seconds, 'seconds')
        time.sleep(sleep_seconds)
        print('Analyzing: ', url)
        comments_list = get_comments_from_url(url)
        if not comments_list:
            print('Warning: Nothing collect from: ', url)
        with open('dzdp_log.txt', 'a') as f:
            for c in comments_list:
                f.write(c)
        all_comments +=  comments_list
    return shop_name, all_comments

def web_crawler(start_url):
    shop_url_list = []
    res = requests.get(start_url, headers = headers)
    res = res.content.decode('utf-8')
    soup = BeautifulSoup(res, 'lxml')
    shops = soup.find_all('div', {'class':'tit'})
    for shop in shops:
        shop_url = shop.find('a').get('href')
        shop_url_list.append(shop_url)
    # pdb.set_trace()
    for shop_url in shop_url_list:
        shop_name, all_comments = get_comments_from_shop(shop_url)
        with open('dzdp_hot_SH.txt', 'a') as f:
            f.write('*[*' + shop_name + '*]*\n')
            for comments in all_comments:
                f.write(comments)


if __name__ == '__main__':
    start_base_url = 'http://www.dianping.com/shanghai/ch10/'
    for i in range(9, 51):
        start_url = start_base_url + 'p' + str(i)

        sleep_seconds = random.randint(5, 15)
        print('sleep ', sleep_seconds, 'seconds')
        time.sleep(sleep_seconds)
        print('Analyzing: ', start_url, ', page: ', i)
        web_crawler(start_url)
# print(get_comments_from_shop('http://www.dianping.com/shop/19612173'))
