from tkinter import *
from PIL import Image
from math import *

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

    return adjacencyList

def createNode(x, y, r, canvasName): # center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, outline="black", fill="white")

def createEdge(x1, y1, x2, y2, canvasName):
    return canvasName.create_line(x1, y1, x2, y2)

def drawGraph(values):
    X = window.winfo_width()//2
    Y = window.winfo_height()//2
    radius = 35 # never changes
    total = 0

    nodes = []
    for value in values:
        nodes.append((value, [X,Y]))
        theta = total/20 * pi
        DX = (90 + 3*theta) *cos(theta)        
        DY = (90 + 3*theta) *sin(theta)
        X += DX
        Y += DY
        total += 35

    drawEdges(adjacencyList, nodes)
    canvas.update()

    X = window.winfo_width()//2
    Y = window.winfo_height()//2
    total = 0

    for value in values:
        createNode(X,Y, radius, canvas)
        canvas.create_text(X, Y, text = value)
        theta = total/20 * pi
        DX = (90 + 3*theta) *cos(theta)        
        DY = (90 + 3*theta) *sin(theta)
        X += DX
        Y += DY
        total += 35

def drawEdges(adjacencyList, nodes):
    nodes = dict(nodes)
    for item in adjacencyList:
        if(adjacencyList[item] != []):
            for i in adjacencyList[item]:
                X1 = nodes[item][0]
                Y1 = nodes[item][1]
                X2 = nodes[i][0]
                Y2 = nodes[i][1]
                createEdge(X1, Y1, X2, Y2, canvas)

fileName = input('Please enter name of input file: ')
imageFile = fileName.strip(".txt")
adjacencyList = parseFile(fileName)

window = Tk()
window.title("Drawing Optimized Graphs")
window.state("zoomed")
canvas = Canvas(window)
canvas.update()
canvas.pack(fill=BOTH, expand=YES)

drawGraph(adjacencyList.keys())
canvas.update()

canvas.postscript(file = (imageFile+".eps"), colormode = "color")
window.mainloop()
#image = Image.open((imageFile+".eps"))
#image.load(scale = 10)
#image.save((imageFile + ".jpeg"), format = "jpeg", quality = 100)
