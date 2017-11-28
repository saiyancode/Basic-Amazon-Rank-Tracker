from bs4 import BeautifulSoup
import time
from selenium import webdriver
import re
import datetime
from collections import deque
import logging
import csv


class AmazonScaper(object):

    def __init__(self,keywords, output_file='example.csv',sleep=2):

        self.browser = webdriver.Chrome(executable_path='/Users/willcecil/Dropbox/Python/chromedriver')  #Add path to your Chromedriver
        self.keyword_queue = deque(keywords)  #Add the start URL to our list of URLs to crawl
        self.output_file = output_file
        self.sleep = sleep
        self.results = []


    def get_page(self, keyword):
        try:
            self.browser.get('https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords={a}'.format(a=keyword))
            return self.browser.page_source
        except Exception as e:
            logging.exception(e)
            return

    def get_soup(self, html):
        if html is not None:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else:
            return

    def get_data(self,soup,keyword):

        try:
            results = soup.findAll('div', attrs={'class': 's-item-container'})
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
                    url = "None"

                # Extract the ASIN from the URL - ASIN is the breaking point to filter out if the position is sponsored

                ASIN = re.sub(r'.*amazon.co.uk.*/dp/', '', str(url))

                # Extract Score Data using ASIN number to find the span class

                score = soup.find('span', attrs={'name': ASIN})
                try:
                    score = score.text
                    score = score.strip('\n')
                    score = re.sub(r' .*', '', str(score))
                except:
                    score = "None"

                # Extract Number of Reviews in the same way
                reviews = soup.find('a', href=re.compile(r'.*#customerReviews'))
                try:
                    reviews = reviews.text
                except:
                    reviews = "None"

                # And again for Prime

                PRIME = soup.find('i', attrs={'aria-label': 'Prime'})
                try:
                    PRIME = PRIME.text
                except:
                    PRIME = "None"

                data = {keyword:[keyword,str(result),title,ASIN,score,reviews,PRIME,datetime.datetime.today().strftime("%B %d, %Y")]}
                self.results.append(data)

        except Exception as e:
            print(e)

        return 1

    def csv_output(self):
        keys = ['Keyword','Rank','Title','ASIN','Score','Reviews','Prime','Date']
        print(self.results)
        with open(self.output_file, 'a', encoding='utf-8') as outputfile:
            dict_writer = csv.DictWriter(outputfile, keys)
            dict_writer.writeheader()
            for item in self.results:
                for key,value in item.items():
                    print(".".join(value))
                    outputfile.write(",".join('"' + item + '"' for item in value)+"\n") # Add "" quote character so the CSV accepts commas

    def run_crawler(self):
        while len(self.keyword_queue): #If we have keywords to check
            keyword = self.keyword_queue.popleft() #We grab a keyword from the left of the list
            html = self.get_page(keyword)
            soup = self.get_soup(html)
            time.sleep(self.sleep) # Wait for the specified time
            if soup is not None:  #If we have soup - parse and save data
                self.get_data(soup,keyword)
        self.browser.quit()
        self.csv_output() # Save the object data to csv


if __name__ == "__main__":
    keywords = [str.replace(line.rstrip('\n'),' ','+') for line in open('keywords.txt')] # Use our file of keywords & replaces spaces with +
    ranker = AmazonScaper(keywords) # Create the object
    ranker.run_crawler() # Run the rank checker


