import Utilities
from tkinter import *

def initWelcome(data):
    data.userList = list()
    for line in Utilities.readFile("profiles.txt").splitlines():
        endName = line.find(":")
        data.userList.append(line[:endName])
    data.continueButton = Button(data.root,text="Continue",command= lambda:continueButtonPressed(data))
    data.newUserButton = Button(data.root,text="Create New User",command= lambda:newUserButtonPressed(data))

def newUserButtonPressed(data):
    data.mode = "newUser"

def continueButtonPressed(data):
    data.mode = "homepage"

def welcomeMousePressed(event, data):
    pass

def welcomeKeyPressed(event, data):
    pass

def welcomeTimerFired(data):
    pass

def welcomeRedrawAll(canvas, data):
    canvas.create_image(data.width/2,100, image=data.logo)
    canvas.create_text(data.width/2,250, text="Welcome.",font="Helvetica 20",fill="white")
    canvas.create_window(data.width - 50, data.height - 150, window=data.continueButton)
    canvas.create_window(data.width - 50, data.height - 250, window=data.newUserButton)