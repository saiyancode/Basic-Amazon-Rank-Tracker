from random import choice
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import datetime
from concurrent.futures import ThreadPoolExecutor
import sqlite3 as sql
import time
from selenium import webdriver
import re
from collections import defaultdict
import pymongo
from pymongo import MongoClient
from threading import Thread

# Mongo Settings

client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.test_collection


unix = int(time.time())
date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))
keyword = [line.rstrip('\n') for line in open('keywords.txt')]
keywords = [str.replace(x,' ','+') for x in keyword]
AgentList = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
             "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17",
             "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0"]
conn = sql.connect(r'Rankings-multi.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS multi(datestamp TEXT, unix TEXT, Keyword TEXT, title TEXT, stars REAL, ASIN TEXT, rank TEXT, url TEXT, Prime TEXT)")
create_table()

data = defaultdict(list)

def ranks(i):
	#driver = webdriver.Chrome(executable_path='/Users/willcecil/Dropbox/Python/chromedriver')
	driver = webdriver.PhantomJS(executable_path='/Users/willcecil/Dropbox/Python/phantomjs')
	url = 'https://www.amazon.co.uk/s/url=search-alias%3Daps&field-keywords='+i
	driver.get(url)
	time.sleep(1)
	soup = BeautifulSoup(driver.page_source)
	print("Opening this page " + 'https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='+i)

	try:
	    results = soup.findAll('div',attrs={'class':'s-item-container'})
	    print(len(results))
	    #print(results)
	    for a,b in enumerate(results):
	    	#print(b)
	    	soup = b
	    	header = soup.find('h2')
	    	result = a + 1
	    	title = header.text
	    	link = soup.find('a',attrs={'class':'a-link-normal s-access-detail-page  a-text-normal'})
	    	url = link['href']
	    	url = re.sub(r'/ref=.*', '',str(url))

	    	# Extract the ASIN from the URL
	    	ASIN = re.sub(r'.*amazon.co.uk.*/dp/', '',str(url))

	    	# Extract Score Data using ASIN number to find the span class

	    	score = soup.find('span',attrs={'name':ASIN})
	    	try:
	    		score = score.text
	    		score = score.strip('\n')
	    		score = re.sub(r' .*', '',str(score))
	    	except:
	    		score = None

	    	# Extract Number of Reviews in the same way
	    	reviews = soup.find('a', href=re.compile(r'.*#customerReviews'))
	    	try:
	    		reviews = reviews.text
	    	except:
	    		reviews = None

	    	# And again for Prime

	    	PRIME = soup.find('i',attrs={'aria-label':'Prime'})
	    	try:
	    		PRIME = PRIME.text
	    	except:
	    		PRIME = None

	    	# Test Statements
	    	# print(title.decode('utf-8'))
	    	# print(url)
	    	# print(ASIN)
	    	# print(reviews)
	    	# print(prime)

	    	# Save to dict for multithreading test

	    	data = defaultdict(list)

	    	data['Date'].append(date)
	    	data['Unix'].append(unix)
	    	data['Keyword'].append(i)
	    	data['Title'].append(title)
	    	data['Review_Score'].append(score)
	    	data['ASIN'].append(ASIN)
	    	data['Rank'].append(result)
	    	data['URL'].append(url)
	    	data['Prime'].append(PRIME)

	    	db.collection.insert(data)

	    	#c.execute("INSERT INTO multi VALUES (?,?, ?, ?,?, ?, ?,?,?)",
            #          (date, unix, i ,title, score, ASIN, result, url, PRIME))
	    	#conn.commit()
	except Exception as e:
	    print(e)
	driver.quit()

futures = []
with ThreadPoolExecutor(max_workers=3) as ex:
    for keyword in keywords:
        futures.append(ex.submit(ranks,keyword))

conn.close()