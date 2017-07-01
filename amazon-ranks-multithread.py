from bs4 import BeautifulSoup
import datetime
from concurrent.futures import ThreadPoolExecutor
import sqlite3 as sql
import time
from selenium import webdriver
import re
from pymongo import MongoClient

unix = int(time.time())
date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))
keyword = [line.rstrip('\n') for line in open('keywords.txt')]
keywords = [str.replace(x, ' ', '+') for x in keyword]

# Mongo Settings

client = MongoClient('localhost', 27017)
db = client.Amazon

def ranks(i):
    driver = webdriver.Chrome(executable_path='/Users/willcecil/Dropbox/Python/chromedriver')
    #driver = webdriver.PhantomJS(executable_path='/Users/willcecil/Dropbox/Python/phantomjs')
    url = 'https://www.amazon.co.uk/s/url=search-alias%3Daps&field-keywords=' + i
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source)
    print(
        "Opening this page " + 'https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + i)

    results = soup.findAll('div', attrs={'class': 's-item-container'})
    print(len(results))
    # print(results)
    for a, b in enumerate(results):
        try:
            # print(b)
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

            # Save to dict for multithreading test

            data = dict.fromkeys(['Date', 'Unix', 'Keyword', 'Title', 'Review_Score', 'ASIN', 'Rank', 'URL', 'Prime'])

            data['Date'] = date
            data['Unix'] = unix
            data['Keyword'] = i
            data['Title'] = title
            data['Review_Score'] = score
            data['ASIN'] = ASIN
            data['Rank'] = result
            data['URL'] = url
            data['Prime'] = PRIME

            db.amazon_ranks.insert(data)

        except Exception as e:
            print(e)
    driver.quit()


futures = []

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=1) as ex:
        for keyword in keywords:
            futures.append(ex.submit(ranks, keyword))