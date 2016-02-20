import requests
from bs4 import BeautifulSoup

r = requests.get("https://clinicaltrials.gov/ct2/results?term=heart+attack&Search=Search")

#r.content contains all the html code

soup = BeautifulSoup(r.content, "html.parser") # clean up the html code

# this prints out an easier to read version of the html stuff
#print(soup.prettify())

# this find all links starting with a, puts in list
#soup.find_all("a")

articles = list()
for link in soup.find_all("a"):
    a = ""
    if(str(link)[68:78] == "Show study"):
        print(str(link)[92:str(link)[95:].index("\"")+95])
        print()
        # print(str(link)[92:str(link)[95:].index("\"")])
    # print("")
    # print(link.get("href"))
    # for char in link.get("href"):
    #     if char 
    # print(link)
