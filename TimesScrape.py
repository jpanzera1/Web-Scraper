# Script written by Jonathon Panzera Feb 20, 2020
# Parser tool designed for articles posted by the New York Times

# Importing libraries
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

# Initializing URL and parser handle
my_url = 'https://www.nytimes.com/2019/10/31/travel/what-to-do-36-Hours-in-Berlin.html'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

# Initializing output file handle
filename = "results.json"
f = open(filename, "w")
f.write("{\n")

# Initializing container handle array
containers = page_soup.findAll("div",{"class":"css-53u6y8"})

# Primary logic begins
# Iterating through each container holding 1-2 locations reviewed
for container in containers:

    # Set to skip intro paragraph
    if not container.h3:
        continue

    headerList = container.findAll("h3")
    bodyList = container.findAll("p")
    itemCount = len(headerList)

    # Parsing headers and corresponding body data
    for i in range (0,len(headerList)):
        header = headerList[i].text
        headerStrings = header.split(". ")
        name = headerStrings[1]
        name = re.sub('[^A-Za-z0-9 ,]+', '', name)
        f.write("Entry Name is: " + name + "\n")

        headerStrings = headerStrings[0].split(") ")
        time = headerStrings[1] + "."
        f.write("Relevant Time is: " + time + "\n")

        body = bodyList[i].text
        body = re.sub('[^A-Za-z0-9 ,.?!€-]+', '', body)
        bodyStrings = body.split(". ")

        linkList = bodyList[i].findAll("a")
        placeCostFound = False

        # Parsing available places attached to links inserted by the author
        # Cannot detect places if they are not associated with a link
        k = 0
        for j in range (0,len(linkList)):
            placeURL = linkList[j]["href"]
            place = linkList[j].text
            f.write("Relevant Place is: " + place + "\n")
            f.write("Place URL is: " + placeURL + "\n")

            # Parsing costs of each location
            # Took surrounding sentence of an amount for context,
            # as the amounts are not comparable
            for k in range (k,len(bodyStrings)):
                if (bodyStrings[k].find("$") != -1):
                    f.write("Place cost is: " + bodyStrings[k] + "\n")
                    placeCostFound = True
                    break
                if (bodyStrings[k].find("free") != -1):
                    f.write("Place cost is: " + bodyStrings[k] + "\n")
                    placeCostFound = True
                    break
                if (bodyStrings[k].find("euro") != -1):
                    f.write("Place cost is: " + bodyStrings[k] + "\n")
                    placeCostFound = True
                    break
                if (bodyStrings[k].find("€") != -1):
                    f.write("Place cost is: " + bodyStrings[k] + "\n")
                    placeCostFound = True
                    break
            if placeCostFound == False:
                f.write("Place cost: not found\n")
            k += k
        f.write("\n")

# Parsing complete; output to a loose JSON format
# Closing file
f.write("}")
f.close()