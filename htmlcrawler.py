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
        links = []  # store news' link
        news_title_spam = []  # store news' title and its spam

        # for each news in news_list, we need get some resource of this news
        # such as images related to this news, and the article
        # the structure of news: news[0] -- link to article, news[1] -- title and spam
        for news in news_list:
            links.append(self.url_base + news[0])  # get the link to news's page
            news_title_spam.append(news[1])
        return links, news_title_spam

    def handle_news_files(self, news_links, dir):
        """

        :type news_links: a str list
        :param news_links: url oriented to news' page
        :type dir: str
        :param dir: the dir used to store news file
        :return: list, file paths
        :return: images_list: a list whose element is image
        """
        x_content = self.handle_content(http=httplib2.Http(), url=news_links, url_type='list')  # get content of news' page
        idx = 0
        files_path = []
        image_links = []

        for content in x_content:
            soup = BeautifulSoup(content, 'html.parser')  # use Beautiful to parse the original page
            # news_title = soup.title.string

            article = soup.find('table', class_='right_news_lb')  # get the real article part
            article_fix = article.contents[1]  # fix the real article part
            images = article_fix.find_all('img')  # find all img tags from fixed article

            # get image resource
            if len(images) > 0:
                # fix the original link, get the real url to image resource
                temp = []
                for img in images:
                    img_link = self.url_base + img.attrs['src']
                    img.attrs['src'] = img_link
                    temp.append(img_link)

                image_links.append(temp[0])
            else:
                image_links.append('')

            file_path = dir + 'article_x' + str(idx) + '.html'
            files_path.append(file_path)

            with open(file_path, 'wb') as f:
                f.write(article_fix.prettify('utf-8'))
            idx += 1

        return files_path, image_links
