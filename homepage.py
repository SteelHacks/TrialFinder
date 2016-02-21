from tkinter import *
import Scraper


def initHomepage(data,canvas):

	data.displayMenu = False
	data.searchbar = Entry(data.root,width=40)
	data.scraper = Scraper.Scraper()
	data.menuSize = (150,data.height)
	data.menuSlider = data.menuSize[0] * -1
	data.scrollbar = Scrollbar(data.root)

	# BUTTONS
	data.searchButton = Button(canvas,text="Search",command = lambda: searchButtonPressed(data)) # add options later

	#initScrollbar(data)
	initMenu(data,canvas)
	loadProfilePicture()
	loadQuickMenu()
	loadTrendingFeed()
	print("initialized homepage successfully")

def initScrollbar(data):

	data.scrollbar = Scrollbar(data.root)
	canvas = Canvas(data.root, bd=0,
                yscrollcommand=data.scrollbar.set)
	data.scrollbar.config(command=canvas.yview,state=ACTIVE)
	data.scrollbar.set(0,0)

def initMenu(data,canvas):
	print("initMenu")
	data.myProfileButton = Button(canvas,text="My Profile", command = lambda: myProfileButtonPressed(data))
	data.browseButton = Button(canvas,text="Browse",command = lambda: browseButtonPressed(data))

def browseButtonPressed(data):
	print("browse button clicked")
	data.mode = "browse"

def myProfileButtonPressed(data):
	print("myProfile button clicked")
	data.mode = "myProfile"	

def loadProfilePicture():
	print("loadProfilePicture")
	
def loadQuickMenu():
	print("loading QuickMenu")


def loadTrendingFeed():
	print("loadTrendingFeed")

def homepageKeyPressed(event,data):
	pass

def homepageTimerFired(data):
	if(data.displayMenu):
		if(data.menuSlider < 0): data.menuSlider += 15
	elif(data.menuSlider > data.menuSize[0] * -1): data.menuSlider -= 15

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
	drawSearchBar(canvas,data)
	drawMenu(canvas,data)
	data.scrollbar.pack(side=RIGHT,fill=Y)

def drawSearchBar(canvas,data):
	searchbarPos = (400,160)
	searchbuttonPos = (570,160)
	canvas.create_window(searchbarPos,window=data.searchbar)
	canvas.create_window(searchbuttonPos,window=data.searchButton)

def drawProfilePicture(canvas,data):
	canvas.create_rectangle(200,140,250,190)
	canvas.create_text(200,170,text="profile pic")

def drawMenu(canvas,data):
	canvas.create_rectangle(0 + data.menuSlider,0,data.menuSize[0] + data.menuSlider,data.menuSize[1])
	canvas.create_window(75 + data.menuSlider,230,window = data.myProfileButton)
	canvas.create_window(75 + data.menuSlider,300,window = data.browseButton)

	# replace this with user data
	canvas.create_rectangle(0 + data.menuSlider,0,data.menuSize[0] + data.menuSlider,data.menuSize[1] - 550)
	canvas.create_text(50 + data.menuSlider,50,text="user data here")

def searchButtonPressed(data):
	print("search button pressed")
	# cast to list to fit Scraper function parameter
	searchTerm = list()
	searchTerm.append(data.searchbar.get())
	searchResults = data.scraper.searchAllStudies(searchTerm)
