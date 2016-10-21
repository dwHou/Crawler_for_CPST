import httplib2
import re
from bs4 import BeautifulSoup
import os


ENCODING = 'GB2312'
DIR_BASE = 'news/'


class HtmlCrawler(object):
    def __init__(self, url_base, encoding, http, dir_base):
        """Initialize some parameters

        :param url_base: the base url of a website, which will be used to get some resource
        :param encoding: the encoding used to decode html file
        :param http: a http object used to send request
        :param dir_base: if the news block is 'employment', then dir_base equals 'employment
        """
        self.url_base = url_base
        self.encoding = encoding
        self.http = http
        self.dir_base = dir_base + '/'

    def _handle_save_(self, dir_name, content, files_path, news_title):
        """Handle saving file at a certain catalog

        :param dir_name: dir name
        :param content: the file content, must be bytes
        :param files_path: store file path
        :param news_title: the origin title of news
        :return: none
        """
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, mode=0o777)

        filename = news_title.replace('/', '|')
        # print(filename)
        file_path = dir_name + filename + '.html'
        files_path.append(file_path)

        with open(file_path, 'wb') as f:
            f.write(content)

    def handle_content(self, url):
        """Get content by url

        :type url: str or list
        :param url: the url of a web-page
        :return homepage, str
        """
        response, content = self.http.request(url)
        content = content.decode(self.encoding, 'ignore')
        return content

    def handle_news_list(self, html, pattern):
        """Get news list from a html-page, and split news into two parts:
        news link -- used for get the content of a certain news
        news title and stamp -- used fro get the title and stamp

        :type html: str
        :param html: a homepage which has a news list

        :type pattern: re.compile
        :param pattern: the regression used to parse the content of html, select news list

        :return: news list, each element includes title, spam, link
        """
        news_list = re.findall(string=html, pattern=pattern)  # get news list
        links = []  # store news' link
        news_spam = []  # store news' title and its spam
        # 2016/(0)9/(0)1 (0)1:
        spam_pattern = re.compile(pattern='[0-9]{4}/[0-9]{1,2}/[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}')

        for news in news_list:
            links.append(self.url_base + news[0])  # get the link to news's page
            news_spam.append(spam_pattern.search(news[1]).group(0))
        return links, news_spam

    def handle_news_files(self, news_links, dirs_pa):
        """Get fixed news files and store them in FTP

        :type news_links: a str list
        :param news_links: url oriented to news' page
        :type dirs_pa: str
        :param dirs_pa: the dir parameters used to store news file, but dirs_pa is time spam
        :return: list, file paths
        :return: images_list: a list whose element is image
        """
        files_path = []
        title_and_img = []

        for idx in range(len(news_links)):
            content = self.handle_content(url=news_links[idx])
            # get date, and combine DIR_BASE to get dir path
            dir_name = DIR_BASE + self.dir_base + dirs_pa[idx].split()[0] + '/'
            soup = BeautifulSoup(content, 'html.parser')  # use Beautiful to parse the original page
            if soup.title:
                news_title = soup.title.string
                article = soup.find('table', class_='right_news_lb')  # get the real article part
                article_fix = article.contents[1]  # fix the real article part
                images = article_fix.find_all('img')  # find all img tags from fixed article

                # get image resource, fix the original link, get the real url to image resource
                if len(images) > 0:
                    temp = []
                    for img in images:
                        img_link = self.url_base + img.attrs['src']
                        img.attrs['src'] = img_link
                        temp.append(img_link)

                    title_and_img.append((news_title, temp[0]))
                else:
                    title_and_img.append((news_title, ''))

                self._handle_save_(dir_name, article_fix.prettify('utf-8'), files_path, news_title)
            else:
                redirect_pattern = re.compile('href=\'(.*?)\'')
                redirect_url = re.findall(string=content, pattern=redirect_pattern)[0]
                r, c = self.http.request(redirect_url)
                c = c.decode('gb2312', 'ignore')
                soup2 = BeautifulSoup(c, 'html.parser')
                if soup2.title:
                    news_title = soup2.title.string
                else:
                    news_title = 'Inner News'
                c1 = '<h1 style=\"text-align: center\">对不起！您访问的链接已损坏，或者需要校园网访问！</h1>'
                c2 = '<a style=\"text-align: center; display: block\" href=\"' + redirect_url + '\">确定接入校园网后，点击此处访问</a>'
                self._handle_save_(dir_name, (c1 + c2).encode(), files_path, news_title)
                title_and_img.append((news_title, ''))

        return files_path, title_and_img
