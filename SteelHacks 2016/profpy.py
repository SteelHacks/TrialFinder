
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
        if name != "":
            profiles[name] = []
        try:
            for condition in line.split(":")[1].split(","):
                if(condition != ""):
                    # print(condition)
                    profiles[name].append(condition)
        except:
            pass
    return profiles

def addProfileCondition(name, condition, data):
    # print(" THIS IS AHTEHHEA WHAH", data.profiles)
    if name not in data.profiles:
        data.profiles[name] = []
    data.profiles[name].append(condition)

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()