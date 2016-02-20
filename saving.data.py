# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *

####################################
# customize these functions
####################################



def init(data):
    data.nameEntry = Entry(data.root, bd =10)
    data.conditionEntry = Entry(data.root, bd =10)
    # data.nameEntry.pack(side = RIGHT)    # e.pack()

    data.profiles = dict()

    # e.delete(0, END)
    # e.insert(0, "a default value")


a = dict()
a["yes"] = ["a", "b", "d"]
a["no"] = ["j", "k", "l"]


def stringProfiles(profiles):
    textFile = readFile("profiles.txt")
    for person in profiles:
        textFile += person + ":"
        for char in profiles[person]:
            textFile += char + ","
        textFile += "\n"
    return textFile



def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()





def mousePressed(event, data):
    if(400 < event.x < 600 and 50 < event.y < 150):
        if(data.nameEntry.get() not in data.profiles):
            data.profiles[data.nameEntry.get()] = set()
        data.profiles[data.nameEntry.get()].add(data.conditionEntry.get())
    writeFile("profiles.txt", stringProfiles(data.profiles))
    print(data.profiles)
    # use event.x and event.y
    pass

def keyPressed(event, data):
    pass        
        # writeFile("profiles.txt", stringProfiles(data.nameEntry.get())




def timerFired(data):
    pass

def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="lightblue")
    canvas.create_window(200, 150, window= data.conditionEntry)
    canvas.create_text(50, 150, text="condition")
    canvas.create_text(50,50,text="profile name")
    canvas.create_window(200,50, window= data.nameEntry)
    canvas.create_rectangle(400,50,600,150, activefill="grey", fill="red")
    canvas.create_text(500,100, text="save")


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
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
    data.timerDelay = 10000 # milliseconds
    # create the root and the canvas
    root = Tk()



    data.root = root




    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    init(data)

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app

    root.mainloop()  # blocks until window is closed

    print("bye!")

run(800, 600)