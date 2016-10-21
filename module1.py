import re, math, httplib2, MySQLdb, threading
from htmlcrawler import HtmlCrawler

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


def crawler(key, value):
    http = httplib2.Http('.cache', timeout=10)
    test_parser = HtmlCrawler(url_base=url_base, encoding='GB2312', http=http, dir_base=key)
    print('Start decode block: ', key, '...')
    html_content = test_parser.handle_content(url=value)

    # get page num
    page_num = math.ceil(int(re.findall(string=html_content, pattern='<b>([0-9]+)</b>')[0]) / 10)

    for idx in range(page_num):
        # get the news list, 're.DOCTALL' accepts '\r\n'
        print('---Page at: ', idx)
        html_content = test_parser.handle_content(url=value + '&page=' + str(idx + 1))
        if isinstance(html_content, str):
            news_links, news_spam = test_parser.handle_news_list(html=html_content, pattern=re.compile(pattern, re.DOTALL))
            # print('->got links')
            files_path, title_and_img = test_parser.handle_news_files(news_links=news_links, dirs_pa=news_spam)
        else:
            print('->Type is wrong, type: ', type(html_content))
    print(key, 'Done!')


for news_name, url in url_links.items():
    crawler(news_name, url)

# class my_thread(threading.Thread):
#     def __init__(self, key, value):
#         threading.Thread.__init__(self)
#         self.key = key
#         self.value = value

#     def run(self):
#         print('开始线程：', self.key)
#         crawler(self.key, self.value)
#         print('结束线程：', self.key)


# thread_list = []
# [threads.append(my_thread(key, value)) for key, value in url_links.items()]
# [ele.start() for ele in thread_list]
# [ele.join() for ele in thread_list]
