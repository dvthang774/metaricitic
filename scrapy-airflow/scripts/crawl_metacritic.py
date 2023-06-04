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

data_dict = {'name':[], 'platform':[], 'release_date':[], 'metascore':[], 'user_score':[]}

def webpage(pageNum):
    url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?sort=desc&view=detailed&page=' + str(pageNum)
    userAgent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=userAgent)
    return response

def numberPages(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = soup.find_all('li', {"class":"active_page"})
    pagesCleaned = pages[0].find('span', {"class":"page_num"})
    return (pagesCleaned.text)
    
def scraper(num_loops, content):
    tblnum = 0
    while tblnum < num_loops:
        #get game name
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            if len(tr)<1:
                continue
            td = tr.find_all('td')
            a = td[1].find('a', {"class":"title"})
            data_dict['name'].append(a.find('h3').text)
            #print(a.find('h3').text)

        #get game release date
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            if len(tr)<1:
                continue
            td = tr.find_all('td')
            date = td[1].find('span',{"class":""})
            data_dict['release_date'].append(date.text)
            #print(date.text)

        #get artist
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            if len(tr)<1:
                continue
            td = tr.find_all('td')
            p1 = td[1].find('div',{"class":"platform"})
            platform = p1.find('span', {"class":"data"})
            data_dict['platform'].append(platform.text.strip())
            #print(platform.text.strip())
            
        #get userscore
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            if len(tr)<1:
                continue
            td = tr.find_all('td')
            div_score = td[1].find('div', {"class":"clamp-userscore"})
            user = div_score.find('div',{"class":"metascore_w"})
            data_dict['user_score'].append(user.text.strip())
            #print(user.text.strip())
            
        #get metascore
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            if len(tr)<1:
                continue
            td = tr.find_all('td')
            score = td[1].find('div', {"class":"metascore_w"})
            data_dict['metascore'].append(score.text)
            #print(score.text)
        tblnum += 1
        
def pages(lastPageNum): 
    currentPage = lastPageNum
    url = url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=' + str(currentPage)
    userAgent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=userAgent)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find_all('table')
    
    num_loops = len(content)
    #print(num_loops)
    scraper(num_loops,content)
    #print(data_dict)
    #time.sleep(6)        

def main():
    
    pgs = list(range(0,399))
    for pg in pgs:
        numPage = (numberPages(webpage(pg)))
        pages(int(pg))
        time.sleep(5)
        print("Page " + str(pg+1) + " completed")
    xData = (pd.DataFrame.from_dict(data_dict))
    xData.to_csv(('{}.csv').format(today))
    
main()
