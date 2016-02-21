from tkinter import *
from ScrolledCanvas import *
from profpy import *

####################################
# customize these functions
####################################

def initNewUser(data,canvas):
    data.profiles = interperateProfiles('profiles.txt')
    data.title = "Welcome New User!"
    data.nameEntry = Entry(data.root, bd = 10)
    data.ageEntry = Entry(data.root, bd = 10)
    data.genderEntry = Entry(data.root, bd = 10)
    data.yesSelected = False
    data.noSelected = False
    data.drawMedicalHistory = False
    data.conditionsEntry = Entry(data.root, bd = 10)
    data.submitSelected = False
    data.logo = PhotoImage(file = 'smalogo.gif')
    data.submitConditionsButton = Button(canvas,text="Submit",command=lambda:submitSelected(data))
    
def newUserMousePressed(event, data):
    if(data.yesSelected):
        yesPressed(event, data)
    elif(data.noSelected):
        noPressed(event, data)
    elif(data.submitSelected):
        submitSelected(data)


def submitSelected(data):
    entry = data.conditionsEntry.get()
    name = data.nameEntry.get()
    addProfileCondition(name, entry, data)
    writeFile('profiles.txt', stringProfiles(data.profiles))
    data.nameEntry.delete(0, END)
    data.ageEntry.delete(0, END)
    data.genderEntry.delete(0, END)
    data.conditionsEntry.delete(0, END)
    data.mode = "homepage"

def yesPressed(event, data):
    data.drawMedicalHistory = True

def noPressed(event, data):
    pass

def newUserKeyPressed(event, data):
    # use event.char and event.keysym
    pass

def newUserTimerFired(data):
    pass

def newUserRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,1000, fill = 'black')
    canvas.create_text(data.width//2,20,text = data.title, fill = "white", font ='Serif 65',
        anchor = N)
    canvas.create_text(data.width//2,130,text = 'Tell us a little about yourself...',
        fill = 'gray', font = 'Serif 28')
    y = 200
    canvas.create_text(data.width//2, y,text = 'What\'s your name?', 
        fill = 'gray', font = 'Serif 22')
    y += 30
    canvas.create_window(data.width//2,y, anchor = N, width = 400,
     height = 45, window = data.nameEntry)
    y += 70
    canvas.create_text(data.width//2, y,text = 'How old are you?', 
        fill = 'gray', font = 'Serif 22')
    y += 30
    canvas.create_window(data.width//2,y, anchor = N, width = 400, height = 45, 
        window = data.ageEntry)
    y += 70
    canvas.create_text(data.width//2, y,text = 'What is your gender?', 
        fill = 'gray', font = 'Serif 22')
    y += 30
    canvas.create_window(data.width//2,y, anchor = N, width = 400, height = 45, 
        window = data.genderEntry)
    y += 85
    canvas.create_text(data.width//2, y,
        text = """  Mind if we learn a little about your medical history?\nThis will allow us to find the trials that are best for you""", 
        fill = 'gray', font = 'Serif 22')
    y += 50
    canvas.create_text(3 * data.width//7, y, text = "Yes", 
        fill = 'white' if data.yesSelected else 'gray', 
        font = 'Serif 28' if data.yesSelected else 'Serif 22', anchor = N)
    canvas.create_text(4 * data.width//7, y, text = "No", 
        fill = 'white' if data.noSelected else 'gray', 
        font = 'Serif 28' if data.noSelected else 'Serif 22', anchor = N)
    if(data.drawMedicalHistory):
        drawMedicalHistory(canvas, data)

def drawMedicalHistory(canvas, data):
    print("hello")
    y = 605
    canvas.create_text(data.width//2, y, text = "Enter some of your previous medical conditions:", font = 'Serif 22',
        fill = 'gray', anchor = N)
    y += 50
    canvas.create_window(data.width//2,y, anchor = N, width = 400, height = 45, window = data.conditionsEntry)
    y += 60
    canvas.create_window(data.width//2,y, anchor = N, width = 400, height = 45, window = data.submitConditionsButton)
    canvas.create_image(data.width//2, y + 70, anchor = N, image = data.logo)

    
def getSelected(x,y, data):
    if(x > 340 and y > 575 and x < 390 and y < 590):
        data.yesSelected = True
    else: 
        data.yesSelected = False

    if(x > 470 and y > 575 and x < 500 and y < 595):
        data.noSelected = True
    else: 
        data.noSelected = False
    if(x > 380 and y > 370 and x < 465 and y < 390):
        data.submitSelected = True
    else:
        data.submitSelected = False

def mouseMotion(event, data):
    getSelected(event.x, event.y, data)