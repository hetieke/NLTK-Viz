#!/usr/local/bin/python2.7

import urllib2 
import base64 
import xml.etree.ElementTree as ET 
import HTMLParser
import csv
import codecs
import sys

def get_olab_root(username,password,start_date,end_date,type,realm):
	try:

		# example request string req_string =
		# 'https://webservice.opinionlab.com/display/?start_date=2013-08-14&
		# end_date=2013-08-15&type=domain&realm=www.hotwire.com&xml_style=2'
		# 
		# insert parameters into request string
		req_string ='https://webservice.opinionlab.com/display/?start_date=%s&end_date=%s&type=%s&realm=%s&xml_style=2' % (start_date, end_date, type, realm)

		# construct request with auth headers source:
		# http://stackoverflow.com/questions/635113/python-urllib2-basic-http-
		# authentication-and-tr-im
		request = urllib2.Request(req_string) 
		base64string=base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % base64string)

		# make request
		result = urllib2.urlopen(request)

		# read request
		data = result.read()

		# print 'data', data

		# parse XML into ElementTree
		root = ET.fromstring(data)

		# h = HTMLParser.HTMLParser()

		# read through data elements and print out items
		# for element in root.findall('.//data'): 	
		# 	urltext = element.findall('url')
		# 	for item in urltext:		
		# 		print 'item', item.text
	
	
		# 	comment=str(unicode(element.findall(".//comments")[0].text))
		# 	print 'type',type(urltext)
		# 	print 'type',type(comment)
		# 	
		# 	nested_list=[urltext,comment]
		# 	f.write('\t'.join(i) + '\n' for i in nested_list)
	
	
		# 	print "*" * 40 
		# 	print 'comment ID: ' + element.get('id') 
		# 	print 'comment text: '
		# 	# use xpath to get to the different parts of the comments returns a
		# 	# list - just take the first thing and print it
		# 	print 
		# 	# decode URL and then decode HTML ;amps
		# 	print h.unescape(urllib2.unquote(urltext))

		# f.close()
	
		return root

	except:
		e = sys.exc_info()[0]
		el=sys.exc_traceback.tb_lineno
		print 'Error: %s' % e 
		print 'lineno: %s' % el	
