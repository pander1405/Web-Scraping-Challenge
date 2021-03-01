# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

#import dependencies
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd
import requests


#initiate driver seperately
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)



def scrape_all():

    browser = init_browser()

    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    titles = soup.find_all('div', class_='content_title')
    texts = soup.find_all('div', class_='article_teaser_body')

    title_text = []
    text_only = []

    #keep only the text
    for x in titles:
        title_text.append(x.text.strip())
        
    for x in texts:
        text_only.append(x.text.strip())


    # JPL Mars Space Image

    #These lines of code are needed to navigate to the next page

    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    image_url_src = soup.find('img', class_='headerimage fade-in')['src']

    url_short = image_url.split('/')

    #rearrange and concatenate URL
    featured_image_url = url_short[0] + '//' + url_short[1] + url_short[2] + '/' + url_short[3] + '/' + image_url_src


    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    df = pd.read_html(facts_url)[0]
    mars_facts = df.to_html()


    # Mars Hemispheres
    pic_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(pic_url)
    hemi_url =[]

    links = browser.find_by_css('a.product-item h3')

    for i in range(len(links)):
        hemi = {}
        browser.find_by_css('a.product-item h3')[i].click()
        sample_image = browser.links.find_by_text('Sample').first
        hemi['img_url'] = sample_image['href']
        hemi['title'] = browser.find_by_css('h2.title').text
        
        hemi_url.append(hemi)
        
        browser.back()

    browser.quit()

    # Store data in one dictionary
    mars_data = {
        "news_title": title_text,
        "news_paragraph": text_only,
        "featured_image": featured_image_url,
        "mars_facts": mars_facts,
        "hemispheres": hemi_url
    }


    return mars_data