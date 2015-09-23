#!/usr/bin/python
import sys
import urllib2
import argparse

#import HTTPError


from bs4 import BeautifulSoup

def main(argv):
	parser = argparse.ArgumentParser(description='Diff properties between two environments.')
	parser.add_argument('src_env', #metavar='N', type=str, nargs='*',
                   help='source environment used in the diff')
	parser.add_argument('dst_env', #metavar='dst', type=str, nargs='*',
                   help='destination environment used in the diff')
	parser.add_argument('--print_all', dest='accumulate', action='store_const',
    	               const=True, default=False,
        	           help='Print all properties')
	args = parser.parse_args()
	#print args.print_all
	#print args.dst_env
	#exit(0)

	src_env = args.src_env
	dst_env = args.dst_env
	PROPERTY_PAGE = "8080/sdp/sdp-admin/admin-service/getPropertiesInfo"
	src_prop = get_properties_by_url('http://{0}:{1}'.format(src_env, PROPERTY_PAGE))
	dst_prop = get_properties_by_url('http://{0}:{1}'.format(dst_env, PROPERTY_PAGE))
	merged_prop = merge_properties(src_prop, dst_prop)
	print_properties_dict(merged_prop) # print_all=args.print_all)
	print "Total {0} properties found in source: {1}".format(len(src_prop), src_env)
	print "Total {0} properties found in destination: {1}".format(len(dst_prop), dst_env)

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
		result[p] = (src[p], dst.get(p, ''))
	for p in dst:
		result[p] = (src.get(p, ''), dst[p])
	return result

def print_properties_dict(properties, print_all=False):
	LINE_DIVIDER = '==========================================='
	for key, val in properties.iteritems():
		if not is_filtered(key, val, print_all=print_all):
			print LINE_DIVIDER
			print "name     : {0}".format(key) 
			print "src value: {0}".format(val[0])
			print "dst value: {0}".format(val[1])
	print LINE_DIVIDER

def is_filtered(prop_name, value, print_all=False):
	'''returns True if the prop_name is supposed to be filtered in the final result. False otherwise'''
	if not print_all:
		if value[0] == value[1]:
			return True #ignore the values that matches
		else:
			return False
	else:
		return False

if __name__ == '__main__':
	main(sys.argv[1:])