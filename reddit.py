#!/usr/bin/env python2.7

import re
import requests
import os
import sys

# default variables
FIELD = 'title'
LIMIT = 10
SUBREDDIT = 'linux'
regexSearch = False

# functions
def usage(status = 0):
	print '''Usage: reddit.py [ -f FIELD -s SUBREDDIT ] regex
		-f FIELD	Which FIELD to search (default: title)
		-n LIMIT	Limit number of articles to report (default: 10)
		-s SUBREDDIT	Which subreddit to search (default: linux)'''
	sys.exit(status)

# command line arguments
args = sys.argv[1:]
while len(args) and args[0].startswith('-') and len(args[0]) > 1:
	arg = args.pop(0)
	if arg == '-h':
		usage(0)
	elif arg == '-f':
		FIELD = args.pop(0)
	elif arg == '-n':
		LIMIT = int(args.pop(0))
	elif arg == '-s':
		SUBREDDIT = args.pop(0)
	else:
		usage(1)
if len(args) > 0:
	regex = args.pop(0)
else:
	regex = ''

headers = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}

# main execution
response = requests.get('https://www.reddit.com/r/{}/.json'.format(SUBREDDIT), headers=headers)
content = response.json()
index = 0
for items in content['data']['children']:
	if index < LIMIT:
		if FIELD not in items['data']:
			print 'Invalid field: {}'.format(FIELD)
			sys.exit(1)
		if re.search(regex, items['data'][FIELD]):
			print '{:>2}'.format(index+1) + '. Title:  ', items['data']['title']
			print '    Author: ', items['data']['author']
			print '    Link:   ', 'https://www.reddit.com' + items['data']['permalink'], '\n'
			index += 1
