
import requests
from bs4 import BeautifulSoup as bs

import os.path 
import urllib.request
import os
import argparse
import html5lib
import lxml
import requests
from mediawiki import MediaWiki
import json
import unidecode
import csv 

import pandas as pd


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}


WIKI_URL = "https://en.wikipedia.org"
WIKI_API = "https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages&piprop=original&titles="
WIKI_SEARCH = "https://en.wikipedia.org/w/api.php?action=query&&format=json&formatversion=2&list=search&srsearch="



name_list = []
state_list = []
midName_list = []
with open('noBio.csv') as file:
	reader = csv.reader(file, delimiter=",")
	count = 0
	for row in reader:
		if count == 0:
			print(f'Column names are {",".join(row)}')
			count += 1
		else:
			name_list.append(f'{row[1]} {row[0]}')
			midName_list.append(f'{row[2]} {row[3]} {row[4]}')
			state_list.append(row[5])
			
			#print(f'\t{row[2]} first name, {row[1]} last name')
			count += 1


#df.to_csv('names.csv', index=False, sep=',')	

def wikiSearch(name, state):
	wikiSR = requests.get(f'{WIKI_SEARCH}{name[0]} {name[1]}', headers = header).text#{state}', headers = header).text	

	data = json.loads(wikiSR)
	for i in data['query']['search']:
		d = i['title'] 
		snip = i['snippet']
		if name[0] in snip and name[1] in snip and state in snip:
			print(d)
			return(d)
		else:
			return(None)

#1: ones with snip full first full last with state name.


for name, state, mid in zip(name_list, state_list, midName_list):
	try:	
		#wikipedia = MediaWiki()
		#searchName1 = wikipedia.search(name)[0]
		#searchName2 = wikipedia.search(name)[1]
		#searchName3 = wikipedia.search(name)[2]
		#print(f'name: {name} search1: {searchName1} search2: {searchName2} search3: {searchName3}')
		
		listName = name.title().split(' ')
		listMid = mid.title().split(' ')
		#stateUp = state.title()
		d = wikiSearch(listName, state)
		if d is None:
			print("None: "+name)
		else:
			with open(r'Book5.csv', 'a', newline='') as fd:
				fieldnames = ['lname','fname','mid','mid2','mid3','state','wikiTitle']
				writer = csv.DictWriter(fd, fieldnames=fieldnames)
				writer.writerow({'lname':listName[1], 'fname':listName[0], 'mid':listMid[0], 'mid2':listMid[1], 'mid3':listMid[2], 'state':state, 'wikiTitle':d})
			
	except:
		pass#print("None")
