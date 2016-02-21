# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
from ScrolledCanvas import *

####################################
# customize these functions
####################################

def init(data):
    #scrollbar = Scrollbar(data.root, orient = VERTICAL)
    #data.canvas.config(yscrollcommand = scrollbar.set)
    #scrollbar.pack(side = RIGHT, fill=Y )
    #scrollbar.config(command=data.canvas.yview)
    pass

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    data.x += data.speed

def redrawAll(canvas, data):
    canvas.create_rectangle(data.x,data.y,data.x+50,data.y + 50,fill='red')

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
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
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    frame = Frame(root)
    canv = ScrolledCanvas(root)
    data.canv = canv
    canv.pack()
    data.root = root
    canvas = canv.canvas
    init(data)
    data.speed = 5
    data.x = 0
    data.y = 500
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(850, 650)