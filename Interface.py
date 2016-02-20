#Animation framework adapted form 15-112 @ CMU course notes

from tkinter import *

#converts rgb values to usable color strings
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

####################################
# customize these functions
####################################

def init(data):
    loadImages(data)
    initLogin(data)

def initLogin(data):
    data.mode = "login"
    loginButtonColor = "blue"
    print(loginButtonColor)
    data.loginButton = Button(data.canvas, text = "Login", 
        command = loginPressed, bg = "red")


def loginPressed():
    print(1)

def loadImages(data):
    data.loginImage = PhotoImage(file = "login.gif")

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if(data.mode == "login"):
        drawLogin(canvas, data)

def drawLogin(canvas, data):
    canvas.create_image(0, 0, anchor = NW, image = data.loginImage)
    canvas.create_window(50,50, window = data.loginButton)

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
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    data.canvas = canvas
    data.root = root
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

run(850, 700)