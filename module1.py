import httplib2
import re
from htmlcrawler import HtmlCrawler

# crawler test module
url_links = {
    'news': 'http://physics.scu.edu.cn/News/index.asp?ClassID=3',
    'notice': 'http://physics.scu.edu.cn/News/index.asp?ClassID=1',
    'recruit': 'http://physics.scu.edu.cn/News/index.asp?ClassID=16',
    'employment': 'http://physics.scu.edu.cn/News/index.asp?ClassID=15'
}


url_base = 'http://physics.scu.edu.cn'
pattern = '<a href=\"(/News/news_show\.asp\?ArticleID=[0-9]+)\" title=\"(.*?)\">'
http = httplib2.Http('.cache')

# initialize the Html parser
test_parser = HtmlCrawler(url_base=url_base, encoding='GB2312')

# get the main page of a certain block, such this: News
# you can select: 'Notice', 'Recruit', 'Employment'
html_content = test_parser.handle_content(http=http, url=url_links['news'])

# get the news list
news_link_list = test_parser.handle_news_list(html=html_content, pattern=re.compile(pattern, re.DOTALL))

# scan the news list, and store news files
test_parser.handle_news_files(news_links=news_link_list)


# database operations test module







