# my mode is the EDIT PROFILE PAAGGEEEEEEEEEEEEEE
# data.mode = editProfile

from profpy import *

from tkinter import *

def initEditProfile(data):
    data.logo = PhotoImage(file="smalogo.gif")
    data.conditionEntry = Entry(data.root, font ="Helvetica 30",text="poo", bd =5)
    data.profiles = interperateProfiles("profiles.txt")

def editProfileMousePressed(event, data):
    for i in range(8):
        # print(event.x, event.y, i)
        # print(380<event.x<410, "x")
        # print(260+50*(i) , 230+50*(i), "y", event.y)
        # print(260+50*(i) < event.y < 230+50*(i))
        if(380 < event.x < 410 and (230+50*(i)) < event.y < (260+50*(i))):
            try:
                data.profiles[data.activeUser].pop(i)
                writeFile("profiles.txt", stringProfiles(data.profiles))
            except:
                pass
        if(380+425 < event.x < 410+425 and (230+50*(i)) < event.y < (260+50*(i))):
            # print("ya")
            try:
                data.profiles[data.activeUser].pop(i+8)
                writeFile("profiles.txt", stringProfiles(data.profiles))
            except:
                pass

def editProfileKeyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Return":
        data.profiles[data.activeUser].append(data.conditionEntry.get())
        writeFile("profiles.txt", stringProfiles(data.profiles))
        data.conditionEntry.delete(0, END)
    pass

def editProfileTimerFired(data):
    pass

def editProfileRedrawAll(canvas, data):
    canvas.create_window(data.width - 100, data.height - 100, window = data.backToHomeButton)
    canvas.create_rectangle(0,0,data.width,data.height, fill="black")
    # canvas.create_image(data.width/2,data.height/2,image=data.ground)
    canvas.create_image(660,100, image=data.logo)
    canvas.create_text(30,80,font="Helvetica 36", fill="white", text="My Profile  -  " + data.activeUser, anchor="sw")
    canvas.create_text(30,140,font="Helvetica 24", fill="white",text="Add a Topic of Interest:", anchor="sw")
    canvas.create_window(30,215, window= data.conditionEntry, anchor="sw")    
    for x in range(len(data.profiles[data.activeUser])):
        canvas.create_text(30+(425*(x//8)), 260 + 50 * (x%8), fill="white", text=data.profiles[data.activeUser][x], font="Helvetica 24", anchor = "sw")
        canvas.create_rectangle(380+(425*(x//8)), 260+50*(x%8), 410+(425*(x//8)), 230+50*(x%8), fill="red")
        canvas.create_text(395+(425*(x//8)), 245 +50*(x%8), text="X",anchor="center")