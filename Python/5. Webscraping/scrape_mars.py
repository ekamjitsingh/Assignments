# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

def scrape():
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"

    #splinter initialization
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #splinter visiting
    browser.visit(url)
    sleep(2)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # scraping NASA news website
    results=soup.find_all('div', class_="content_title")
    news_title=results[0].find('a').text
    news_paragraph=soup.find_all('div', class_="article_teaser_body")[0].text
    
    # visiting NASA Mars space images
    url2='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    sleep(2)
    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(4)
    html2=browser.html
    
    #Scraping featured image from NASA Mars space images website
    soup2 = BeautifulSoup(html2, 'html.parser')
    main_image=soup2.find('img', class_='fancybox-image')['src']
    featured_image_url= 'https://www.jpl.nasa.gov'+main_image
    
    # Visiting Mars weather twitter
    url3='https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    sleep(2)
    html3=browser.html
    
    #Scraping latest tweet
    soup3 = BeautifulSoup(html3, 'html.parser')
    first_tweet=soup3.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
    #Visiting Mars Space-Facts website
    url4= 'https://space-facts.com/mars/'
    
    #Scraping page using Pandas
    tabledf=pd.read_html(url4)[0]
    tabledf.columns = ['title', 'value']
    table_html=tabledf.to_html(index=False)
    mars_facts_table=table_html
    
    #Visiting Mars hemisphere gallery
    url5="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    sleep(2)
    
    #Scraping titles of Mars Hemisphere
    html4= browser.html
    soup4 = BeautifulSoup(html4, 'html.parser')
    hemisphere_titles=[]
    for q in soup4.find_all('a', class_='itemLink product-item'):
        if q.text !='':
            hemisphere_titles.append(q.text)
    
    #Scraping urls of Mars Hemisphere images
    hemisphere_urls=[]
    for hemisphere_title in hemisphere_titles:
        browser.click_link_by_partial_text(hemisphere_title)
        sleep(2)
        html5 = browser.html
        soup5 = BeautifulSoup(html5, 'html.parser')
        hemisphere_urls.append(soup5.find_all('div', class_='downloads')[0].find('li').a['href'])
        browser.back()
        sleep(2)
    
    #Creating dictionary of Mars Hemisphere titles and hemisphere images url
    hemisphere_image_urls=[]
    for i in range(len(hemisphere_titles)):
        dict={'title':hemisphere_titles[i], 'img_url':hemisphere_urls[i]}
        hemisphere_image_urls.append(dict)
        
    #Closing Splinter browser
    browser.quit()
    
    #Storing all scraped data in a dictionary
    scraped_dict={"title":news_title, 
                "paragraph":news_paragraph, 
                "featured_img_url":featured_image_url, 
                "tweet":first_tweet,
                "mars_table":mars_facts_table,
                "hemispheres":hemisphere_image_urls
                }
    print(scraped_dict)
    return scraped_dict
