import numpy as np
import pandas as pd
import requests
import time
import csv
from bs4 import BeautifulSoup
import lxml
import html5lib
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import scipy as sp
from datetime import date
import random as rand
import os


pd.options.mode.chained_assignment = None
today = date.today()

url1 = requests.get("https://script.google.com/macros/s/AKfycbz6ZauINGIoDCZIUrRO8MsRCa2kq0ur-1UatuSobcxIpijHZMTPh8Lqwepqsd1THGuBhg/exec?action=url1").json()[1318:1537]
url = []


for i in list(range(0,199)):
    url.append(url1[i]['URL'])

url_custome = []
for _url in url:
    for page in list(range(0,199)):
        _url_ = str(_url)+'/user-reviews?page='+str(page)
        url_custome.append(_url_)

review_dict = {'game':[], 'name':[], 'date':[], 'rating':[], 'review':[]}


for page in url_custome:
    _page = str(_url)+'/user-reviews?page='+str(page)
    user_agent = {'User-agent': 'Mozilla/5.0'}
    response  = requests.get(_page, headers = user_agent)
    headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    time.sleep(rand.randint(3,30)) 
    soup = BeautifulSoup(response.text, 'html.parser')
    for review in soup.find_all('div', class_='review_content'):
        
        if review.find('div', class_='name') == None:
                    break 
        if review.find('div', class_='product_title') == None:
            review_dict['game'].append(_page)
        else:
            review_dict['game'].append(review.find('div', class_='product_title').find('h1').text)
        review_dict['name'].append(review.find('div', class_='name').find('a').text)
        review_dict['date'].append(review.find('div', class_='date').text)
        review_dict['rating'].append(review.find('div', class_='review_grade').find_all('div')[0].text)
        if review.find('span', class_='blurb blurb_expanded'):
            review_dict['review'].append(review.find('span', class_='blurb blurb_expanded').text)
        else:
            review_dict['review'].append(review.find('div', class_='review_body').find('span').text)

sword_reviews = pd.DataFrame(review_dict)
sword_reviews.to_csv(('user_review_{}.csv').format(today))

