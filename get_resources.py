import httplib2, re, chardet


http = httplib2.Http('.cache')


def get_html(url):
	response, content = http.request(url)
	check_dict = chardet.check()