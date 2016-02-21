import Utilities
from tkinter import *
from profpy import *

def initWelcome(canvas, data):
    data.activeUser = None
    data.userList = list()
    data.nameSelected = None
    data.profiles = interperateProfiles("profiles.txt")
    print(data.profiles, "ps")
    for line in Utilities.readFile("profiles.txt").splitlines():
        endName = line.find(":")
        data.userList.append(line[:endName])
    data.nameList = []
    data.nameButtons = []
    for name in data.profiles:
        # print(name)
        # button = Button(canvas, text = "Login", command = login())
        data.nameList.append(name)
    data.nameList = sorted(data.nameList)

    data.newUserButton = Button(data.root, text="Create New User",bd=0,
            activebackground="black",command=lambda:newUserButtonPressed(data),overrelief=SUNKEN,
            font="Helvetica 14 bold",bg="black",fg="white",activeforeground="grey")

def newUserButtonPressed(data):
    data.mode = "newUser"

def continueButtonPressed(data):
    data.mode = "homepage"

def welcomeMousePressed(event, data):
    data.activeUser = data.nameSelected if data.nameSelected != None else None
    if(data.nameSelected != None):
        data.mode = 'homepage'

def welcomeKeyPressed(event, data):
    pass

def welcomeTimerFired(data):
    pass

def motion(event, canvas, data):
    (x,y) = (event.x, event.y)
    index = None
    if(x > 11 * data.width // 24 and x <  13 * data.width // 24):
        if(y > 340 and y < 360):
            index = 0
        elif(y > 390 and y < 410):
            index = 1
        elif(y > 440 and y < 460):
            index = 2
        elif(y > 490 and y < 510):
            index = 3
    else:
        data.nameSelected = None
    if(index != None):
        try:
            data.nameSelected = data.nameList[index]
        except: data.nameSelected = None
    print(data.nameSelected)


def welcomeRedrawAll(canvas, data):
    canvas.create_text(data.width/2,300,text="Log in as:", font="Helvetica 28",fill="white")
    for name in range(len(data.nameList)):
        canvas.create_text(data.width/2, 350+50*name, text=data.nameList[name], 
            font="Helvetica 28" if data.nameSelected == data.nameList[name] else 'Helvetica 20', 
            fill="white" if data.nameSelected == data.nameList[name] else 'grey')
    canvas.create_image(data.width/2,100, image=data.logo)
    canvas.create_text(data.width/2,230, text="Welcome.",font="Helvetica 40",fill="white")
    # canvas.create_window(data.width - 50, data.height - 150, window=data.continueButton)
    canvas.create_window(data.width/2, data.height - 150, window=data.newUserButton)




