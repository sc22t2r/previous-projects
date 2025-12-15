from ursina import * 
import guizero
import sys
from math import *
from random import *
app=Ursina() 
buttonList=[]
graphType=[]
objVertexList=[None]
#if the list starts with nothing, the bespoke update function errors
objEdgeList=[]
endPoint=[]
vertexStrList2=[None]
#if the list starts with nothing, the bespoke update function errors
initEdges=[]
moveVertex=[None]
#if the list starts with nothing, the bespoke update function error
alphabetList=["a","b","c","d","e","f","g","h","i","j","k","l","m"]
#for names of random vertices
edgeCon=[]#list of which vertex are connected to each other
discoveryOrder=[]
seq1=Sequence()
chosenAlgorithm=None
count=0

def traversalDisplay(nextpage):
    """this function displays the graph 
    traversal algorithms selection through buttons"""
    clearScreen()
    BFSButton=button1("BFS",0,3,nextpage,10,1)
    DFSButton=button1("DFS",0,1,nextpage,10,1)
    AstarButton=button1("A*",0,-1,nextpage,10,1)
    dijkstraButton=button1("Dijkstra",0,-3,nextpage,10,1)
    global buttonList 
    # means that clear screen has access and can remove these buttons
    buttonList=[BFSButton,DFSButton,AstarButton,dijkstraButton]

def inputMakeGraph():
    """this function is using buttons to determine if the user wants a 
    weighted or unweighted graph"""
    clearScreen()
    weightedButton=button1("weighted",0,3,"inputMakeGraph2",10,1)
    unweightedButton=button1("unweighted",0,-3,"inputMakeGraph2",10,1)
    global buttonList 
    # means that clear screen has access and can remove these buttons
    buttonList=[weightedButton,unweightedButton]

def inputMakeGraph2():
    """this function uses buttons to determine if the user wants a directed 
    or undirected graph"""
    graphType.append(buttonChecker())
    #adds whether or not the graph is weighted to a list describing the graph
    clearScreen()
    directedButton=button1("directed",0,3,"inputMakeGraph3",10,1)
    undirectedButton=button1("undirected",0,-3,"inputMakeGraph3",10,1)
    global buttonList # means that clear screen has access and can remove these buttons
    buttonList=[directedButton,undirectedButton]

def inputMakeGraph3():
    """this determines whether the user wants a random or user made graph"""
    graphType.append(buttonChecker())
    #adds whether or not the graph is directed to a list describing the graph
    clearScreen()
    randomButton=button1("random",0,3,"makeGraph",10,1)
    userMadeButton=button1("usermade",0,-3,"inputUser",10,1)
    global buttonList 
    # means that clear screen has access and can remove these buttons
    buttonList=[randomButton,userMadeButton]

def destruction():
    """removes the guizero window"""
    app1.destroy()#needs to be a separate function

def stringToList(string1):
    """changes the user input (vertices, edges and weights)
     into easier to use list"""
    finalList=[]
    
    while "," in string1:
        curRecord=string1[0:string1.index(",")]
        #find the first comma
        curRecord=curRecord.strip()
        #remove all white space
        finalList.append(curRecord)
        string1=string1[string1.index(",")+1:]
        #make string everything not including curRecord
    
    string1=string1.strip()
    #remove all whitespace
    finalList.append(string1)
    return finalList

