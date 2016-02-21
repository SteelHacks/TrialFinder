from tkinter import *
import Scraper
from ScrolledCanvas import *
from profpy import *

class searchRect(object):
    def __init__(self,data,canvas, index):
        self.index = index
        self.moreButton = Button(data.root, bd = 5, font = "Helvetica 12",
               text = "More", command = lambda: indivSearch(data))
        self.faveButton = Button(data.root, bd = 5, font = "Helvetica 12",
               text = "Favorite", command = lambda: faveSearch(data, self.index))


def initBrowse(data,canvas):
    data.canvas = canvas
    data.favs = interperateProfiles("favs.txt")
    print(data.favs, "THESE ARE DA FAVZZZZ")
    data.searchInput = ""
    data.searchBarClicked = False
    data.searchBarWidth = 400
    data.searchBarHeight = 50
    data.searchBarLeft = 150
    data.searchBarTop = 50
    data.searchEntry = Entry(data.root, bd = 10)
    # data.activeUser=

    data.searchButtonWidth = 100
    data.searchButtonHeight = 41
    data.searchButtonLeft = 600
    data.searchButtonTop = 50
    data.searchButtonClicked = False
    data.searchButton2 = Button(data.root, bd = 5, font = "Helvetica 12", 
                   text = "Search", command = lambda: makeSearch(data))
    data.searchTerms = []
    data.searchList = {1:None, 2:None, 3:None, 4:None, 5:None}
    data.searchRects = [searchRect(data,canvas,0),searchRect(data,canvas,1),
                        searchRect(data,canvas,2),searchRect(data,canvas,3),
                        searchRect(data,canvas,4)]
    data.currentRectNum = None

    data.scraper = Scraper.Scraper()
    data.showResults = False
    data.titles = None

    data.scrollStart = 0
    data.scrollEnd = 5

    data.backButton = Button(data.root, bd = 5, font = "Helvetica 12",
                      text = "Back", command = lambda: searchBack(data))
    data.nextButton = Button(data.root, bd = 5, font = "Helvetica 12", 
                      text = "Next", command = lambda: searchNext(data))

def browseMousePressed(event, data):
    pass

def browseKeyPressed(event, data):
    pass

def browseTimerFired(data):
    pass

def browseRedrawAll(canvas, data):
    x,y = data.searchBarLeft, data.searchBarTop
    canvas.create_window(x,y, anchor = NW, width = data.searchBarWidth, window = data.searchEntry)

    w,x = data.searchButtonLeft, data.searchButtonTop
    y,z = data.searchButtonWidth, data.searchButtonHeight
    canvas.create_window(w,x, anchor = NW, width = y, height = z, window = data.searchButton2)
    if data.titles != None: 
        drawSearchPreviews(canvas,data)

def drawSearchPreviews(canvas,data):
    x,y = data.searchBarLeft, data.searchBarTop + data.searchBarHeight + 100
    for i in range(data.scrollStart, data.scrollEnd):
        data.currentRectNum = i
        canvas.create_window(725,y,anchor = NW, width = 100, height = 50, 
                             window = data.searchRects[i%5].moreButton)
        canvas.create_window(725,y + 75, anchor = NW, width = 100, height = 50,
                             window = data.searchRects[i%5].faveButton)

        (charLimit, spacing, endGap) = (41,32,37)
        print(data.searchList[(i%5)+1])
        y = createTitle(canvas, data.searchList[(i%5)+1][0], "Helvetica 18", charLimit, x, y, spacing, endGap)
        (charLimit, spacing, endGap) = (100,15,30)
        y = createTitle(canvas, data.searchList[(i%5)+1][1], "Helvetica 12", charLimit, x, y, spacing, endGap)
        (charLimit, spacing, endGap) = (90,15,55)
        y = createTitle(canvas, data.searchList[(i%5)+1][2], "Helvetica 8",  charLimit, x, y, spacing, endGap)
        
        y += 75

    canvas.create_window(x,y, anchor = NW, width = 100, height = 50, window = data.backButton)
    x += 100
    canvas.create_window(x,y, anchor = NW, width = 100, height = 50, window = data.nextButton)

