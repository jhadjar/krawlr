"""
	krawlr: the cute crawler.
"""
import re
import time

import requests

__title__ = 'krawlr'
__version__ = '1.0'
__author__ = 'Jugurtha Hadjar'
__copyright__ = 'Copyright 2016'

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0'
USER_AGENT_ = 'krawlr github.com/jhadjar/krawlr'

RE_SITEMAP_ROBOTS = 'Sitemap: (.+)'
RE_SITEMAP_LINKS = '<loc>(.*?)</loc>'


# TODO: Add a courtesy throttling mechanism.
# TODO: Figure out why requests is taking so long to be imported.
#		I'm not using the full power of requests but fear having
#		to come back to it again if I go the urllib2 route.

# QUESTION: Should I use Chunk-Encoded Requests to get a stream?
#			I've seen sitemaps that are about 10MB. Is it better
#			to receive and parse chunks for links instead of 
#			downloading the whole thing and then parsing?

def throttle(func, delay=1):
	"""Throttle func by delay seconds"""
	def wrapper(*args, **kwargs):
		time.sleep(delay)
		return func(*args, **kwargs)
	return wrapper


@throttle
def fetch(url, user_agent=USER_AGENT):
	"""Use session to fetch a url."""
	headers = {'User-Agent': user_agent}

	with requests.Session() as s:
		try:
			r = s.get(url, headers=headers)
			yield r
		except Exception as e:
			print "{}".format(e)
			yield None


def readfile(filename):
	"""Read a file line by line"""
	try:
		with open(filename) as f:
			for line in f:
				yield line
	except IOError as e:
		print "{}".format(e)

def parse(data, pattern):
	"""Parse data looking for pattern."""
	for item in re.findall(pattern, data):
		yield item

		
def crawl_from_robots(url):
	try:
		robots = next(fetch(url + '/robots.txt')).text
	except AttributeError:
		print "The url does not have a robots.txt file"
		return
	sitemap_links = parse(robots, RE_SITEMAP_ROBOTS)

	for sitemap_link in sitemap_links:
		sitemap = next(fetch(sitemap_link)).text
		links = parse(sitemap, RE_SITEMAP_LINKS)

		for link in links:
			resource = next(fetch(link))
			print link, resource.status_code
