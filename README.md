# Amazon Simple Rank Tracker

I needed to scrape some data in order to understand performance of products on Amazon. This script has two versions, one which uses Mongodb and is multithreaded and another which is single threaded and exports to sqlite. 

# Requirements

  - Chrome or PhantomJS drivers
  - Selenium & BeautifulSoup

# Setup

The setup requires you to install these libraries if you've not got them

```sh
$ pip install selenium
$ pip install beautifulsoup4
```
The you'll need to update the keyword list within the keywords.txt file

```sh
driver = webdriver.Chrome(executable_path='/Users/willcecil/Dropbox/Python/chromedriver') # this needs to be updated to your driver location
```
Having done that everything should run as planned. 

You will need to edit the keywords.txt file and add your keywords one per line

This is configured for Amazon UK in this example but if you change the domain to another market e.g. .com it will run there too!

Any questions hit me up on twitter (@willceciltech) or open an issue!
