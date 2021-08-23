import pandas as pd
from bs4 import BeautifulSoup
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
from splinter import Browser


def scrape():

    # Make Mongo Database
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    client.drop_database('mars_db')
    db = client.mars_db
    collection = db.articles

    # Connect to browser
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    mars = {}

    # NASA Mars News

    url = "https://mars.nasa.gov/news/"

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='content_title')
    title = results[1].a.text

    results = soup.find_all('div', class_= 'article_teaser_body')
    para = results[0].text

    mars['news_title'] = title
    mars['news_paragraph'] = para


    

    # JPL Mars Space Image

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = browser.find_by_tag('button')[1]
    results.click()
    img_results = soup.find_all('img')[1]['src']
    mars['featured_image_url'] = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + img_results

    
    # Mars Facts

    url = 'https://space-facts.com/mars/'

    table = pd.read_html(url)[0]
    table.columns=['Description', 'Mars']
    table.set_index('Description', inplace = True)
    mars_facts = table.to_html()
    mars['mars_facts'] = mars_facts

    
    # Mars Hemispheres


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_ = 'description')

    img_urls = []

    for name in results:
        dic_pic = {}
        temp = name.find('h3').text
        two_words = temp[:-9]
        dic_pic['title'] = two_words

        browser.click_link_by_partial_text(temp)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.find_all('img')[5]['src']
        base_url = 'https://astrogeology.usgs.gov'
        img_url = base_url + img
        dic_pic['img_urls'] = img_url
        img_urls.append(dic_pic)
        browser.back()
    
    
    mars['hemispheres'] = img_urls

    


    browser.quit()

    collection.insert_one(mars)

    return(mars)