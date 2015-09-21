#!/usr/bin/python
import sys
import urllib2
#import HTTPError

from bs4 import BeautifulSoup

def main(argv):
	src_env = argv[0]
	dst_env = argv[1]
	PROPERTY_PAGE = "8080/sdp/sdp-admin/admin-service/getPropertiesInfo"
	properties = get_properties_by_url('http://{0}:{1}'.format(src_env, PROPERTY_PAGE))
	print_properties_dict(properties)
	print "Total {0} properties found.".format(len(properties))

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

def print_properties_dict(properties):
	#properties.iteritems()
	for pro, val in properties.iteritems():
		print "{0}: {1}".format(pro, val) #properties[pro])

if __name__ == '__main__':
	main(sys.argv[1:])