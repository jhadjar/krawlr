"""
	krawlr: the cute crawler.
"""
import re
import requests

__title__ = 'krawlr'
__version__ = '1.0'
__author__ = 'Jugurtha Hadjar'


USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0'
USER_AGENT_ = 'krawlr github.com/jhadjar/krawlr'

RE_SITEMAP_ROBOTS = 'Sitemap: (.+)'
RE_SITEMAP_LINKS = '<loc>(.*?)</loc>'


# TODO: Add a courtesy throttling mechanism.
# TODO: Figure out why requests is taking so long to be imported.
#		I'm not using the full power of requests but fear having
#		to come back to it again if I go the urllib2 route.


def fetch(url, retry=2, user_agent=USER_AGENT):
	"""Fetch a `url` a maximum of `retries`."""

	headers = {'User-Agent': user_agent}
	r = requests.get(url, headers=headers)
	if (200 != r.status_code) and retry > 0:
		fetch(url, retry - 1)
	else:
		return r
	

def parser(pattern, target):
	"""Yield a match for a pattern in a target file or URL."""
	try:
		with open(target, 'r') as f:
			data = f.read()
	except (IOError, AttributeError) as e:
		data = fetch(target).text
	for item in re.findall(pattern, data):
		yield item


def krawl(url):
	for sm in parser(RE_SITEMAP_ROBOTS, url + '/robots.txt'):
		for link in parser(RE_SITEMAP_LINKS, sm):
			yield fetch(link)
	 