def inputUser():
    """this produces a guizero window 
    for the user to manually input data into"""
    global app1
    #so that the destruction function can access it
    app1=guizero.App()
    #make the screen for the user input
    app1.width=3000
    app1.height=3000
    vertexText="input the names of all vertices, separating each with a comma"
    inputVertex=guizero.TextBox(app1,text=vertexText,width=2500)
    edgeText="input the names of all edges, separating each with a comma"
    inputEdge=guizero.TextBox(app1,text=edgeText,width=2500)
    weightText1="input the names of all weights, separating each with a comma "
    weightText2="please enter the weights in the same order as the edges"
    weightText=weightText1+weightText2
    inputWeight=guizero.TextBox(app1,text=weightText,width=2500)

    if graphType[0]=="weighted":
        inputWeight.visible=True

    else:
        inputWeight.visible=False

    #only allows user to see the weighted box
    #if they clicked on the weighted button
    destroyText="press when finished"
    destroyButton=guizero.PushButton(app1,text=destroyText,command=destruction)
    #shuts down the window
    app1.display()
    repeat=False#does the function need to run again
    vertexList=stringToList(inputVertex.value)
    edgeList=stringToList(inputEdge.value)
    edgeList2=[]
    """for loop below finds the two vertices that define 
    the edges, and makes that into a new list"""
    for i in range(len(edgeList)):
        comparison=[]
        for j in range(len(vertexList)):

            if vertexList[j] in edgeList[i]:
                comparison.append(vertexList[j])

        if len(comparison)!=2:
        #cannot have an edge that connects to more than 2 vertices
            repeat=True
        else:
            if comparison[0]+comparison[1]==edgeList[i]:
                #checks if this is an edge that exists
                edgeList2.append(comparison)

            elif comparison[1]+comparison[0]==edgeList[i]:
                edgeList2.append(comparison[::-1])
                #comparison is always ordered the same as in vertex list,
                #so sometimes needs changing

    weightList=stringToList(inputWeight.value)
    if len(weightList)!=len(edgeList2) and graphType[0]=="weighted":
        repeat=True
            #every edge needs a weight
    weightList2=[]
    for i in range(len(edgeList2)):
        if graphType[0]=="weighted":
            try:
                weightList2.append(int(weightList[i]))
            except:
                # this is occuring when the weightlist term isn't an integer
                repeat=True
        else:
            weightList2.append(0)
    if repeat==True:
        inputUser()
        #if the user has inputted data wrong, the window reappears

    elif repeat==False:
        graphType.append(vertexList)
        graphType.append(edgeList2)
        graphType.append(weightList2)
        #add the vertices, edges and weights to the graph description
        makeGraph()

def makeGraph():
    """this section actually makes and displays the graph,
    also making the random input if they have asked for a random graph"""
    clearScreen()

    if len(graphType)==2:
        #if the graph is random
        vertexNum=randint(6,12)
        edgeNum=(randint(vertexNum-1,int(vertexNum*(vertexNum-1)/2)))
        #random number of edges, between the minimum and maximum number
        vertexNames=alphabetList[:vertexNum]
        #take the first letters of alphabet, make them names of the vertices
        vertexNames2=vertexNames[:]
        #duplicate the list
        graphType.append(vertexNames2)
        #add names of vertices to graph description
        shuffle(vertexNames)
        treeLength=len(vertexNames)-1
        #all lengths of trees are one less than number of vertices

        for i in range(treeLength):
            initEdges.append([vertexNames[i],vertexNames[i+1]])
            #ensures that the graph can be traversed

        edgesLeft=edgeNum-treeLength

        while edgesLeft!=0:
            startvertex=choice(vertexNames)
            endvertex=choice(vertexNames)
            newEdge=[startvertex,endvertex]

            if endvertex!=startvertex:
                if newEdge not in initEdges and newEdge[::-1] not in initEdges:
                    #if the edge is not already in the list
                    initEdges.append(newEdge)
                    edgesLeft+=-1

        graphType.append(initEdges)
        #add list of random edges to graph description
        weightList=[]

        for i in range(edgeNum):
            if graphType[0]=="weighted":
                weightList.append(randint(6,30))
                # 6 is the minimum number of the heuristic value for A*

            else:
                weightList.append(0)

        graphType.append(weightList)
        #add list of random weights to graph description

    wText1="input the names of all weights" 
    wText2="separating each with a comma please"
    wText3="enter the weights in the same order as the edges"
    #made in a different function, so not accessible through
    #  local scope, so needs to be made again
    if graphType[0]=="unweighted" and graphType[4]==[wText1,wText2,wText3]:
        del graphType[4]
        #remove the incorrect weight list
        newList=[]
        
        for i in range(len(graphType[3])):
            newList.append(0)
        
        graphType.append(newList)
        #add a new weight list with the same number of elements as the edgelist
    
    vertexStrList=graphType[2]
    
    for i in range(len(vertexStrList)):
        vertexStrList2.append(vertexStrList[i])
    
    positions=posFinder(len(vertexStrList))
    #find where to initially put the vertices
    
    for i in range(len(vertexStrList)):
        curVertex=vertex(vertexStrList[i],positions[i])
        objVertexList.append(curVertex)
        #instansiate the vertices then add them to a list
    
    edgeStrList=graphType[3]
    
    for i in range(len(edgeStrList)):
        initialVertex=objVertexList[vertexStrList.index(edgeStrList[i][0])+1]
        #find start vertex
        finalVertex=objVertexList[vertexStrList.index(edgeStrList[i][1])+1]
        #find end vertex
        curEdge=edge(initialVertex,finalVertex,graphType[1],graphType[4][i])
        objEdgeList.append(curEdge)
        #instansiate the edges and add them to a list
    for i in range(1,len(objVertexList)):
        subList=[]
        
        for j in range(len(objEdgeList)):
            if objVertexList[i].name==edgeStrList[j][0]:
                subList.append(objEdgeList[j])
            
            elif objVertexList[i].name==edgeStrList[j][1]:
                subList.append(objEdgeList[j])
        
        edgeCon.append(subList)
    #all makes a 2d list of which vertices are connected to which other vertices
    
    BFSButton=button1("BFS",-4,3,"BFS",4,1)
    DFSButton=button1("DFS",-4,1.5,"DFS",4,1)
    AstarButton=button1("A*",-4,0,"aStar",4,1)
    dijkstraButton=button1("Dijkstra",-4,-1.5,"dijkstra",4,1)
    info=Text("the last vertex you click on will be the start vertex",position=(-6/8,-3/8),size=(10,10))
    global buttonList
    # means that clear screen has access and can remove these buttons
    buttonList=[BFSButton,DFSButton,AstarButton,dijkstraButton,info]

