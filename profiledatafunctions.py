# this is outline for the functions we use to store data of profiles
# data in profiles is stored as a dictionary in our computations
# the key is the name of the profile and it is linked to the set of diseases
# when the data is saved as a .txt file, the format is NAME:CONDITION,CONDITION,...
# the fucntions are:

#             stringProfiles(profiles)
#                 takes in dictionary and makes .txt format string

#             interperateProfiles(textFile)
#                 takes in string of text file and makes dictionary format

#             addProfileCondition(name, condition, data):
#                 adds to dictionary



from tkinter import *

####################################
# customize these functions
####################################



def init(data):
    data.nameEntry = Entry(data.root, bd =10)
    data.conditionEntry = Entry(data.root, bd =10)
    # data.nameEntry.pack(side = RIGHT)    # e.pack()

    data.profiles = interperateProfiles("profiles.txt")


    # e.delete(0, END)
    # e.insert(0, "a default value")

#example of way profile and conditions are stored
#yes/no are names, letters are conditions
#edit: conditions are actually sets now
a = dict()
a["yes"] = ["a", "b", "d"]
a["no"] = ["j", "k", "l"]


def stringProfiles(profiles):
    #this takes the dictionary string->set and makes it the .txt file
    textFile = ""
    for person in profiles:
        textFile += person + ":"
        for char in profiles[person]:
            textFile += char + ","
        textFile += "\n"
    return textFile

def interperateProfiles(textFile):
    #this takes the .txt file and makes it the dictionary  string->set
    textFile = readFile(textFile)
    profiles = dict()
    for line in textFile.split("\n"):
        name = line.split(":")[0]
        # print(line.split(":"))
        if name != "":
            print(name)
            profiles[name] = set()
        try:
            for condition in line.split(":")[1].split(","):
                if(condition != ""):
                    print(condition)
                    profiles[name].add(condition)
        except:
            pass
    return profiles
    # print(profiles)
    # return profiles

def addProfileCondition(name, condition, data):
    # print(" THIS IS AHTEHHEA WHAH", data.profiles)
    if name not in data.profiles:
        data.profiles[name] = set()
    data.profiles[name].add(condition)



def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()





def mousePressed(event, data):
    if(400 < event.x < 600 and 50 < event.y < 150):
        addProfileCondition(data.nameEntry.get(),data.conditionEntry.get(), data)
        writeFile("profiles.txt", stringProfiles(data.profiles))
    # use event.x and event.y

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


run(800, 600)