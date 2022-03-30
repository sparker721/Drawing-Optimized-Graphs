from tkinter import *
from PIL import Image

def parseFile(inputFile):
    f = open(inputFile, 'r')
    content = f.read()
    inputFileSplitByRow = content.splitlines()
    
    adjacencyList = {}
    
    for edge in inputFileSplitByRow:
        leftNode, rightNode = edge.split('->')[0], edge.split('->')[1]
        
        if leftNode in adjacencyList:
            adjacencyList[leftNode].append(rightNode)
            if rightNode not in adjacencyList:
                adjacencyList[rightNode] = [leftNode]
            else:
                adjacencyList[rightNode].append(leftNode)
        
        else:
            adjacencyList[leftNode] = [rightNode]
            adjacencyList[rightNode] = [leftNode]

    print(adjacencyList)
    return adjacencyList

def createNode(x, y, r, canvasName): # center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1)

def drawNodes(values):
    window = Tk()
    window.title("Drawing Optimized Graphs")
    window.state("zoomed")
    canvas = Canvas(window)
    canvas.pack(fill="both", expand=True)

    X = 50
    Y = 40
    radius = 35 # never changes

    for value in values:
        createNode(X, Y, radius, canvas)
        canvas.create_text(X, Y, text = value)
        X += 80
        #Y += 60
        canvas.update()

    canvas.postscript(file = (imageFile+".eps"), colormode = "color")
    window.mainloop()
    image = Image.open((imageFile+".eps"))
    image.load(scale = 10)
    image.save((imageFile + ".jpeg"), format = "jpeg", quality = 100)


fileName = input('Please enter name of input file: ')
imageFile = fileName.strip(".txt")
adjacencyList = parseFile(fileName)
drawNodes(adjacencyList.keys())

# resize window
# x,y axis thing, draw lines, can have overlapping edges (place em in a circle)
# place circles on large 2D grid
