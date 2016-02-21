# my mode is the EDIT PROFILE PAAGGEEEEEEEEEEEEEE
# data.mode = editProfile

from profpy import *



from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.ground = PhotoImage(file="ground.gif")
    data.image = PhotoImage(file="smalogo.gif")
    print(data.image)
    data.conditionEntry = Entry(data.root, font ="Helvetica 44",text="poo", bd =5)
    data.mode = "editProfile"
    data.currentUser = "Scott"
    data.profiles = interperateProfiles("profiles.txt")

def mousePressed(event, data):
    for i in range(8):
        # print(event.x, event.y, i)
        # print(380<event.x<410, "x")
        # print(260+50*(i) , 230+50*(i), "y", event.y)
        # print(260+50*(i) < event.y < 230+50*(i))
        if(380 < event.x < 410 and (230+50*(i)) < event.y < (260+50*(i))):
            try:
                data.profiles[data.currentUser].pop(i)
                writeFile("profiles.txt", stringProfiles(data.profiles))
            except:
                pass
        if(380+425 < event.x < 410+425 and (230+50*(i)) < event.y < (260+50*(i))):
            # print("ya")
            try:
                data.profiles[data.currentUser].pop(i+8)
                writeFile("profiles.txt", stringProfiles(data.profiles))
            except:
                pass


def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Return":
        data.profiles[data.currentUser].append(data.conditionEntry.get())
        writeFile("profiles.txt", stringProfiles(data.profiles))
        data.conditionEntry.delete(0, END)
    pass

def timerFired(data):
    pass



def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height, fill="black")
    # canvas.create_image(data.width/2,data.height/2,image=data.ground)
    canvas.create_image(660,100, image=data.image)
    canvas.create_text(30,80,font="Helvetica 44", fill="white", text="My Profile  -  " + data.currentUser, anchor="sw")
    canvas.create_text(30,140,font="Helvetica 24", fill="white",text="Add a Topic of Interest:", anchor="sw")
    canvas.create_window(30,215, window= data.conditionEntry, anchor="sw")    
    for x in range(len(data.profiles[data.currentUser])):
        canvas.create_text(30+(425*(x//8)), 260 + 50 * (x%8), fill="white", text=data.profiles[data.currentUser][x], font="Helvetica 24", anchor = "sw")
        canvas.create_rectangle(380+(425*(x//8)), 260+50*(x%8), 410+(425*(x//8)), 230+50*(x%8), fill="red")
        canvas.create_text(395+(425*(x//8)), 245 +50*(x%8), text="X",anchor="center")


####################################
# use the run function as-is
####################################

def run(width=850, height=650):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
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
    data.timerDelay = 1000 # milliseconds
    # create the root and the canvas
    root = Tk()
    data.root = root

    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    init(data)
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()