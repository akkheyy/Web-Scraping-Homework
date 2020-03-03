from bs4 import BeautifulSoup
from selenium import webdriver
from splinter import Browser
import urllib.parse
import pandas as pd
import pymongo
import requests
import os

def scrape():
    # mars_data = {}

    # Nasa Mars News
    news_url = "https://mars.nasa.gov/news/"
    text = requests.get(news_url).text
    news_file_name = "news-html-requests.txt"
    news_file = "news-selenium-.txt"


    driver = webdriver.Firefox()
    driver.implicitly_wait(40)
    driver.get(news_url)
    news_html = driver.page_source
    driver.close()


    news_soup = BeautifulSoup(news_html, "html.parser")

    news_article = news_soup.find("div", class_ = "list_text")
    news_title = news_article.find("div", class_ = "content_title").text
    news_p = news_article.find("div", class_ = "article_teaser_body").text

    # mars_data["news_title"] = news_title
    # mars_data["news_p"] = news_p

    # JPL Mars Space Images
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    image_text = requests.get(image_url).text
    image_soup = BeautifulSoup(image_text, "html.parser")


    image = image_soup.find("div", class_="carousel_container")
    for a in image.find_all("a", class_= "button fancybox"):
        featured_image_url = urllib.parse.urljoin("https://www.jpl.nasa.gov", a["data-fancybox-href"])

    # mars_data["featured_image_url"] = featured_image_url

    # Mars Weather
    weather_url = "https://twitter.com/marswxreport?lang=en"
    weather_file = "weather-html-requests.txt"
    weather_text = requests.get(weather_url).text
    weather_soup = BeautifulSoup(weather_text, "html.parser")


    weather = weather_soup.find("div", class_="js-tweet-text-container")


    mars_weather = weather.find("p", class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # mars_data["mars_weather"] = mars_weather

    # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    facts_text = requests.get(facts_url).text
    facts_soup = BeautifulSoup(facts_text, "html.parser")


    facts_table = facts_soup.find("table")
    table_rows = facts_table.find_all('tr')
    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)
    facts_df = pd.DataFrame(l)


    facts_html = facts_df.to_html()

    # mars_data["mars_table"] = facts_html

    # facts_table = soup.find_all("table")[0] 
    # facts_df = pd.read_html(str(table))

    # Mars Hemispheres
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver = webdriver.Firefox()
    driver.get(hemispheres_url)
    driver.implicitly_wait(15)
    hemispheres_html = driver.page_source
    driver.close()


    hemispheres_soup = BeautifulSoup(hemispheres_html, "html.parser")


    items = hemispheres_soup.find_all("div", class_= "item")

    hemisphere_image_urls = []

    for i in items: 
        title = i.find("h3").text
        partial_url = i.find("a", class_= "itemLink product-item")["href"]
        full_url = urllib.parse.urljoin("https://astrogeology.usgs.gov", partial_url)
        browser = Browser("firefox")
        browser.visit(full_url)
        partial_html = browser.html
        partial_soup = BeautifulSoup(partial_html, "html.parser")
        img_url = "https://astrogeology.usgs.gov" + partial_soup.find("img", class_= "wide-image")["src"]
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        browser.quit()
    
    # mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_tabe": facts_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    
    return mars_data