def BFS():
    """performs breadth first search"""
    clearScreen()
    startVertex=objVertexList[vertexStrList2.index(moveVertex[-1])]
    #makes start vertex the last vertex the user clicked on
    if startVertex==None:
        startVertex=objVertexList[1]
    startVertex.discovery=True
    discoveryOrder.append(startVertex)
    
    queue=[startVertex]

    while queue!=[]:
        currentVertex=queue[0]
        del queue[0]

        for i in range(len(currentVertex.connectvertexs)):
            #for every edge that current vertex has
            newVertex=currentVertex.connectvertexs[i]
            #find next vertex in system

            if newVertex.discovery==False:
                #if not already found
                curEdge=edgeFinder(currentVertex,newVertex)
                discoveryOrder.append(curEdge)
                discoveryOrder.append(newVertex)
                newVertex.prevvertex=currentVertex
                #helps the pathfinding function later on
                newVertex.discovery=True
                queue.append(newVertex)
    global chosenAlgorithm
    chosenAlgorithm="BFS"
    speedStepInput()

def DFS():
    clearScreen()
    startVertex=objVertexList[vertexStrList2.index(moveVertex[-1])]
    if startVertex==None:
        startVertex=objVertexList[1]
    #makes start vertex the last vertex that was clicked on
    runDFS(startVertex)
    # pass start vertex into run DFS, starting the iterative process
    global chosenAlgorithm
    chosenAlgorithm="DFS"
    speedStepInput()

def runDFS(currentVertex):
    """performs recursive depth first search"""
    currentVertex.discovery=True
    discoveryOrder.append(currentVertex)

    for i in range(len(currentVertex.connectvertexs)):
        #for every edge connected to current vertex
        newVertex=currentVertex.connectvertexs[i]
        #new vertex is a vertex connected to current vertex

        if newVertex.discovery==False:
            #if not already found new vertex
            curEdge=edgeFinder(currentVertex,newVertex)
            discoveryOrder.append(curEdge)
            newVertex.prevvertex=currentVertex
            #helps the pathfinding function later on
            runDFS(newVertex)#run this function again

