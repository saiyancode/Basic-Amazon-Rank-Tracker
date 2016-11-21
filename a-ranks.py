from random import choice
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import csv
import datetime
import pandas as pd
import numpy as np
import pandas.io.sql as pd_sql
from concurrent.futures import ThreadPoolExecutor
import sqlite3 as sql
import time
import os

#Settings
directory = '/Users/willcecil/Desktop/Amazon-Scraper/Amazon-Scraper'
os.chdir(directory)
unix = int(time.time())
date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))
keyword = [line.rstrip('\n') for line in open('keywords.txt')]
keywords = [str.replace(x,' ','+') for x in keyword]
AgentList = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
             "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17",
             "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0"]
conn = sql.connect(r'Rankings.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS amazon_rankings(unix REAL, datestamp TEXT, title TEXT, description TEXT, status REAL, canonical TEXT, h1 TEXT, meta_robots TEXT, accessibility TEXT, body TEXT, hreflang TEXT)")
#create_table()

# Not Working Need to use headless Browser
def ranks():
	for i in keywords:
		userAgent = choice(AgentList)
		headers = {'User-Agent':userAgent}
		response = requests.get('https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords'+i,headers=headers,timeout=50)
		page_text = response.text.encode('utf-8')
		print(page_text)
		try:
			soup = BeautifulSoup(page_text, 'html')
			results = soup.findAll(attrs={"id" : "s-results-list-atf"})
			print(len(results))

		except Exception as e:
			print(e)

ranks()
