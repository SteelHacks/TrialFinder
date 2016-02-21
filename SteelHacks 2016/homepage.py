from tkinter import *
import Scraper
import searchscreen
import profpy

def initHomepage(data,canvas):
	print("initializing")
	data.favs = profpy.interperateProfiles("favs.txt")
	data.displayMenu = False
	data.searchbar = Entry(data.root,width=40)
	data.scraper = Scraper.Scraper()
	data.menuSize = (150,data.height)
	data.menuSlider = data.menuSize[0] * -1
	data.favsLoaded = False
	data.favsPreviews = dict()
	data.favsSummaries = dict()
	data.lag = False

	# BUTTONS
	data.searchButton = Button(canvas,text="Search",command = lambda: searchButtonPressed(data)) # add options later

	initMenu(data,canvas)
	loadProfilePicture()
	loadQuickMenu()
	loadUsersTrials()

def initMenu(data,canvas):
	print("initMenu")
	data.myProfileButton = Button(canvas,text="My Profile", command = lambda: myProfileButtonPressed(data))
	data.browseButton = Button(canvas,text="Browse",command = lambda: browseButtonPressed(data))

def browseButtonPressed(data):
	print("browse button clicked")
	data.mode = "browse"

def myProfileButtonPressed(data):
	print("myProfile button clicked")
	data.mode = "editProfile"	

def loadProfilePicture():
	print("loadProfilePicture")
	
def loadQuickMenu():
	print("loading QuickMenu")


def loadUsersTrials():
	print("loading user's trials")


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
	canvas.create_image(data.width/2-30,160, image=data.logo)
	drawSearchBar(canvas,data)
	drawMenu(canvas,data)
	if(data.lag):
		try:drawFavs(canvas, data)
		except: pass
	data.lag = True

def drawFavs(canvas, data):
	#list of urls favorited by the current user
	print(data.favs, end = "<-----")
	favs = data.favs[data.activeUser]
	x = 237
	y = 380
	for url in favs:
		if url not in data.favsPreviews.keys():
			preview = data.scraper.getPreview(url,True).split("\n")
			data.favsPreviews[url] = preview
			#data.favsSummaries[url] = data.scraper.getSummary(url,True)
		else:
			preview = data.favsPreviews[url]
		(charLimit, spacing, endGap) = (41,32,37)
		y = searchscreen.createTitle(canvas, preview[0], "Helvetica 18", charLimit, x, y, spacing, endGap)
		(charLimit, spacing, endGap) = (100,15,30)
		y = searchscreen.createTitle(canvas, preview[1], "Helvetica 12", charLimit, x, y, spacing, endGap)
		(charLimit, spacing, endGap) = (90,15,55)
		y = searchscreen.createTitle(canvas, preview[2], "Helvetica 8",  charLimit, x, y, spacing, endGap)

def drawSearchBar(canvas,data):
	searchbarPos = (420,210)
	searchbuttonPos = (590,210)
	canvas.create_window(searchbarPos,window=data.searchbar)
	canvas.create_window(searchbuttonPos,window=data.searchButton)

def drawProfilePicture(canvas,data):
	canvas.create_rectangle(220,190,270,240,fill="white")
	canvas.create_text(200,220,text="profile pic",fill="white")

def drawMenu(canvas,data):
	canvas.create_rectangle(0 + data.menuSlider,0,data.menuSize[0] + data.menuSlider,data.menuSize[1],fill="white")
	canvas.create_window(75 + data.menuSlider,230,window = data.myProfileButton)
	canvas.create_window(75 + data.menuSlider,300,window = data.browseButton)
	# replace this with user data
	canvas.create_rectangle(0 + data.menuSlider,0,data.menuSize[0] + data.menuSlider,data.menuSize[1] - 550,fill="white")
	canvas.create_text(50 + data.menuSlider,50,text=data.activeUser,fill="black")

def searchButtonPressed(data):
	print("search button pressed")
	data.mode = "browse"
	searchTerm = list()
	searchTerm.append(data.searchbar.get())
	data.titles = data.scraper.searchAllStudies(searchTerm)
	searchscreen.updateSearchList(data)