def heuris(current,end):
    """performs the heuristic function for the a* algorithm"""
    xdif=current.present.x-end.present.x
    ydif=current.present.y-end.present.y
    return hypot(xdif,ydif)

def aStar():
    """runs the A* algorithm"""
    clearScreen()
    startVertex=objVertexList[vertexStrList2.index(moveVertex[-2])]
    if startVertex==None:
        startVertex=objVertexList[1]
    #start vertex is the penultimately clicked on edge

    try:
        endVertex=objVertexList[vertexStrList2.index(moveVertex[-1])]

    except IndexError:
        objVertexList[2]
    #end vertex is the last clicked on edge

    endPoint.append(endVertex)
    #needs to be global to be accessed by the speed step input function
    startVertex.distRootvertex=0
    startVertex.heurValue=heuris(startVertex,endVertex)
    startVertex.aStarValue=startVertex.distRootvertex+startVertex.heurValue
    openList=[startVertex]

    while openList!=[]:
        openList.sort(key=lambda x:x.aStarValue)
        curVertex=openList[0]
        #pick vertex with lowest aStar value from open list
        discoveryOrder.append(curVertex)
        if curVertex==endVertex:
            global chosenAlgorithm
            chosenAlgorithm="aStar"
            speedStepInput()
            break
            #algorithm has stopped, go to next function

        del openList[openList.index(curVertex)]
        #remove current vertex from open list

        for i in range(len(curVertex.connectvertexs)):
            #for every vertex connected to current vertex
            newVertex=curVertex.connectvertexs[i]
            curEdge=edgeFinder(curVertex,newVertex)
            nextCost=curVertex.distRootvertex+curEdge.weight
            if nextCost<newVertex.distRootvertex:
                #if new path is shorter
                discoveryOrder.append(curEdge)
                newVertex.prevvertex=curVertex
                newVertex.distRootvertex=nextCost
                newVertex.heurValue=heuris(newVertex,endVertex)
                newVertex.aStarValue=newVertex.distRootvertex+newVertex.heurValue

                if newVertex not in openList:
                    openList.append(newVertex)
        
def dijkstra():
    """performs dijkstra's algorithm on the graph"""
    clearScreen()
    startVertex=objVertexList[vertexStrList2.index(moveVertex[-1])]
    if startVertex==None:
        startVertex=objVertexList[1]

    #start vertex is the last vertex to be clicked on
    startVertex.distRootvertex=0
    vertexList2=objVertexList.copy()
    #need a copy as we are going to make alterations to the list
    del vertexList2[0]

    while vertexList2!=[]:
        vertexList2.sort(key=lambda x:x.distRootvertex)
        currentVertex=vertexList2[0]
        #finds vertex with shortest distance to root vertex
        discoveryOrder.append(currentVertex)
        del vertexList2[0]

        for i in range(len(currentVertex.connectvertexs)):
            newVertex=currentVertex.connectvertexs[i]
            edgeConnect=edgeFinder(currentVertex,newVertex)
            distance=currentVertex.distRootvertex+edgeConnect.weight
            #find distance from root vertex fore new vertex via currentVertex

            if distance<newVertex.distRootvertex:
                #if this new distance is shorter than the one we already have
                discoveryOrder.append(edgeConnect)                
                newVertex.distRootvertex=distance
                newVertex.prevvertex=currentVertex
    global chosenAlgorithm
    chosenAlgorithm="Dijkstra"
    speedStepInput()

def speedStepInput():
    """displays the graph traversal algorithms on the graphs"""

    speedButton=button1("speed control",-3,-3,"speed bar",4,1)
    stepButton=button1("step by step control",-3,3,"control bar",7,1)
    global buttonList
    # means that clear screen has access and can remove these buttons
    buttonList=[speedButton,stepButton]

