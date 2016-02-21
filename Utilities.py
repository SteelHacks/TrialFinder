import string

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def ASCIIfy(string):
    return ''.join(i for i in string if ord(i)<128)

    
