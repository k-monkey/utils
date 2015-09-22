#!/usr/bin/python
import sys
import urllib2
#import HTTPError

from bs4 import BeautifulSoup

def main(argv):
	src_env = argv[0]
	dst_env = argv[1]
	PROPERTY_PAGE = "8080/sdp/sdp-admin/admin-service/getPropertiesInfo"
	src_prop = get_properties_by_url('http://{0}:{1}'.format(src_env, PROPERTY_PAGE))
	dst_prop = get_properties_by_url('http://{0}:{1}'.format(dst_env, PROPERTY_PAGE))
	merged_prop = merge_properties(src_prop, dst_prop)
	print_properties_dict(merged_prop)
	print "Total {0} properties found in source.".format(len(src_prop))
	print "Total {0} properties found in destination.".format(len(dst_prop))

def get_properties_by_url(url):
	'''returns a list of (proerpty: value) as a dict'''
	try:
		content = urllib2.urlopen(url).read()
	except HTTPError as e:
		print "Unable to open URL {0}. error: {1}".format(url, e.strerror)
		return {}
	parser = BeautifulSoup(content)
	tds = [row.findAll('td') for row in parser.findAll('tr')]
	results = { td[0].string: td[1].string for td in tds }
	return results

def merge_properties(src, dst):
	result = {}
	for p in src:
		result[p] = (src[p], dst.get(p, None))
	for p in dst:
		result[p] = (src.get(p, None), dst[p])
	return result

def print_properties_dict(properties):
	LINE_DIVIDER = '==========================================='
	for pro, val in properties.iteritems():
		print LINE_DIVIDER
		print "name     : {0}".format(pro) 
		print "src value: {0}".format(val[0])
		print "dst value: {0}".format(val[1])
	print LINE_DIVIDER

if __name__ == '__main__':
	main(sys.argv[1:])