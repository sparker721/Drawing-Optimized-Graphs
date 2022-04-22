from tkinter import *
from PIL import Image
from math import *
import re

def parseFile(inputFile):
    f = open(inputFile, 'r')
    content = f.read()
    inputFileSplitByRow = content.splitlines()
    
    adjacencyList = {}

    for edge in inputFileSplitByRow:
        # If input file does not meet formatting requirements, return error
        if (re.search("->" , edge) == None):
            print("ERROR: Please make sure formatting of input file matches 'firstNodeLabel->secondNodeLabel'")
            return None

        # Input file has weighted edges
        if (re.search("w([0-9])+" , edge) != None):
            return WeightedAdjacencyList(inputFile)
        
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

def WeightedAdjacencyList(inputFile):
    f = open(inputFile, 'r')
    content = f.read()
    inputFileSplitByRow = content.splitlines()
    
    adjacencyList = {}
    sortingList = []
    for edge in inputFileSplitByRow:
        if (re.search("w([0-9])+" , edge) == None):
            print("ERROR: Please make sure input file has specified all weighted edges")
            return None

        weight = re.search("w([0-9])+" , edge).group(0)[1:]
        edgeToDraw = re.split("w([0-9])+" , edge)[0]
        sortingList.append(weight + '#' + edgeToDraw)

    sortingList.sort()
    for item in sortingList:
        leftNode, rightNode = (item.split("#")[1]).split("->")[0], (item.split("#")[1]).split("->")[1]
        
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

if adjacencyList != None:
    window = Tk()
    window.title("Drawing Optimized Graphs")
    window.state("zoomed")
    length = len(adjacencyList)
    window.geometry("{}x{}".format(length*80, (length+2)*90))
    canvas = Canvas(window)
    canvas.update()
    canvas.pack(fill=BOTH, expand=YES)

    drawGraph(adjacencyList.keys())
    canvas.update()

    canvas.postscript(file = (imageFile+".eps"), colormode = "color")
    window.mainloop()
