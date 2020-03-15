# Script written by Jonathon Panzera Feb 20, 2020
# Parser tool designed for articles posted by the Infatuation Los Angeles

# Importing libraries
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

# Initializing URL and parser handle
my_url = 'https://www.theinfatuation.com/los-angeles/guides/restaurants-for-last-meal-in-la'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

# Initializing output file
filename = "results.json"
f = open(filename, "w")
f.write("{\n")

# Initializing container
container = page_soup.find('div', {'class': 'post__section post__section--guide-body'})
scriptContainer = page_soup.find('div',{'class':'post__sidebar sticky-sidebar'})
children = container.findChildren(["div","h2"] , recursive=False)

# Begin primary logic - iterating through each instance in the handle containing
# the restaurant reviews
for child in children:

    # Desist for intro paragraph
    if child['class'] == ['post__content__text-block']:
        continue

    # Extracting group headers where they exist
    if child['class'] == ['post__content__section-header']:
        f.write("\n\nGROUP SUBTITLE: " + child.span.text + "\n\n")
        continue
    
    # Extracting restaurant information
    nameChild = child.find('div',{'class':'spot-block__title-copy'})
    f.write("Name: " + nameChild.a.h3.text + "\n")

    placeURL = nameChild.a['href']
    f.write("Related Article: https://www.theinfatuation.com" + placeURL + "\n")

    # Needed if statements: not all restaurants have every property
    # we are seeking
    if child.find('div', {'class': 'overview-price-rating'}):
        costChild = child.find('div', {'class': 'overview-price-rating'})
        f.write("Cost Index: " + costChild['data-price'] + "\n")
    else:
        f.write("Cost Index: No Cost Listed\n")

    if child.find('span', {'class': 'overview-bold'}):
        contentChild = child.find('span', {'class': 'overview-bold'})
        f.write("Cuisine Type: " + contentChild.text + "\n")
        contentChild = contentChild.parent
        contentChild = contentChild.nextSibling
        contentChild = contentChild.nextSibling
        f.write("Neighborhood: " + contentChild.text + "\n")
    else:
        f.write("Cuisine Type: No Cuisine Type Listed\n")
        f.write("Neighborhood: No Neighborhood Listed\n")


    if child.find('img'):
        imgChild = child.find('img')
        imgURL = imgChild['data-src']
        f.write("Image URL: " + imgURL + "\n")
    else:
        f.write("Image URL: No Image Found\n")

    if child.find('div', {'class': 'rating'}):
        rateChild = child.find('div', {'class': 'rating'})
        f.write("Rating: " + rateChild['data-rating'] + rateChild.span.text + "\n")
    else:
        f.write("Rating: No Rating Listed\n")

    f.write("\n")


# Finished extracting data. Output stored in loose JSON format
# Closing file
f.write("}")
f.close()