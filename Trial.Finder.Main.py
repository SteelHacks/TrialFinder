from tkinter import *

# import all necessary files
import Scraper
import homepage

class Struct(object): pass
data = Struct()

def initAll(data,canvas):
    data.mode = "homepage"
    homepage.initHomepage(data,canvas)

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "welcomeScreen"): welcomeScreenMousePressed(event, data)
    if (data.mode == "homepage"): homepage.homepageMousePressed(event,data)
    if (data.mode == "myProfile"): myProfileMousePressed(event,data)
    if (data.mode == "browse"): browseMousePressed(event,data)

def keyPressed(event, data):
    if (data.mode == "welcomeScreen"): welcomeScreenKeyPressed(event, data)
    if (data.mode == "homepage"):homepage.homepageKeyPressed(event,data)
    if (data.mode == "myProfile"):myProfileKeyPressed(event,data)
    if (data.mode == "browse"): browseKeyPressed(event,data)

def timerFired(data):
    if (data.mode == "welcomeScreen"): welcomeScreenTimerFired(data)
    if (data.mode == "homepage"): homepage.homepageTimerFired(data)
    if (data.mode == "myProfile"): myProfileTimerFired(data)
    if (data.mode == "browse"): browseTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "welcomeScreen"): welcomeScreenRedrawAll(canvas, data)
    if (data.mode == "homepage"): homepage.homepageRedrawAll(canvas,data)
    if (data.mode == "myProfile"): myProfileRedrawAll(canvas,data)
    if (data.mode == "browse"): browseRedrawAll(canvas,data)

def detectHover(event,canvas,data):
    # if menu is already there, then show it until the mouse is off the menu
    if(data.displayMenu and
       canvas.winfo_pointerx()-canvas.winfo_rootx() < data.menuSize[0]):
        return
    # menu appears when user hovers in top left corner of window
    # top left 50 x 50 pixel square
    elif(canvas.winfo_pointerx()-canvas.winfo_rootx() > 50 or 
       canvas.winfo_pointery()-canvas.winfo_rooty() > 50):
        data.displayMenu = False
    else: data.displayMenu = True

def run(width=850, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event,data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event,data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    data.root = root
    initAll(data,canvas)
    canvas.pack()
    # set up events
    data.root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    data.root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event: detectHover(event,canvas,data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

run()