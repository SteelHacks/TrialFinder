#imports
import requests
from bs4 import BeautifulSoup

#neatly package all the webscraping tools
class Scraper(object):

    def __init__(self):
        self.url_map = dict()

    #function takes html markup language and removes the <> tags from the text
    @staticmethod
    def removeMarkup(line):
        removing = False
        result = ""
        start = 0
        end = 0
        length = len(line)
        for i in range(length):
            if(removing == False and line[i] != "<" and i != length - 1):
                end += 1
            elif(removing == False and line[i] == "<"):
                removing = True
                result += line[start : end]
            elif(removing == True and line[i] == ">"):
                removing = False
                start = i + 1
                end = i + 1
            else:
                if(i == length - 1):
                    result += line[start:]
        return result

    #ensures all values in a string are printable ascii characters
    @staticmethod
    def isASCII(string):
        for char in string:
            if(ord(char) > 127):
                return False
        return True

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

    #takes the title or link arguments passed into get_____ functions
    #returns the URL that can be used in that function
    #raises exception if url cannot be extracted from title or link
    def processURL(self, title, link):
        if(link == None and title == None):
            raise Exception("Must pass a title or a link")
        elif(link == None and title != None): 
            url = self.url_map[title]
        else: 
            url = link
        http = requests.get(url)
        soup = BeautifulSoup(http.content, "html.parser")
        return soup

    #returns a list of the titles in a top level keyword search
    #also maps in url_map the title to the corresponding url
    def searchAllStudies(self, keywords, url_mapping = True):
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

    #for ease of implementation these functions can work
    #whether given a title it's seen before or a url to parse
    def getPurpose(self, title = None, link = None):
        soup = self.processURL(title, link)
        html = str(soup).splitlines()
        start_index = html.index("<!-- purpose_section -->")
        next_section = "<!-- condition, intervention, phase summary table -->"
        end_index = html.index(next_section)
        result = ""
        for i in range(start_index, end_index):
            line = self.removeMarkup(html[i])
            if(self.isASCII(line)):
                result += line + "\n"
        return result.strip()
    
    #returns (start, end) of study / (None, None) if no date found        
    def getTimeFrame(self, title = None, link = None):
        soup = self.processURL(title, link)
        html = str(soup).splitlines()
        start = self.getStart(soup, html)
        end = self.getEnd(soup, html)
        return (start, end)

    def getStart(self, soup, html):
        length = len(html)
        start_index = None
        for i in range(length):
            if(html[i].find("Start Date") != -1):
                start_index = i + 1
        if(start_index == None): return None
        return self.removeMarkup(html[start_index]).strip()

    def getEnd(self, soup, html):
        length = len(html)
        end_index = None
        for i in range(length):
            if(html[i].find("Completion Date") != -1):
                end_index = i + 1
        if(end_index == None): return None
        result = self.removeMarkup(html[end_index])
        date = (result.split(" "))
        if(len(date) > 2):
            result = date[0] + " " + date[1]
        return result.strip()

    def getCriteria(self, title = None, link = None):
        soup = self.processURL(title, link)
        html = str(soup).splitlines()
        start_index = html.index("<!-- eligibility_section -->")
        next_section = "<!-- location_section -->"
        end_index = html.index(next_section)
        result = ""
        start = False
        for i in range(start_index, end_index):
            line = self.removeMarkup(html[i])
            if(start == False and line.find("Inclusion") != -1):
                start = True
            elif(line.find("Exclusion") != -1): 
                break
            if(self.isASCII(line) and start == True):
                result += line + "\n"
        return result.strip()

keywords = ["trisomy", "21"]
x = Scraper()
titles = x.searchAllStudies(keywords)
i = 5
#title
print(titles[i], end = "\n\n")
#URL
print(x.url_map[titles[i]], end = "\n\n")
#START AND END DATE
print(x.getTimeFrame(title = titles[i]), end = "\n\n")
#PURPOSE
print(x.getPurpose(titles[i]), end = "\n\n")
#INCLUSION CRITERIA
print(x.getCriteria(titles[i]), end = "\n\n")
