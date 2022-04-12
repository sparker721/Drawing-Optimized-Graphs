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
                adjacencyList[rightNode] = []
        
        else:
            adjacencyList[leftNode] = [rightNode]
            adjacencyList[rightNode] = []

    return adjacencyList

def createNode(x, y, r, canvasName): # center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1)

def createEdge(x1, y1, x2, y2, canvasName):
    totalX = abs(x2 - x1)
    totalY = abs(y2 - y1)

    if(abs(totalX) <= 1):
        if(y1 > y2):
            y1 -= 35
            y2 += 35
        else:
            y1 += 35
            y2 -= 35

    elif(abs(totalY) <= 1):
        if(x1 > x2):
            x1 -= 35
            x2 += 35
        else:
            x1 += 35
            x2 -= 35

    else:
        if(x1 < x2 and y1 < y2):
            x1 += 35*sin(totalX/totalY)
            x2 -= 35*sin(totalX/totalY)
            y1 += 35*cos(totalX/totalY)
            y2 -= 35*cos(totalX/totalY)

        elif(x1 > x2 and y1 < y2):
            x1 -= 35*sin(totalX/totalY)
            x2 += 35*sin(totalX/totalY)
            y1 += 35*cos(totalX/totalY)
            y2 -= 35*cos(totalX/totalY)

        elif(x1 < x2 and y1 > y2):
            x1 += 35*sin(totalX/totalY)
            x2 -= 35*sin(totalX/totalY)
            y1 -= 35*cos(totalX/totalY)
            y2 += 35*cos(totalX/totalY)

        else:
            x1 -= 35*sin(totalX/totalY)
            x2 += 35*sin(totalX/totalY)
            y1 -= 35*cos(totalX/totalY)
            y2 += 35*cos(totalX/totalY)

    return canvasName.create_line(x1, y1, x2, y2)

def drawNodes(values):
    centerX = window.winfo_width()//2
    centerY = window.winfo_height()//2
    X = centerX
    Y = centerY
    radius = 35 # never changes
    total = 0

    for value in values:
        createNode(X,Y, radius, canvas)
        canvas.create_text(X, Y, text = value)
        nodes.append((value, [X,Y]))
        theta = total/20 * pi
        DX = (90 + 3*theta) *cos(theta)        
        DY = (90 + 3*theta) *sin(theta)
        X += DX
        Y += DY
        total += 36

def drawEdges(AdjacencyList, nodes):
    nodes = dict(nodes)
    for item in AdjacencyList:
        if(AdjacencyList[item] != []):
            for i in AdjacencyList[item]:
                X1 = nodes[item][0]
                Y1 = nodes[item][1]
                X2 = nodes[i][0]
                Y2 = nodes[i][1]
                createEdge(X1, Y1, X2, Y2, canvas)

fileName = input('Please enter name of input file: ')
imageFile = fileName.strip(".txt")
adjacencyList = parseFile(fileName)
nodes = []

window = Tk()
window.title("Drawing Optimized Graphs")
window.state("zoomed")
canvas = Canvas(window)
canvas.pack(fill="both", expand=True)
canvas.update()

print(adjacencyList)
drawNodes(adjacencyList.keys())
print(nodes)
drawEdges(adjacencyList, nodes)

canvas.postscript(file = (imageFile+".eps"), colormode = "color")
window.mainloop()
image = Image.open((imageFile+".eps"))
image.load(scale = 10)
image.save((imageFile + ".jpeg"), format = "jpeg", quality = 100)

