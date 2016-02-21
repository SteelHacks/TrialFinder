
from tkinter import *
from profpy import *

# import all necessary files
import Scraper
import welcome
import searchscreen
import homepage
import editprofile
import profpy
import ScrolledCanvas
import newUser

class Struct(object): pass
data = Struct()

def initAll(data,canvas):

    canvas.config(bg="black")
    # variables
    data.mode = "welcomeScreen"
    data.backToHomeButton = Button(canvas,text="Back to Home",command = lambda: backToHomeButtonPressed(data),bg="white")
    data.activeUser = None

    # init all modes
    welcome.initWelcome(canvas, data)
    homepage.initHomepage(data,canvas)
    editprofile.initEditProfile(data)
    searchscreen.initBrowse(data,canvas)
    newUser.initNewUser(data,canvas)

def backToHomeButtonPressed(data):
    print("backToHomeButton pressed")
    data.mode = "homepage"

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "welcomeScreen"): welcome.welcomeMousePressed(event, data)
    if (data.mode == "homepage"): homepage.homepageMousePressed(event,data)
    if (data.mode == "editProfile"): editprofile.editProfileMousePressed(event,data)
    if (data.mode == "browse"): searchscreen.browseMousePressed(event,data)
    if (data.mode == "newUser"): newUser.newUserMousePressed(event,data)

def keyPressed(event, data):
    if (data.mode == "welcomeScreen"): welcome.welcomeKeyPressed(event, data)
    if (data.mode == "homepage"):homepage.homepageKeyPressed(event,data)
    if (data.mode == "editProfile"):editprofile.editProfileKeyPressed(event,data)
    if (data.mode == "browse"): searchscreen.browseKeyPressed(event,data)
    if (data.mode == "newUser"): newUser.newUserKeyPressed(event,data)

def timerFired(data):
    if (data.mode == "welcomeScreen"): welcome.welcomeTimerFired(data)
    if (data.mode == "homepage"): homepage.homepageTimerFired(data)
    if (data.mode == "editProfile"): editprofile.editProfileTimerFired(data)
    if (data.mode == "browse"): searchscreen.browseTimerFired(data)
    if (data.mode == "newUser"): newUser.newUserTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "welcomeScreen"): welcome.welcomeRedrawAll(canvas, data)
    if (data.mode == "homepage"): homepage.homepageRedrawAll(canvas,data)
    if (data.mode == "editProfile"): editprofile.editProfileRedrawAll(canvas,data)
    if (data.mode == "browse"): searchscreen.browseRedrawAll(canvas,data)
    if (data.mode == "newUser"): newUser.newUserRedrawAll(canvas,data)

# placed in the main file to be binded to <Motion>
def detectHover(event,canvas,data):
    if(data.mode == "newUser"): 
        newUser.mouseMotion(event,data)
        return
    elif(data.mode == 'welcomeScreen'):
        welcome.motion(event, canvas, data)
    # if menu is already there, then show it until the mouse is off the menu
    if(data.displayMenu and
       canvas.winfo_pointerx()-canvas.winfo_rootx() < data.menuSize[0]):
        return
    # menu appears when user hovers in top left corner of window
    # top left 50 x 50 pixel square
    elif(canvas.winfo_pointerx()-canvas.winfo_rootx() > 50):
        data.displayMenu = False
    else: data.displayMenu = True

def run(width=850, height=700):
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
    data.timerDelay = 40 # milliseconds
    # create the root and the canvas
    root = Tk()
    frame = Frame(root)
    canv = ScrolledCanvas.ScrolledCanvas(root)
    data.canv = canv
    canv.pack()
    data.root = root
    canvas = canv.canvas
    initAll(data,canvas)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event: detectHover(event,canvas,data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()