def tableMake(timeLength,discoveredVertex):
    """creates tablethat shows the paths, and removes any superfluous highlighted lines"""
    startTitle=Text(text="Current Vertex",parent=scene,
    position=(-7,4,0),scale=(8,8,0))
    Pathtoroute=Text(text="Path To Root Vertex",parent=scene,
    position=(-5.5,4,0),scale=(8,8,0))
    weightTitle=Text(text="Weight Of Path",parent=scene,
    position=(-3.5,4,0),scale=(8,8,0))
    #all creates the column headings for the rest of the code to follow
    totalCurPath=[]
    #sum of all the edges and vertices in the completed treee

    for i in range(0,len(discoveredVertex),1):
        curPath=pathFinder(discoveredVertex[i])
        
        totalCurPath.append(curPath)
        weightList=0
        orderString=""
        #will have route from current vertex to start vertex in it by the end

        for j in range(len(curPath)):
            if isinstance(curPath[j],edge):
                #checking to see if its an edge
                if graphType[0]=="weighted":
                    weightList+=curPath[j].weight

                else:
                    weightList="N/A"
                    #there needs to be an option for the unweighted graphs

            elif isinstance(curPath[j],vertex):
                #checking to see if it is a vertex
                orderString+=curPath[j].name+", "
                #adds to path from root vertex to current vertex

        curWeight=Text(text=str(weightList),parent=scene,
        position=(-3.5,3.75-(i/4),0),scale=(8,8,0))

        curVertex=Text(text=str(discoveredVertex[i].name),parent=scene,
        position=(-7,3.75-(i/4),0),scale=(8,8,0))

        curRoute=Text(text=orderString,parent=scene,
        position=(-5.5,3.75-(i/4),0),scale=(8,8,0))

    totalCurPath2=sum(totalCurPath)#changes from a 1d list to a 2d list

    for i in range(len(discoveryOrder)):
        if discoveryOrder[i] not in totalCurPath2:
            seq1.append(1)
            #this ensures the program doesn't perform all the functions at once
            seq1.append(Func(discoveryOrder[i].present.fade_in, duration=timeLength))#change colour from blue to white

def mainSpeedStep():
    """function that highlights discovered vertices"""
    discoveredVertex=objVertexList[1:]
    timeLength=(int(buttonChecker())**2+1)/10
    #modification to time instruction to make it more useful
    clearScreen()

    if chosenAlgorithm=="aStar":
        discoveryOrder.append(endPoint[0])
        discoveredVertex=[endPoint[0]]
        #means that the aStar can display like the other algorithms do

    for i in range(len(discoveryOrder)):
        seq1.append(1)
        #stops all commands in sequence running at once
        seq1.append(Func(discoveryOrder[i].present.fade_out, duration=timeLength))
        #change colour of vertex from white to blue

    tableMake(timeLength,discoveredVertex)

    displayButton=Button(text="show algorithm",position=(-3,0,0),
    scale=(4,1,0),parent=scene)
    displayButton.on_click=seq1.start
    seq1.append(1)
    #stops all commands in sequence running at once
    seq1.append(Func(destroy, entity=displayButton))

def speedBar():
    """displays a list of buttons that the user can adjust
     to control the speed of the demonstration"""
    clearScreen()
    global buttonList
    #means clear screen can access these buttons
    buttonList=[]
    for i in range(10):
        button=button1(str(i+1),-6.5,(3.75-(3*i/4)),"mainSpeedStep",0.6,0.6)
        buttonList.append(button)

def controlBar():
    """allows the user to step through the program,
     going forwards and backwards"""
    clearScreen()
    global count
    if count==len(discoveryOrder):
        if chosenAlgorithm=="aStar":
            discoveredVertex=[endPoint[0]]
            #allows the aStar function to work like the other functions

        else:
            discoveredVertex=objVertexList[1:]
        tableMake(0.001,discoveredVertex)
        #passing in very short time for the edges/vertices to change colour
        return None
        #if the graph traversal algorithm has finished running

    forwardButton=button1("go forwards",-3,-3,"ford",5,1)
    backwardButton=button1("go backwards",-3,3,"back",5,1)
    global buttonList
    buttonList=[forwardButton,backwardButton]

def ford():
    """steps the graph traversal algorithm forwards one in the demonstration"""
    clearScreen()
    global count
    discoveryOrder[count].present.fade_out(duration=1)
    count+=1
    controlBar()

