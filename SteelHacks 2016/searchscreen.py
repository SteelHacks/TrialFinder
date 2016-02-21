from tkinter import *
import Scraper

def initBrowse(data,canvas):
    data.canvas = canvas

    data.searchInput = ""
    data.searchBarClicked = False
    data.searchBarWidth = 400
    data.searchBarHeight = 50
    data.searchBarLeft = 150
    data.searchBarTop = 50
    data.searchEntry = Entry(data.root, bd = 10)

    data.searchButtonWidth = 100
    data.searchButtonHeight = 41
    data.searchButtonLeft = 600
    data.searchButtonTop = 50
    data.searchButtonClicked = False
    data.searchButton2 = Button(data.root, bd = 5, font = "Helvetica 12", 
                   text = "Search", command = lambda: makeSearch(data))
    data.searchTerms = []
    data.searchList = {1:None, 2:None, 3:None, 4:None, 5:None}

    data.scraper = Scraper.Scraper()
    data.showResults = False
    data.titles = None

    data.scrollStart = 0
    data.scrollEnd = 5

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
        (charLimit, spacing, endGap) = (41,32,37)
        y = createTitle(canvas, data.searchList[i][0], "Helvetica 18", charLimit, x, y, spacing, endGap)
        (charLimit, spacing, endGap) = (100,15,30)
        y = createTitle(canvas, data.searchList[i][1], "Helvetica 12", charLimit, x, y, spacing, endGap)
        (charLimit, spacing, endGap) = (105,15,55)
        y = createTitle(canvas, data.searchList[i][2], "Helvetica 8",  charLimit, x, y, spacing, endGap)
        y += 50

def makeSearch(data):
    data.searchInput = data.searchEntry.get()
    keywords = data.searchInput.split(" ")
    data.titles = data.scraper.searchAllStudies(keywords)
    updateSearchList(data)

def updateSearchList(data):
    for i in range(data.scrollStart, data.scrollEnd):
        data.searchList[i] = data.scraper.getPreview(data.titles[i]).split("\n")

def createTitle(canvas, inputText, inputFont, charLimit, x, y, spacing, endGap):
    if len(inputText) < charLimit:
        canvas.create_text(x,y,text = inputText, font = inputFont, anchor = NW,fill="white")
    else:
        textCopy = inputText
        while len(textCopy) > charLimit:
            i = findClosestSpace(textCopy,charLimit)
            canvas.create_text(x,y,text = textCopy[:i+1], font = inputFont, anchor = NW,fill="white")
            textCopy = textCopy[i+1:]
            y += spacing
        canvas.create_text(x,y,text = textCopy, font = inputFont, anchor = NW,fill="white")
    y += endGap
    return y

def findClosestSpace(text, charLimit):
    result = charLimit
    while text[result] != " ":
        result -= 1
    return result