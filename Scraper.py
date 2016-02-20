#imports
import requests
from bs4 import BeautifulSoup

#neatly package all the webscraping tools
class Scraper(object):

    def __init__(self):
        self.url_map = dict()

    #returns the url generated from searching keywords on clinicaltrials.gov
    def generateURL(self, keywords):
        url = "https://clinicaltrials.gov/ct2/results?term="
        for i in range(len(keywords)):
            if(i == 0):
                url += keywords[i]
            else:
                url = url + "+" + keywords[i]
        url += "&Search=Search"
        return url

    #returns a list of the titles in a top level keyword search
    #also maps in url_map the title to the corresponding url
    def searchAllStudies(self, keywords):
        url = self.generateURL(keywords)
        http = requests.get(url)
        soup = BeautifulSoup(http.content, "html.parser")
        titles = []
        for tag in soup.find_all("a"):
            line = str(tag)
            if(line.startswith("<a href")):
                index = line.find("Show study")
                if(index != -1):
                    start = line.find(":", index) + 2
                    end = line.find(">", start) - 1
                    url_start = line.find("href=") + 6
                    url_end = line.find("\"", url_start)
                    base = "https://clinicaltrials.gov"
                    new_url = base + line[url_start: url_end]
                    if(start != -1 and end != -1):
                        title = line[start: end]
                        titles.append(title)
                        #map titles to a url in object memory
                        self.url_map[title] = new_url
        return titles

keywords = ["cancer", "diabetes", "cholesterol"]
x = Scraper()
x.searchAllStudies(keywords)









