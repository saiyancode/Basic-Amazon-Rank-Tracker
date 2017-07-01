# Amazon Simple Rank Tracker

I needed to scrape some data in order to understand performance of products on Amazon. This script has two versions, one which uses Mongodb and is multithreaded and another which is single threaded and exports to sqlite. 

# Requirements

  - Chrome or PhantomJS drivers
  - Selenium & BeautifulSoup, MongoDB if using the multithread version

# Setup

The setup requires you to install these libraries if you've not got them

```sh
$ pip install selenium
$ pip install beautifulsoup4
```
The you'll need to update the keyword list within the keywords.txt file

```sh
conn = sql.connect(r'Rankings-test.db') # this can be changed to rename the database
driver = webdriver.Chrome(executable_path='/Users/willcecil/Dropbox/Python/chromedriver') # this needs to be updated to your driver location
```
Having done that everything should run as planned. 

Install guides for monogodb
[Install Mongo on MacOSX](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/) 

Any questions hit me up on twitter (@willceciltech) or open an issue!
