from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from IPython.display import HTML
import requests as r
import os
import time
from splinter import Browser
import re 


def init_browser():
    executable_path = {'executable_path': 'c:\\chromedrv\chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=False)
    #browser.visit('http://www.google.com')
    return Browser('chrome', **executable_path, headless=False)

#mars =  {}

def scrape_info():
    mars = {}
    news_title, news_p = mars_news()
    feature_image_url = mars_space_images()
    mars_facts_table = mars_facts()
    hemispheres_image_url = mars_hems()
    mars_weather = mars_weather1()

    mars = {
        "News_title" : news_title,
        "News_p" : news_p,
        "feature_image_url" : feature_image_url,
        "mars_facts_table" : mars_facts_table,
        "hemispheres_image_url" : hemispheres_image_url,
        "mars_weather": mars_weather

    }

    return mars

# ### Mars News
def mars_news():
    #mars =  {}
    browser = init_browser()

    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    results=browser.html
    soup_a=BeautifulSoup(results,'html.parser')
    news_title=soup_a.find('div',class_='content_title').get_text()
    news_p=soup_a.find('div',class_='article_teaser_body').get_text()
    #mars["news_title"] = news_title
    #mars["news_p"] = news_paragraph
   
    browser.quit()
    return news_title, news_p


#     # ### Mars Space Images
def mars_space_images():
    #mars =  {}
    browser = init_browser()

    mars_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_url)
    time.sleep(2)
    browser.find_by_id("full_image").click()
    time.sleep(2)
    browser.find_link_by_partial_text("more info").click()
    time.sleep(2)
    results=browser.html
    soup_a=BeautifulSoup(results,'html.parser')
    result= soup_a.find("figure",class_="lede")
    link= result.a.img["src"]
    feature_image_url = "https://www.jpl.nasa.gov" + link
    #mars["feature_image"] = feature_image_url

    browser.quit()
    return feature_image_url

    # ### Mars Weather
def mars_weather1():
    #mars =  {}
    mars_weather = ""
    browser = init_browser()

    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_twitter_url)
    time.sleep(5)
    browser.execute_script("window.scrollTo(0,-80000);")
    time.sleep(3)
    results=browser.html
    soup_a=BeautifulSoup(results,'html.parser')
    pattern = re.compile(r'InSight')
    mars_weather = soup_a.find('span',text=pattern)
    mars_weather=mars_weather.get_text()
    #mars["weather"] = mars_weather#.get_text()

    browser.quit()
    return mars_weather

    # ### Mars Facts
def mars_facts():
    #mars =  {}
    browser = init_browser()

    mars_fact_url = "https://space-facts.com/mars/"
    browser.visit(mars_fact_url)
    results=browser.html
    soup_a=BeautifulSoup(results,'html.parser')
    facts=pd.read_html(mars_fact_url)
    mars_facts = facts[0]
    mars_facts.columns = ["description","value"]
    mars_facts.set_index("description",inplace=True)
    mars_facts_table = mars_facts.to_html()
    mars_facts_table = mars_facts_table.replace('\n','')
    #mars["facts"] = mars_facts_table

    browser.quit()
    return mars_facts_table


    # ### Mars Hemispheres
def mars_hems():
    #mars =  {}
    browser = init_browser()

    mars_hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hem_url)
    hemispheres_image_url = []

    for i in range(4):
        hemispheres = {}
        browser.find_by_css("a.product-item h3")[i].click()
        results=browser.html
        soup=BeautifulSoup(results,'html.parser')
        title = soup.find("h2",class_="title").text
        url = soup.find("a",text = "Sample")["href"]
        hemispheres["title"] = title
        hemispheres["img_url"] = url
        hemispheres_image_url.append(hemispheres)
        browser.back()

    hemispheres_image_url
    #mars["hemispheres"] = hemispheres_image_url

    browser.quit()
    return hemispheres_image_url