def makeSearch(data):
    data.searchInput = data.searchEntry.get()
    keywords = data.searchInput.split(" ")
    data.titles = data.scraper.searchAllStudies(keywords)
    updateSearchList(data)

def updateSearchList(data):
    for i in range(data.scrollStart, data.scrollEnd):
        data.searchList[(i%5)+1] = data.scraper.getPreview(data.titles[i]).split("\n")

def createTitle(canvas, inputText, inputFont, charLimit, x, y, spacing, endGap, filler = "white"):
    if len(inputText) < charLimit:
        canvas.create_text(x,y,text = inputText, font = inputFont, anchor = NW, fill=filler)
    else:
        textCopy = inputText
        while len(textCopy) > charLimit:
            i = findClosestSpace(textCopy,charLimit)
            canvas.create_text(x,y,text = textCopy[:i+1], font = inputFont, anchor = NW, fill=filler)
            textCopy = textCopy[i+1:]
            y += spacing
        canvas.create_text(x,y,text = textCopy, font = inputFont, anchor = NW, fill=filler)
    y += endGap
    return y

def findClosestSpace(text, charLimit):
    result = charLimit
    while text[result] != " " and text[result] != "\n":
        result -= 1
    return result

def searchBack(data):
    if data.scrollStart < 5:
        pass
    else:
        data.scrollStart -= 5
        data.scrollEnd -= 5
        updateSearchList(data)

def searchNext(data):
    if len(data.titles) > data.scrollEnd + 5:
        data.scrollEnd += 5
        data.scrollStart += 5
        updateSearchList(data)
    else:
        pass

def indivSearch(data):
    clickedTitle = data.titles[data.currentRectNum + data.scrollStart]
    summary = data.scraper.getSummary(clickedTitle)
    displaySummary(data,summary)

def faveSearch(data, index):
    clickedTitle = data.titles[index+ data.scrollStart]
    print(clickedTitle)
    print(data.favs, "befORE")
    addFav(data.activeUser, data.scraper.url_map[clickedTitle], data)
    print(data.favs, "AFTER")
    #print(data.favs)
    writeFile("favs.txt", stringProfiles(data.favs))


def displaySummary(data,summary):
    newWindow = Toplevel()
    newCanvas = Canvas(newWindow,height = 700, width = 1000)
    (charLimit, spacing, endGap) = (50,40,45)
    x,y = 50,25
    y = createTitle(newCanvas, summary[0], "Helvetica 18", charLimit, x, y, spacing, endGap, "black")
    (charLimit, spacing, endGap) = (100,20,60)
    # summary[1] is URL
    y = createTitle(newCanvas, summary[1], "Helvetica 12 bold underline", charLimit, x, y, spacing, endGap, "blue")
    # summary[2] is dates
    y = createTitle(newCanvas, summary[2], "Helvetica 12 bold", charLimit, x, y, spacing, endGap, "black")
    (charLimit, spacing, endGap) = (150,20,60)
    y = createTitle(newCanvas, summary[3], "Helvetica 9",  charLimit, x, y, spacing, endGap, "black")
    inclusion = removeNewLines(summary[4].split("\n"))
    endGap = 15
    for line in inclusion:
        y = createTitle(newCanvas, line, "Helvetica 9", charLimit, x, y, spacing, endGap, "black")
    # exclusion = removeNewLines(summary[5].split("\n"))
    # y += 10
    # for line in exclusion:
    #    y = createTitle(newCanvas, line, "Helvetica 8", charLimit, x, y, spacing, endGap, "black")
    
    newCanvas.pack()
    newWindow.mainloop()

def removeNewLines(lineList):
    result = []
    for line in lineList:
        if line != "":
            result.append(line)
    return result
