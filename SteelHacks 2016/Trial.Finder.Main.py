from tkinter import *
import Scraper
from ScrolledCanvas import *
from profpy import *

class searchRect(object):
    def __init__(self,data,canvas):
        self.moreButton = Button(data.root, bd = 5, font = "Helvetica 12",
               text = "More", command = lambda: indivSearch(data))
        self.faveButton = Button(data.root, bd = 5, font = "Helvetica 12",
               text = "Favorite", command = lambda: faveSearch(data))

def initBrowse(data,canvas):
    data.canvas = canvas
    data.favs = dict()
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
    data.searchRects = [searchRect(data,canvas),searchRect(data,canvas),
                        searchRect(data,canvas),searchRect(data,canvas),
                        searchRect(data,canvas)]
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
                             window = data.searchRects[(i-1)%5].moreButton)
        canvas.create_window(725,y + 75, anchor = NW, width = 100, height = 50,
                             window = data.searchRects[(i-1)%5].faveButton)

        (charLimit, spacing, endGap) = (41,32,37)
        y = createTitle(canvas, data.searchList[i][0], "Helvetica 18", charLimit, x, y, spacing, endGap)
        (charLimit, spacing, endGap) = (100,15,30)
        y = createTitle(canvas, data.searchList[i][1], "Helvetica 12", charLimit, x, y, spacing, endGap)
        (charLimit, spacing, endGap) = (90,15,55)
        y = createTitle(canvas, data.searchList[i][2], "Helvetica 8",  charLimit, x, y, spacing, endGap)
        
        y += 75

    canvas.create_window(x,y, anchor = NW, width = 100, height = 50, window = data.backButton)
    x += 100
    canvas.create_window(x,y, anchor = NW, width = 100, height = 50, window = data.nextButton)

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        data.canv.delete()
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    # create the root and the canvas
    root = Tk()
    frame = Frame(root)
    canv = ScrolledCanvas(root)
    data.canv = canv
    canv.pack()
    data.root = root
    canvas = canv.canvas
    init(data, canvas)
    data.speed = 5
    data.x = 0
    data.y = 500
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

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
        canvas.create_text(x,y,text = inputText, font = inputFont, anchor = NW, fill="white")
    else:
        textCopy = inputText
        while len(textCopy) > charLimit:
            i = findClosestSpace(textCopy,charLimit)
            canvas.create_text(x,y,text = textCopy[:i+1], font = inputFont, anchor = NW, fill="white")
            textCopy = textCopy[i+1:]
            y += spacing
        canvas.create_text(x,y,text = textCopy, font = inputFont, anchor = NW, fill="white")
    y += endGap
    return y

def findClosestSpace(text, charLimit):
    result = charLimit
    while text[result] != " ":
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

def faveSearch(data):
    clickedTitle = data.titles[data.currentRectNum + data.scrollStart]
    addFav(data.activeUser, data.scraper.url_map[clickedTitle], data)
    writeFile("favs.txt", stringProfiles(data.favs))


def displaySummary(data,summary):
    (charLimit, spacing, endGap) = (41,32,37)
    newWindow = Toplevel()
    newCanvas = Canvas(newWindow)
    (charLimit, spacing, endGap) = (41,32,37)
    x,y = 0,0
    y = createTitle(newCanvas, summary[0], "Helvetica 18", charLimit, x, y, spacing, endGap)
    (charLimit, spacing, endGap) = (100,15,30)
    y = createTitle(newCanvas, summary[1], "Helvetica 12", charLimit, x, y, spacing, endGap)
    y = createTitle(newCanvas, summary[2], "Helvetica 12", charLimit, x, y, spacing, endGap)
    (charLimit, spacing, endGap) = (105,15,55)
    y = createTitle(newCanvas, summary[3], "Helvetica 8",  charLimit, x, y, spacing, endGap)
    y = createTitle(newCanvas, summary[4], "Helvetica 8",  charLimit, x, y, spacing, endGap)
    y = createTitle(newCanvas, summary[5], "Helvetica 8",  charLimit, x, y, spacing, endGap)
    y += 50
    newCanvas.pack()
    newWindow.mainloop()
