from tkinter import *
from webscraper import Scraper
from ScrolledCanvas import *

def init(data):
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
    data.searchButton = Button(data.root, bd = 5, font = "Times 12", 
                   text = "Search", command = lambda: makeSearch(data))
    data.searchTerms = []

    data.scraper = Scraper()
    data.showResults = False
    data.titles = None

    data.scrollStart = 0
    data.scrollEnd = 3

def mousePressed(event, data):
    pass
    # if (data.searchBarLeft <= event.x <= data.searchBarLeft + data.searchBarWidth) and\
    #    (data.searchBarTop <= event.y <= data.searchBarTop + data.searchBarHeight):
    #         data.searchBarClicked = True
    # else: data.searchBarClicked = False
    # if data.searchButtonLeft <= event.x <= data.searchButtonLeft + data.searchButtonWidth and\
    #    data.searchButtonTop <= event.y <= data.searchButtonTop + data.searchButtonHeight:
    #         data.searchButtonClicked = True

def keyPressed(event, data):
    pass
    # if data.searchBarClicked:
    #     if event.keysym != "BackSpace":
    #         data.searchInput += event.keysym
    #     elif len(data.searchInput) > 0:
    #         data.searchInput = data.searchInput[:len(data.searchInput)]

def timerFired(data):
    pass

def redrawAll(canvas, data):
    x,y = data.searchBarLeft, data.searchBarTop
    canvas.create_window(x,y, anchor = NW, width = data.searchBarWidth, window = data.searchEntry)

    w,x = data.searchButtonLeft, data.searchButtonTop
    y,z = data.searchButtonWidth, data.searchButtonHeight
    canvas.create_window(w,x, anchor = NW, width = y, height = z, window = data.searchButton)
    if data.titles != None: 
        drawSearchPreviews(canvas,data)

def drawSearchPreviews(canvas,data):
    x,y = 0,0
    for i in range(data.scrollStart, data.scrollEnd):
        canvas.create_text(x,y,text = data.scraper.getPreview(data.titles[i]), anchor = NW)
        y += 200

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
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    frame = Frame(root)
    canv = ScrolledCanvas(root)
    data.canv = canv
    canv.pack()
    data.root = root
    canvas = canv.canvas
    init(data)
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

run(850, 650)