def back():
    """reverses the last thing the graph
    traversal algorithm did"""
    clearScreen()
    global count
    count+=-1
    discoveryOrder[count].present.fade_in(duration=1)
    controlBar()

def buttonChecker():
    """determines which buttons has been pressed, 
    and returns the information that button holds"""
    for i in range(len(buttonList)):
        if buttonList[i].pressed==True:
            return buttonList[i].text

def clearScreen():
    """removes all buttons and titles from the screen"""
    for i in range(len(buttonList)):
        curButton=buttonList[0]
        del buttonList[0]
        destroy(curButton)

    destroy(title) 

def edgeFinder(start,end):
    """finds the edges given two vertices"""

    for j in range(len(objEdgeList)):
    #for every single edge
        begin=objEdgeList[j].startVertex
        finish=objEdgeList[j].endVertex
        if begin==start and finish==end:
            #if this is the edge we want
            return objEdgeList[j]

        elif finish==start and begin==end and graphType[1]=="undirected":
            #if this is the reverse of the edge
            # we want and the graph is undirected
            return objEdgeList[j]

def pathFinder(start):
    displayList=[]
    while start.prevvertex!=None:
        #while there is still a path
        displayList.append(start)
        curEdge=edgeFinder(start.prevvertex,start)
        displayList.append(curEdge)
        start=start.prevvertex
        #set current vertex to the next vertex in the path

    displayList.append(start)
    return displayList

def posFinder(vertexNum):
    """finds the position for all the vertices"""
    posList=[]
    turnAngle=2*pi/vertexNum
    #finds angle to turn after every point has been found
    curAngle=0
    #starting at the positive real axis,

    for i in range (vertexNum):
        posList.append((3*cos(curAngle)+3,3*sin(curAngle)))
        #the y value is found by sine, the x value is found by cos
        #moved 3 to the right ot make space for the buttons
        curAngle+=turnAngle

    return posList

def moveEdge(edges):
    """function that moves the edges of the vertex that is being moved"""

    for i in range(len(edges)):
        #for all the vertices connected to the moving vertex
        x1=8*(edges[i].startVertex.present.x)
        y1=8*(edges[i].startVertex.present.y)
        x2=8*(edges[i].endVertex.present.x)
        y2=8*(edges[i].endVertex.present.y)
        #8 is the scalar required to adjust between the 2 coordinate systems
        try:
            grad=(y1-y2)/(x1-x2)

        except:
            grad=sys.maxsize
            #if no change in x, line deals with divide by 0 error
            #no change in x means vertical line

        xmid=(x1+x2)/2
        ymid=(y1+y2)/2
        edges[i].present.position=(xmid,ymid,0)
        edges[i].present2.position=(xmid,ymid,0)
        edges[i].present.rotation_z=-(atan(grad)*180/pi)
        edges[i].present2.rotation_z=-(atan(grad)*180/pi)
        #math function works in radians but rotation works in degrees
        pyth=sqrt((x1-x2)**2+(y1-y2)**2)
        edges[i].present.scale=(pyth,0.03,0)
        edges[i].present2.scale=(pyth,0.03,0)
        #set length to be the distance between the two vertices
        #make line thicker so its easier to see

        if graphType[0]=="weighted":
            curText=edges[i].weightDisplay
            curText.position=(xmid-edges[i].xadd,ymid+0.05,-0.01)
            #move solely the text of a weighted graph

            if graphType[1]=="undirected":
                edges[i].block.position=(xmid,ymid,0)
                #move the block surrounding the
                #  text on a weighted undirected graph

        if graphType[1]=="directed":
            rot1=atan(grad)
            rot2=(atan(grad)+2*pi/3)
            rot3=(atan(grad)+4*pi/3)
            #use to make the equilateral triangle
            destroy(edges[i].topArrow)
            #remove triangle

            if edges[i].startVertex.present.x<edges[i].endVertex.present.x:
                #if the start vertex is more to the left than the end vertex
                edges[i].topArrow=Entity(model=Mesh(
                vertices=((xmid+0.2*cos(rot1),ymid+0.2*sin(rot1),0),
                (xmid+0.2*cos(rot2),ymid+0.2*sin(rot2),0),
                (xmid+0.2*cos(rot3),ymid+0.2*sin(rot3),0))))
                #creates a triangle

            else:
                edges[i].topArrow=Entity(model=Mesh(
                vertices=((xmid-0.2*cos(rot1),ymid-0.2*sin(rot1),0),
                (xmid-0.2*cos(rot2),ymid-0.2*sin(rot2),0),
                (xmid-0.2*cos(rot3),ymid-0.2*sin(rot3),0))))

