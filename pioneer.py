from newspaper import Article
import feedparser as fp
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import time
import datetime
import numpy as np

#def image_download(url,filename):
  #  r = requests.get(url)
 #   with open(filename, 'wb') as outfile:
#        outfile.write(r.content)

def get_links(table):
    temp = []
    for i in table[0].findAll('h2'):
        temp.append(i.a['href'])
        
    for i in table[0].findAll('h3'):
        temp.append(i.a['href'])    
    return temp




links = []


#r = requests.get(url, headers=headers, proxies=proxyDict)

p = 1
while 1: 
    r = requests.get('https://www.dailypioneer.com/searchlist.php?yr=2020&mn=4&page='+ str(p))
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.findAll('div', attrs = {'class':'col-12 col-sm'})
    
    link = get_links(table)
    if len(link) == 0:
        break
    links.extend(link)
    p= p + 1
    time.sleep(1.1)


t = 'https://www.dailypioneer.com'
for i in range(len(links)):
    links[i] = t+links[i]
        

import csv
with open("links_FEB.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(links)
    
    


#cols = ['Date','Title','Article','Summary','Category','Image_link','Article_link']

d=[]
category = []
titles = []
content = []
img = []
link= []
br = 0

data  = {}
for i in range(1,31):
    data[i] = pd.DataFrame(columns = ['Date','Title','Article','Category','Image_link','Article_link'])
#for rss_link in get_links:
    
    
for j in range(5260,len(links)):
    print(j)
    print(br)
    r1 = requests.get(links[j])
    soup1 = BeautifulSoup(r1.content, 'html5lib') 
    date = soup1.findAll('span', attrs = {'itemprop':'dateModified'})
   
    da = date[0]['content']
    da= da.split(' ')[1] 
    dat= da + '-4-20'
    
    
    if br == 0:
        br = int(da)
   
    if (br != int(da) and br!=0) or j == len(links)-1:
        temp = pd.DataFrame(columns = ['Date','Title','Article','Category','Image_link','Article_link'])
        temp['Date'] = d
        temp['Title'] = titles
        temp['Article'] = content
        temp['Category'] = category
        temp['Image_link'] = img
        temp['Article_link'] = link
        data[br] = data[br].append(temp,ignore_index = True)
        
        link= []
        d=[]
        category = []
        titles = []
        content = []
        img = []
        br = 0
    time.sleep(0.8)
    article = Article(links[j], language="en")
    article.download()
    article.parse()
    content.append(article.text)
    img.append(article.top_image) 
    titles.append(article.title)
    category.append(links[j].split('/')[-2])
    link.append(links[j])
    d.append(dat)
    time.sleep(0.7)
    

for i in range(1,8):
    directory = r'C:\Users\ajain\Desktop\News\\' + str(i) +'-4-20' +'\Pioneer\\'
    os.makedirs(directory,exist_ok = True) 
    data[i].to_csv(directory+str(i)+'.csv')
    
    
    
    
    
    
    