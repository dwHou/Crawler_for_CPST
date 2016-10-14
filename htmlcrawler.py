import httplib2
import re
from bs4 import BeautifulSoup


ENCODING = 'GB2312'


class HtmlCrawler(object):
    def __init__(self, url_base, encoding):
        """

        :param url_base: the base url of a website, which will be used to get some resource
        :param encoding: the encoding used to decode html file
        """
        self.url_base = url_base
        self.encoding = encoding

    def handle_content(self, http, url, url_type='str'):
        """

        :type http: httplib2.Http()
        :param http: a http object

        :type url: str or list
        :param url: the url of a web-page

        :type url_type: str
        :param url_type: point that the type of url: str or list
        :return homepage
        """

        if url_type == 'list':
            homepage = []
            for ele in url:
                response, content = http.request(ele)
                homepage.append(content.decode(self.encoding))
        else:
            response, homepage = http.request(url)
            homepage = homepage.decode(self.encoding)

        return homepage

    def handle_news_list(self, html, pattern):
        """

        :type html: str
        :param html: a homepage which has a news list

        :type pattern: re.compile
        :param pattern: the regression used to parse the content of html, select news list

        :return: news list, each element includes title, spam, link
        """
        news_list = re.findall(string=html, pattern=pattern)  # get news list
        idx = 0  # index of a certain, also a calculator
        link = ''

        # for each news in news_list, we need get some resource of this news
        # such as images related to this news, and the article
        # the structure of news: news[0] -- link to article, news[1] -- title and spam
        for news in news_list:
            link = self.url_base + news[0]  # get the link to news's page
        return news_list

    def handle_news_files(self, news_links):
        """

        :type news_links: a str list
        :param news_links: url oriented to news' page
        :return: news_files: a news file which file type is HTML,
        :return: images_list: a list whose element is image
        """
        x_content = self.handle_content(news_links, url_type='list')  # get content of news' page
        idx = 0

        for content in x_content:
            soup = BeautifulSoup(content, 'html.parser')  # use Beautiful to parse the original page
            # news_title = soup.title.string

            article = soup.find('table', class_='right_news_lb')  # get the real article part
            article_fix = article.contents[1]  # fix the real article part
            img_link = []  # list which used to store the image resource, some links
            images = article_fix.find_all('img')  # find all img tags from fixed article

            # get image resource
            if images is not None:
                # fix the original link, get the real url to image resource
                for img in images:
                    img.attrs['src'] = self.url_base + img.attrs['src']
                    img_link.append(img.attrs['src'])

            file_name = 'article_x' + str(idx) + '.html'
            with open(file_name, 'w') as f:
                f.write(content)