def update():
    """a bespoke function in ursina that automatically runs to see
     if anything is to be updated whilst the program is running,
     here it allows the vertices and edges to move"""
    location=vertexStrList2.index(moveVertex[-1])
    #last vertex clicked on is location
    currentVertex=objVertexList[location]
    #gets the object from the string
    
    if held_keys["w"]:
        currentVertex.present.y+=0.001
        currentVertex.present2.y+=0.001
        alterStr=edgeCon[location-1]
        #find list of all vertices connected to current vertex
        moveEdge(alterStr)

    if held_keys["s"]:
        currentVertex.present.y+=-0.001
        currentVertex.present2.y+=-0.001
        alterStr=edgeCon[location-1]
        moveEdge(alterStr)

    if held_keys["a"]:
        currentVertex.present.x+=-0.001
        currentVertex.present2.x+=-0.001
        alterStr=edgeCon[location-1]
        moveEdge(alterStr)

    if held_keys["d"]:
        currentVertex.present.x+=0.001
        currentVertex.present2.x+=0.001
        alterStr=edgeCon[location-1]
        moveEdge(alterStr)        

class vertexButton(Button):
    """This is a class that makes the vertices a button in ursina 
    that can be moved"""
    def __init__(self,text, xlocation,ylocation,zposition,colour):
        super().__init__(
            model="circle",
            scale=(0.1,0.1,0),
            color=colour,
            position=(xlocation/8,ylocation/8,zposition)
        )

        self.text=text

    def input(self,key):
        if self.hovered:
            if key=="left mouse down":
                moveVertex.append(self.text) #add to global list that this is the last vertex clicked on

class button1(Button):
    """creating the button class that,
     when a button is clicked, a function runs"""

    def __init__(self,input_text,xlocation,ylocation,nextStage,sizex,sizey):
        super().__init__(
           parent=scene,
           model="cube",
           color=color.Color(300,100,0.3,0.2),
           position=(xlocation,ylocation,0),
           scale=(sizex,sizey,0)              
        )

        self.text=input_text
        self.text_color=color.white
        self.text_origin=(0,0,-1)
        self.pressed=False
        self.nextStage=nextStage#name of next function to be run

    def input(self,key):
        #a bespoke method, that constantly looks 
        # to see if the buttons receive input
        if self.hovered:
            if key=="left mouse down":
                self.pressed=True
                funcDict[self.nextStage]()#a dictionary that turns srings into functions, then runs those functions

