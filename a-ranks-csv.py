from random import choice
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
import pandas.io.sql as pd_sql
from concurrent.futures import ThreadPoolExecutor
import sqlite3 as sql
import time
from selenium import webdriver
import re

unix = int(time.time())
date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))
keyword = [line.rstrip('\n') for line in open('keywords.txt')]
keywords = [str.replace(x, ' ', '+') for x in keyword]
conn = sql.connect(r'Rankings-test.db')
c = conn.cursor()


def create_table():
    c.execute(
        "CREATE TABLE IF NOT EXISTS amazon_rankings(datestamp TEXT, unix TEXT, Keyword TEXT, title TEXT, stars REAL, ASIN TEXT, rank TEXT, url TEXT, Prime TEXT)")


create_table()


def ranks():
    for i in keywords:
        # driver = webdriver.Chrome(executable_path=r'C:\Users\w.cecil\Python35\chromedriver.exe')
        driver = webdriver.Chrome(executable_path='/Users/willcecil/Dropbox/Python/chromedriver')
        # driver = webdriver.PhantomJS(executable_path=r'C:\Users\w.cecil\Python35\phantomjs-2.1.1-windows\bin\phantomjs.exe') # or add to your PATH
        # driver = webdriver.PhantomJS(executable_path=r'C:\Users\w.cecil\Python35\phantomjs-2.1.1-windows\bin\phantomjs.exe') # or add to your PATH
        url = 'https://www.amazon.co.uk/s/url=search-alias%3Daps&field-keywords=' + i
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source)
        print(
            "Opening this page " + 'https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + i)

        try:
            results = soup.findAll('div', attrs={'class': 's-item-container'})
            print(len(results))
            # print(results)
            for a, b in enumerate(results):
                soup = b
                header = soup.find('h2')
                result = a + 1
                title = header.text
                try:
                    link = soup.find('a', attrs={'class': 'a-link-normal a-text-normal'})
                    url = link['href']
                    url = re.sub(r'/ref=.*', '', str(url))
                except:
                    url = None

                print(url)

                # Extract the ASIN from the URL - ASIN is the breaking point to filter out if the position is sponsored

                ASIN = re.sub(r'.*amazon.co.uk.*/dp/', '', str(url))

                # Extract Score Data using ASIN number to find the span class

                score = soup.find('span', attrs={'name': ASIN})
                try:
                    score = score.text
                    score = score.strip('\n')
                    score = re.sub(r' .*', '', str(score))
                except:
                    score = None

                # Extract Number of Reviews in the same way
                reviews = soup.find('a', href=re.compile(r'.*#customerReviews'))
                try:
                    reviews = reviews.text
                except:
                    reviews = None

                # And again for Prime

                PRIME = soup.find('i', attrs={'aria-label': 'Prime'})
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
                c.execute("INSERT INTO amazon_rankings VALUES (?,?, ?, ?,?, ?, ?,?,?)",
                          (date, unix, i, title, score, ASIN, result, url, PRIME))
                conn.commit()
        except Exception as e:
            print(e)
        driver.quit()


ranks()

conn.close()
