

# Import Splinter and BeautifulSoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'

browser.visit(url)

# Optional delay for loading the page

browser.is_element_present_by_css('div.list_text', wait_time=1)


#set up the html parser

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')



slide_elem.find('div', class_='content_title')


# get_text pulls out the text (as opposed to the tags/elements)

news_title = slide_elem.find('div', class_='content_title').get_text()
news_title



#There are two methods used to find tags and attributes with BeautifulSoup:

# .find() is used when we want only the first class and attribute we've specified.
# .find_all() is used when we want to retrieve all of the tags and attributes.

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

news_p


# ### Featured Images
# 
# 



# Visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)


#we want it to click a button- find and click the full image button

full_image_elem = browser.find_by_tag('button')[1]

full_image_elem.click()



# Parse the resulting html (the full image page) with soup

html = browser.html

img_soup = soup(html, 'html.parser')



#build the relative image url (can't hard-code the url or it will give the same image every time)

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

#get('src') give the partial link to the image (Source)

img_url_rel



#add the base link so we can put them together to create a working link 

img_url = f'https://spaceimages-mars.com/{img_url_rel}'

img_url


#getting mars facts from another site, just scraping the entire html table from it using pandas


# read_html() finds all tables on the page, [0] returns the first table it finds 

df = pd.read_html('https://galaxyfacts-mars.com')[0]

df.columns = df.columns=['Description', 'Mars', 'Earth']

df.set_index('Description', inplace=True)

df


# convert the pandas df back to html with to_html()

df.to_html()


# end the browsing session

browser.quit()





