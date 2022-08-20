

# Import Splinter, BeautifulSoup, Pandas, Datetime

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():

    executable_path = {'executable_path': ChromeDriverManager().install()}

    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(browser),
        "hemispheres": mars_hemi_images(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data

    browser.quit()

    return data

# Create Function

def mars_news(browser):

    # Visit the mars nasa news site

    url = 'https://redplanetscience.com'

    browser.visit(url)

    # Optional delay for loading the page

    browser.is_element_present_by_css('div.list_text', wait_time=1)


    #set up the html parser

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:

        slide_elem = news_soup.select_one('div.list_text')

        # get_text pulls out the text (as opposed to the tags/elements)

        news_title = slide_elem.find('div', class_='content_title').get_text()
        

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:

        return None, None

    return news_title, news_p


# ### Featured Images
# 
# 

# Visit URL

def featured_image(browser):

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


    #we want it to click a button- find and click the full image button

    full_image_elem = browser.find_by_tag('button')[1]

    full_image_elem.click()


    # Parse the resulting html (the full image page) with soup

    html = browser.html

    img_soup = soup(html, 'html.parser')


    #build the relative image url (can't hard-code the url or it will give the same image every time)

    try:

        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    #get('src') give the partial link to the image (Source)

    except AttributeError:

        return None

    #add the base link so we can put them together to create a working link 

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'


    return img_url


#getting mars facts from another site, just scraping the entire html table from it using pandas


# read_html() finds all tables on the page, [0] returns the first table it finds 

def mars_facts(browser):

    try:

        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    
    except BaseException:
    
        return None

    df.columns = df.columns=['Description', 'Mars', 'Earth']

    df.set_index('Description', inplace=True)


    # convert the pandas df back to html with to_html()

    return df.to_html(classes="table table-striped")

def mars_hemi_images(browser):

    url = 'https://marshemispheres.com/'

    browser.visit(url)

    try:
        links = browser.find_by_css('a.product-item img')

    except AttributeError: 

        return None
    
    hemisphere_image_urls = []

    for i in range(len(links)):
        #create the enpty dict entry
        hemisphere = {}
        #find image and click[
        browser.find_by_css('a.product-item img')[i].click()
        #from next page, click the full sample
        hemi_sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['image_url'] = hemi_sample_elem['href']
        #get title
        hemisphere['title'] = browser.find_by_css('h2.title').text
        #add dict to list
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    print(hemisphere_image_urls)
    return hemisphere_image_urls

#engage flask

if __name__ == "__main__":

    # If running as script, print scraped data

    print(scrape_all())







