from tkinter import *

class Struct(object): pass
data = Struct()

def initHomepage(data,canvas):

	data.displayMenu = False
	data.searchButton = Button(canvas,text="Search",command=searchButtonPressed) # add options later

	data.searchbar = Entry(data.root,width=40)

	initMenu()
	loadProfilePicture()
	loadQuickMenu()
	loadTrendingFeed()
	print("initialized homepage successfully")

def initMenu():
	print("initMenu")

def loadProfilePicture():
	print("loadProfilePicture")
	
def loadQuickMenu():
	print("loadQuickMenu")

def loadTrendingFeed():
	print("loadTrendingFeed")

def homepageKeyPressed(event,data):
	pass

def homepageTimerFired(data):
    pass

def homepageMousePressed(event,data):
	pass

def detectHover(event,canvas,data):
	# menu appears when user hovers in top left corner of window
	if(canvas.winfo_pointerx()-canvas.winfo_rootx() > 50 or 
	   canvas.winfo_pointery()-canvas.winfo_rooty() > 50):
		data.displayMenu = False
		return
	# function returns if not top left corner
	data.displayMenu = True

def homepageRedrawAll(canvas,data):
	drawProfilePicture(canvas,data)
	drawQuickMenu(canvas,data)
	drawSearchBar(canvas,data)
	if(data.displayMenu):
		drawMenu(canvas,data)

def drawSearchBar(canvas,data):
	searchbarPos = (320,50)
	searchbuttonPos = (500,50)
	canvas.create_window(searchbarPos,window=data.searchbar)
	canvas.create_window(searchbuttonPos,window=data.searchButton)

def drawQuickMenu(canvas,data):
	canvas.create_rectangle(280,200,650,250)
	canvas.create_text(280,200,text="quickmenu")

def drawProfilePicture(canvas,data):
	canvas.create_rectangle(200,200,250,250)
	canvas.create_text(200,200,text="profile pic")

def drawMenu(canvas,data):
	canvas.create_rectangle(0,0,150,data.height)

def searchButtonPressed():
	print("search button pressed")
	print("search term: ",data.searchbar.get())

def run(width=850, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        homepageRedrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        homepageMousePressed(event,data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        homepageKeyPressed(event,data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        homepageTimerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    data.root = root
    initHomepage(data,canvas)
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
