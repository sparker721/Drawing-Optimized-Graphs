from tkinter import *

def parseFile(inputFile):
    f = open(inputFile, 'r')
    content = f.read()
    inputFileSplitByRow = content.splitlines()
    
    adjacencyList = {}
    
    for edge in inputFileSplitByRow:
        leftNode, rightNode = edge.split('->')[0], edge.split('->')[1]
        if leftNode in adjacencyList:
            adjacencyList[leftNode].append(rightNode)
        else:
            adjacencyList[leftNode] = [rightNode]
    
    return adjacencyList

def createNode(x, y, r, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1)

def drawNodes(values):
    window = Tk()
    canvas = Canvas(window)
    canvas.pack()

    X = 50
    Y = 40
    radius = 35 #never changes

    for value in values:
        createNode(X, Y, radius, canvas)
        canvas.create_text(X, Y, text = value)
        X += 80
        #Y += 60
        canvas.update()

    window.mainloop()

fileName = input('Please enter name of input file: ')
adjacencyList = parseFile(fileName)
drawNodes(adjacencyList.keys())