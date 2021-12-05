# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Visit the NASA Mars News Site
# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

# ### JPL Space Images Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

df = pd.read_html('https://galaxyfacts-mars.com')[0]

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)

df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
# url = 'https://astrogeology.usgs.gov' 
browser.visit(url)

# HTML Object
html_hemi = browser.html

# Parse HTML with Beautiful Soup
hemi_soup = soup(html_hemi, 'html.parser')

# Retreive all items that contain mars hemispheres information
items = hemi_soup.find_all('div', class_='item')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in items:
   # Store title
   title = i.find('h3').text
  
   # Store link that leads to full image website
   partial_img_url = i.find('a', class_='itemLink product-item')['href']
   
   # Visit the link that contains the full image website 
   browser.visit(url + partial_img_url)

   # HTML Object of each hemisphere website 
   partial_img_html = browser.html

   # Parse HTML with Beautiful Soup for every each hemisphere website 
   hemi_soup = soup( partial_img_html, 'html.parser')

   # Retrieve full image source 
   img_url = url + hemi_soup.find('img', class_='wide-image')['src']

   # Append the retreived information into a list of dictionaries 
   hemisphere_image_urls.append({ "img_url" : img_url, "title" : title,})

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()