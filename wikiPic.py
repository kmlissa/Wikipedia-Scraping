#!/usr/bin/env python
# coding: utf-8



import requests
from bs4 import BeautifulSoup as bs
# from os.path  import basename
import os.path 

import urllib.request
import os
import argparse
import html5lib
import lxml
import time
import math
# import urllib2
import requests#K
from mediawiki import MediaWiki
import json
import re
import unidecode
import csv
import pandas as pd

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

WIKI_API = "https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages&piprop=original&titles="
WIKI_SEARCH = "https://en.wikipedia.org/w/api.php?action=query&&format=json&formatversion=2&list=search&srsearch="

name_list = []
state_list = []
other_name = []
other_name2 = []

#get name/aliases and state from csv file
with open('uniqueName.csv', encoding="utf8") as file:
	reader = csv.reader(file, delimiter=",")
	count = 0
	
	for row in reader:
		if count == 0:
			#print(f'Column names are {",".join(row)}')
			count += 1
		else:
			name_list.append(f'{row[101]}')
			state_list.append(f'{row[2]}')
			other_name.append(f'{row[104]}')
			other_name2.append(f'{row[109]} {row[110]}')
			count += 1
		"""
			if row[114] is None or "NA":
				if row[116] is
				name_list.append(f'{row[110]} {row[109]}')
			else:	
				name_list.append(f'{row[110]} {row[114]} {row[109]}')
			state_list.append(f'{row[2]}')
			count += 1
		"""
		
#search wiki title for pic source
def wikiSearch(name, state, other, other2):
	listName = name.split(' ')
	wikipedia = MediaWiki()
	search = wikipedia.search(name +" "+ state)
	if search:
		searchName = search[0]
		if len(listName) is 1:
			listName = other.split(' ')
			if len(listName) is 1: 
				listName = other2.split(' ')
		if wikiS(listName, searchName, state.lower()):
			wikiSR = requests.get(WIKI_API + searchName, headers = header).text	
			d = json.loads(wikiSR)
			for i in d['query']['pages']:
				if 'original' in i.keys():
					return i['original']['source']
				else:
					return None	
			 
		
#get wiki title based on name
def wikiS(name, searchName, state):
	name[0] = name[0].lower().replace(",", "")
	name[1] = name[1].lower().replace(",", "")
	
	wikiSR = requests.get(WIKI_SEARCH + searchName, headers = header).text	
	data = json.loads(wikiSR)
	
	for i in data['query']['search']:
		snip = i['snippet'].lower()
		d = i['title']
		if name[0] in snip and name[1] in snip and (state in snip or "politician" in snip):
			return(d)
		else:
			return(None)
	#wikiSR = requests.get(f'{WIKI_SEARCH}{name[0]} {name[1]}', headers = header).text
	##wikiSR = requests.get(WIKI_SEARCH + searchName, headers = header).text	
	#data = json.loads(wikiSR)
	

#insert picture into folders based on state
for name, state, other, other2 in zip(name_list, state_list, other_name, other_name2):
	
	path = r'.\wiki3\{0}'.format(state)
	if not os.path.exists(path):
		os.makedirs(path)
		
	src = wikiSearch(name, state,other, other2)
	print(f'{name} ***{src}***')
	
	filename = name.replace("’"," ").replace("."," ").replace(","," ").replace("”"," ").replace("\n", " ").replace("'", " ").replace(" ", "_").title()
	if filename[-1] in "_":
		filename = filename[:-1]
	
	
	unaccented_string = unidecode.unidecode(filename)
	clean = re.sub(r'[\W]+', '', unaccented_string)
	file = r"{0}\{1}.jpg".format(path, clean)
	if src:
		with open(file.replace("__","_").replace("\"", " " ,1), "wb") as f:
			response = requests.get(src, headers = header)
			f.write(response.content)
	
	
"""
def wikiSearch(title):
    wikiSR = requests.get(WIKI_API+ title, headers = header).text	
    d = json.loads(wikiSR)
    for i in d['query']['pages']:
        if 'original' in i.keys():
            src = i['original']['source']
        else:
            src = None				

    return src
	
	

#os.makedirs(path)	

for title, state in zip(wikiTitleList, state_list):
	path = r'.\wiki\{0}'.format(state)
	if not os.path.exists(path):
		os.makedirs(path)
		
	src = wikiSearch(title)
	name = title.replace("’"," ").replace("."," ").replace("”"," ").replace("\n", " ").replace("'", " ").replace(" ", "_")
	if name[-1] in "_":
		name = name[:-1]
	unaccented_string = unidecode.unidecode(name)
	clean = re.sub(r'[\W]+', '', unaccented_string)
	filename = r"{0}\{1}.jpg".format(path, clean)
	with open(filename.replace("__","_").replace("\"", " " ,1), "wb") as f:
		if src:
			response = requests.get(src, headers = header)
			f.write(response.content)
		else: pass
"""
