import httplib2
import re
import math
import os
import hashlib
from bs4 import BeautifulSoup


http = httplib2.Http('.cache')
encoding = 'GB2312'
DIR_BASE = 'news/'
# url links
# these links are the different news blocks' url
url_links = {
    'news': 'http://physics.scu.edu.cn/News/index.asp?ClassID=3',
    'notice': 'http://physics.scu.edu.cn/News/index.asp?ClassID=1',
    'recruit': 'http://physics.scu.edu.cn/News/index.asp?ClassID=16',
    'employment': 'http://physics.scu.edu.cn/News/index.asp?ClassID=15',
    'science': 'http://physics.scu.edu.cn/News/index.asp?ClassID=2'
}


url_base = 'http://physics.scu.edu.cn'  # to get image sources
pattern = '<a href=\"(/News/news_show\.asp\?ArticleID=[0-9]+)\" title=\"(.*?)\">'  # pattern used to get news_list


def str_to_md5(filename):
    m = hashlib.md5()
    m.update(filename.encode())
    return m.hexdigest()


def handle_content(url, url_type='str'):
    if url_type == 'list':
        contents = []
        for ele in url:
            response, content = http.request(ele)
            print('->got the content of news')
            try:
                contents.append(content.decode(encoding))
            except:
                print('Decode wrong at: {0}'.format(ele))
    else:
        response, contents = http.request(url)
        print('->got the news col')
        try:
            contents = contents.decode(encoding)
        except:
            print('Decode wrong at: {0}'.format(url))
    return contents


def handle_news_list(html, pattern):
    news_list = re.findall(string=html, pattern=pattern)  # get news list
    links = []  # store news' link
    news_spam = []  # store news' title and its spam
    spam_pattern = re.compile(pattern='[0-9]{4}/[0-9]{1,2}/[0-9]{1,2} [0-9]{1,2}:[0-9]{2}:[0-9]{2}')

    for news in news_list:
        links.append(url_base + news[0])  # get the link to news's page
        news_spam.append(spam_pattern.search(news[1]).group(0))
    return links, news_spam


def handle_news_files(news_links, dirs_pa):
    x_content = handle_content(url=news_links, url_type='list')  # content of news' page
    idx = 0
    files_path = []
    title_and_img = []

    for content in x_content:
        print('>>> parse news: ', idx)
        soup = BeautifulSoup(content, 'html.parser')  # use Beautiful to parse the original page
        news_title = soup.title.string

        article = soup.find('table', class_='right_news_lb')  # get the real article part
        article_fix = article.contents[1]  # fix the real article part
        images = article_fix.find_all('img')  # find all img tags from fixed article

        # get image resource, fix the original link, get the real url to image resource
        if len(images) > 0:
            temp = []
            for img in images:
                img_link = url_base + img.attrs['src']
                img.attrs['src'] = img_link
                temp.append(img_link)
            title_and_img.append((news_title, temp[0]))
        else:
            title_and_img.append((news_title, ''))

        dir_name = DIR_BASE + dirs_pa[idx].split()[0] + '/'  # get date, and combine DIR_BASE to get dir path

        if not os.path.exists(dir_name):
            os.makedirs(dir_name, mode=0o777)

        filename = str_to_md5(news_title)
        file_path = dir_name + filename + '.html'
        files_path.append(file_path)

        with open(file_path, 'wb') as f:
            f.write(article_fix.prettify('utf-8'))
        idx += 1

    return files_path, title_and_img


if __name__ == '__main__':
    for key, value in url_links.items():
        print('Start decode block: ', key, '...')
        html_content = handle_content(url=value)
        # get page num
        page_num = math.ceil(int(re.findall(string=html_content, pattern='<b>([0-9]+)</b>')[0]) / 10)
        for idx in range(page_num):
            # get the news list, 're.DOCTALL' accepts '\r\n'
            print('---Page at: ', idx)
            html_content = handle_content(url=value + '&page=' + str(idx + 1))
            if isinstance(html_content, str):
                news_links, news_spam = handle_news_list(html=html_content, pattern=re.compile(pattern, re.DOTALL))
                print('->get links over')
                files_path, title_and_img = handle_news_files(news_links=news_links, dirs_pa=news_spam)
            else:
                print('->Type is wrong, type: ', type(html_content))
        print(key, 'Done!')
    print('-Done!-')
