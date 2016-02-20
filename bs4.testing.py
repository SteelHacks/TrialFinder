import requests
from bs4 import BeautifulSoup

r = requests.get("https://clinicaltrials.gov/ct2/results?term=&Search=Search")

#r.content contains all the html code

soup = BeautifulSoup(r.content) # clean up the html code

# this prints out an easier to read version of the html stuff
#print(soup.prettify())

# this find all links starting with a, puts in list
#soup.find_all("a")

for link in soup.find_all("a"):
    print(link.get("href"), end = "")
    print(link)