class edge():
    """creates an edge class"""

    def __init__(self,startVertex,endVertex,diCheck,weight):
        self.startVertex=startVertex
        self.endVertex=endVertex
        self.name=startVertex.name+endVertex.name
        #define the name of the edge as the start vertex
        #add the end vertex
        self.xmid=(self.startVertex.hori+self.endVertex.hori)/2
        self.ymid=(self.startVertex.vert+self.endVertex.vert)/2
        self.ychange=self.startVertex.vert-self.endVertex.vert
        self.xchange=self.startVertex.hori-self.endVertex.hori
        self.fadedOut=False
        
        try:
            self.gradient=self.ychange/self.xchange

        except ZeroDivisionError:
            self.gradient=sys.maxsize
            #if line is vertical set gradient to be as big as possible

        self.length=hypot(self.ychange,self.xchange)
        #find length using pythagoreas
        self.angle1=atan(self.gradient)
        self.angle2=atan(self.gradient)*180/pi
        #math function works in radians but rotation works in degrees
        self.startVertex.connectvertexs.append(endVertex)
        
        if diCheck=="undirected":
            self.endVertex.connectvertexs.append(startVertex)
            #in an undirected graph,
            #  you can also go from end vertex to start vertex
        
        if diCheck=="directed":
            rot1=self.angle1
            rot2=(self.angle1+2*pi/3)
            rot3=(self.angle1+4*pi/3)
            #rotation 0f 2 pi starting at the initial gradient
            if startVertex.hori<endVertex.hori:
                self.topArrow=Entity(model=Mesh(
                vertices=((self.xmid+0.2*cos(rot1),self.ymid+0.2*sin(rot1),0),
                (self.xmid+0.2*cos(rot2),self.ymid+0.2*sin(rot2),0),
                (self.xmid+0.2*cos(rot3),self.ymid+0.2*sin(rot3),0))))
                #if start vertex is more to the left of end vertex
            else:
                self.topArrow=Entity(model=Mesh(
                vertices=((self.xmid-0.2*cos(rot1),self.ymid-0.2*sin(rot1),0),
                (self.xmid-0.2*cos(rot2),self.ymid-0.2*sin(rot2),0),
                (self.xmid-0.2*cos(rot3),self.ymid-0.2*sin(rot3),0))))
                #create triangle using 3 coordinate points
        
        elif diCheck=="undirected" and weight!=0:
            #create a block for the text to be displayed against
            self.block=Entity(
                model="cube",
                parent=scene,
                scale=(0.2,0.2,0),
                color=color.white,
                position=(self.xmid,self.ymid,0)
            )
        
        self.present=Entity(model="quad",
        position=(self.xmid,self.ymid,-0.001),
        rotation_z=-self.angle2,
        scale=(self.length,0.03,0),
        color=color.white)
        self.weight=weight
        self.present2=Entity(model="quad",
        position=(self.xmid,self.ymid,0),
        rotation_z=-self.angle2,
        scale=(self.length,0.03,0),
        color=color.rgb(100,0,180))
        #create line as quadrilateral to alter width and height
        
        if self.weight!=0:
            if self.weight<10:
                xadd=0.05

            else:
                xadd=0.08
                #a 2 digit number needs to be put more to the right 

            self.xadd=xadd
            self.weightDisplay=Text(text=str(self.weight),
            parent=scene,
            scale=(6,6,0),
            color=color.black,
            position=(self.xmid-xadd,self.ymid+0.05,-0.01))

class vertex():
    """this creates the vertex class"""
    def __init__(self,name,coord):
        self.hori=coord[0]
        self.vert=coord[1]
        self.connectvertexs=[]
        self.discovery=False
        self.colour=color.black
        self.name=name
        self.distList=[]
        self.prevvertex=None
        self.heurValue=sys.maxsize
        self.distRootvertex=sys.maxsize
        self.aStarValue=self.distRootvertex+self.heurValue
        self.present=vertexButton(self.name,self.hori,self.vert,0.001,color.black)
        self.present.fit_to_text(radius=0.1)
        self.present2=vertexButton(self.name,self.hori,self.vert,0.002,color.rgb(100,0,180))
        self.present2.fit_to_text(radius=0.1)
        self.fadedOut=False #makes the circle object wrap around the the text

funcDict={"inputMakeGraph":inputMakeGraph,
"inputMakeGraph2":inputMakeGraph2,
"inputMakeGraph3":inputMakeGraph3,"inputUser":inputUser,
"makeGraph":makeGraph,"BFS":BFS,"DFS":DFS,"aStar":aStar,"dijkstra":dijkstra,
"control bar":controlBar,"speed bar":speedBar,"mainSpeedStep":mainSpeedStep,
"ford":ford,"back":back}
#dictionary changing all functions that buttons will call

window.color=color.blue
title=Text("Graph Traversal Demonstrator")
title.size=0.1
title.origin=(0,-4)
title.color=color.white
make_graph_button=button1("Make Graph",0,2,"inputMakeGraph",10,1)
buttonList=[make_graph_button]
app.run()
