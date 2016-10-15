import httplib2
import re
from htmlcrawler import HtmlCrawler
import MySQLdb

# crawler test module

# url links
# these links are the diferent news blocks' url
url_links = {
    'news': 'http://physics.scu.edu.cn/News/index.asp?ClassID=3',
    'notice': 'http://physics.scu.edu.cn/News/index.asp?ClassID=1',
    'recruit': 'http://physics.scu.edu.cn/News/index.asp?ClassID=16',
    'employment': 'http://physics.scu.edu.cn/News/index.asp?ClassID=15'
}


url_base = 'http://physics.scu.edu.cn'  # to get some image source
pattern = '<a href=\"(/News/news_show\.asp\?ArticleID=[0-9]+)\" title=\"(.*?)\">'  # pattern used to get news_list
http = httplib2.Http('.cache')  # http object, use cache server

# initialize the Html parser
test_parser = HtmlCrawler(url_base=url_base, encoding='GB2312')

# get the main page of a certain block, such this: News
# you can select: 'Notice', 'Recruit', 'Employment'
html_content = test_parser.handle_content(http=http, url=url_links['news'])

# get the news list
news_links, news_title = test_parser.handle_news_list(html=html_content, pattern=re.compile(pattern, re.DOTALL))
news_title = [(ele.split('\r\n')) for ele in news_title]
news_title = [(e[0][5:], e[1][5:]) for e in news_title]  # element type is tuple(news_tiltle, datetime)

# scan the news list, and store news files
files_path, image_links = test_parser.handle_news_files(news_links=news_links, dir='/Users/zhouming/Desktop/temp/')
print(files_path)
print(image_links)
# combine news_links with file url


# database operations test module
conn = MySQLdb.connect(host='localhost', user='root', passwd='961727', db='crawler')
conn.set_character_set('utf8')
cursor = conn.cursor()
for i in range(len(files_path)):
    cursor.execute('insert into article(news_title, news_date, news_url, img_url) values(%s,%s,%s,%s)',
                   [news_title[i][0], news_title[i][1], files_path[i], image_links[i]])
conn.commit()
cursor.close()
conn.close()