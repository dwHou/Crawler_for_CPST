import httplib2, re, chardet


http = httplib2.Http('.cache')

pattern_dict = {
        'news': '<a href=\"(/News/news_show\.asp\?ArticleID=[0-9]+)\" title=\"(.*?)\">'
        }

def get_html(url):
    response, content = http.request(url)
    check_dict = chardet.detect(content)
    content_de = content.decode(check_dict['encoding'])
    return content_de


def get_content(html, pattern):
    pattern = re.compile(pattern, re.DOTALL)
    content = re.findall(string=html, pattern=pattern)
    return content


if __name__ == '__main__':
    import sys
    url = sys.argv[1]
    print(url)
    html = get_html(url)
    content = get_content(html, pattern_dict['news'])

    num = len(content)
    for i in range(num):
        print('News #{0}\nlink: {1}\n{2}\n'.format(i, url + content[i][0], content[i][1]))



