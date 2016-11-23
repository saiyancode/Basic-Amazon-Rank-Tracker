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
from selenium import webdriver
import re

#Settings
# directory = '/Users/willcecil/Desktop/Amazon-Scraper/Amazon-Scraper'
# os.chdir(directory)

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
    c.execute("CREATE TABLE IF NOT EXISTS amazon_rankings(datestamp TEXT, title TEXT, stars REAL, ASIN TEXT, Url TEXT, Prime TEXT)")
create_table()

# def prime(soup):

# def stars(soup):



# Not Working Need to use headless Browser
def ranks():
	for i in keywords:
		#driver = webdriver.Chrome(executable_path=r'C:\Users\w.cecil\Python35\chromedriver.exe')
		driver = webdriver.Chrome(executable_path='/Users/willcecil/Dropbox/Python/chromedriver')
		#driver = webdriver.PhantomJS(executable_path=r'C:\Users\w.cecil\Python35\phantomjs-2.1.1-windows\bin\phantomjs.exe') # or add to your PATH
		url = 'https://www.amazon.co.uk/s/url=search-alias%3Daps&field-keywords='+i
		driver.get(url)
		time.sleep(5)
		soup = BeautifulSoup(driver.page_source)
		print("Opening this page " + 'https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='+i)
		# try:
		# 	NAME = '//*[@id="result_0"]/div/div[3]/div[1]/a/h2//text()'

		# 	RAW_NAME = driver.get_element_by_xpath(NAME)

		try:
		    results = soup.findAll('div',attrs={'class':'s-item-container'})
		    print(len(results))
		    #print(results)
		    for a,b in enumerate(results):
		    	#print(b)
		    	soup = b
		    	header = soup.find('h2')
		    	result = a
		    	title = header.text.encode('utf-8')
		    	link = soup.find('a',attrs={'class':'a-link-normal s-access-detail-page  a-text-normal'})
		    	url = link['href']
		    	print(title)
		    	print(url)
		    	price = None
		    	link = None
		    	ASIN =None
		    	PRIME = None
		    	stars = None
		    	# c.execute("INSERT INTO amazon_rankings VALUES (?, ?, ?,?, ?, ?)",
       #                    (date, title, stars, ASIN, result, PRIME))

		except Exception as e:
		    print(e)
		driver.quit()



ranks()
conn.close()