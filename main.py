#!/usr/bin/env python
from src import *
import argparse, os, math, random
from manim import *
from manim.utils.file_ops import open_file as open_media_file 
from minimumBoundingBox import MinimumBoundingBox, rotate_points

SCALE = 0.95
class networkVisualiser(Scene):
    def __init__(self, simulation, **kwargs):
        super().__init__(**kwargs)

        self.simulation = simulation

        self.requests = self.simulation.historicRequests
        self.requests = sorted(self.requests.copy(),key=lambda x: x[0])

        self.nodes = self.simulation.network.nodeContainer
        self.timeScale = 20 # n times faster than the real sim

        # scale the nodes in x and y direction
        self.scaleNodesX = None
        self.scaleNodesY = None 
        self.angleRotate = None # this is the angle to rotate all the coords by
        self.centreOfRotation = None
        self.translate = None
        self.fixCoords() # find the bounding box etc.. append to attributes        
        
        

    
    def construct(self):
        
        self.plane()
        self.counter()
        self.wait(1)
        self.makeSimulation()

    
    def plane(self):
        rect2 = Rectangle(width=6, height=6)
        rect2.set_fill(color=GREEN,opacity=0.7)
        y_arrow = DoubleArrow(start=rect2.get_corner(DL) + LEFT * 0.3, end=rect2.get_corner(UL) + LEFT *0.3)
        x_arrow = DoubleArrow(start=rect2.get_corner(DL) + DOWN *0.3, end=rect2.get_corner(DR)+ DOWN *0.3)
        yArrowMid  = (y_arrow.get_start() + y_arrow.get_end()) / 2
        xArrowMid = (x_arrow.get_start() + x_arrow.get_end()) / 2
       
        yText = Text("300 meters", font_size=24).rotate(-PI/2).move_to(yArrowMid + LEFT * 0.30)
        xText = Text("300 meters", font_size=24).move_to(xArrowMid + DOWN * 0.25)

        self.add(rect2)
        self.wait(2)
        
        
        self.play(FadeIn(y_arrow,x_arrow,xText,yText),run_time= 1.5)
        self.wait(0.5)
        number_plane = NumberPlane(x_length=6,y_length=6,x_range=(-6, 6, 1),y_range=(-6, 6, 1),background_line_style={"stroke_color": TEAL})
        self.play(FadeIn(number_plane,scale=1),run_time=1.5)
        self.wait(0.5)
        

        
        plane = Group(rect2,y_arrow,x_arrow,yText,xText,number_plane)
        animation = plane.animate.shift(LEFT * 3)
        self.play(animation,run_time = 2.5)

    def fixNodeCoord(self, coord):
        coord = rotate_points(self.centreOfRotation,self.angleRotate,[coord])[0]
        coord = (coord[0]-self.translate[0],coord[1]-self.translate[1])
        coord =  (coord[0]*self.scaleNodesX,coord[1]*self.scaleNodesY)
        coord = np.array([coord[0],coord[1],0])
        return coord + 3*LEFT # move to where the plane is 
        
    
    def findCorners(self,points): # given the vertices of a rectangle label them tr,tl,br,bl
        tl = max(sorted(points,key=lambda x: x[0]),key=lambda x: x[1])

        points.remove(tl)
        oCorners = points
        def distance(num):
            x1,y1 = tl
            x2,y2 = num
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        oCorners = sorted(oCorners, key=distance)
        if abs(oCorners[0][1] -tl[1]) < abs(oCorners[1][1] - tl[1]):
            tr,br,bl = oCorners[0],oCorners[2],oCorners[1]
        
        else:
            tr,br,bl = oCorners[1],oCorners[2],oCorners[0]
       
       
        return (tl,tr,br,bl)


        

    def fixCoords(self):
        allHistory = []
        for i in self.nodes:
            for hL in i.historicLocation:
                if hL != None:
                  allHistory.append((hL.location[0],hL.location[1]))

        coords = allHistory
        boundingBox = MinimumBoundingBox(coords)
        corners = [i for i in boundingBox.corner_points] # getting the smallest box around all these points
        corners = self.findCorners(corners)
        tl,tr,br,bl = corners
        self.centreOfRotation = ((tl[0] + tr[0])/2,(tl[1] + br[1])/2)
        xDist = tr[0] - tl[0]
        yDist = tr[1] - tl[1]
        angle = math.atan(yDist/xDist) #+ 0.5*math.pi #find the angle that the top left point of the rectangle has and the top right and rotate all these points accordingly
        self.angleRotate = angle 
        
        cornersOld = (tl,tr,br,bl)
        corners = rotate_points(self.centreOfRotation,self.angleRotate,cornersOld)
        corners = self.findCorners(corners)
        
        tl,tr,br,bl = corners



        


        

        newXDist = tr[0]-tl[0]
        newYDist = tr[1]-br[1]
        centreOfRect = ((tl[0] + tr[0])/2,(tl[1] + br[1])/2)
        #newPointsMoved = [(i[0]-centreOfRect[0],i[1]-centreOfRect[1]) for i in newPointsRotated]
        self.translate = centreOfRect 

        scalex = 6/newXDist
        scaley = 6/newXDist
        self.scaleNodesX = scalex * SCALE
        self.scaleNodesY = scaley * SCALE
        

    def getDot(self,arr,gUid): # from an array of Dots, find the Dot with given loc
        for i in arr:
            if i.uid == gUid:
                return i

    def makeSimulation(self):
        print (self.requests[-1])
        # making the dots representing the nodes, TODO, colour code master, etc
        createdDots = []
        for request in self.requests:
            if request[1].__func__ == node.Node.updateLocation:
                    movedNode = request[1].__self__
                    if movedNode.uid not in [i.uid for i in createdDots]:
                        loc = request[1].__self__.getLocation() 
                        print (loc)
                        return
                        virtualNode = node.Node(movedNode.uid)
                        virtualNode.updateLocation(loc)
                        
                        
                        virtualNode.visualDot = Dot(self.fixNodeCoord(virtualNode.getLocation())).scale(1.5)
                        print (virtualNode.getLocation(),virtualNode.uid)
                        createdDots.append(virtualNode)


        





        finishedTime = self.requests[-1][0]
        #print (finishedTime, 'IS the finish time')
        # iterate through each interval of the sim
        intervalInVisualisation = (self.timeScale/finishedTime)*self.simulation.interval # how long each interval is in the visualisation
        #print (intervalInVisualisation)
        for i in range(0,math.ceil(finishedTime/self.simulation.interval) + 1):
            intervalAnims = []
            dotsAnims = []
            packetsAnims = []
            while len(self.requests) > 0 and float(self.requests[0][0]) <= float(i):
                cRequest = self.requests[0]
                
                if cRequest[1].__func__ == node.Node.updateLocation:
                    movedNode = cRequest[1].__self__
                    newLoc = self.fixNodeCoord(cRequest[2].location) # TODO work out why this is a thing
                    originalDot = self.getDot(createdDots,movedNode.uid)                  
                    
                    newDot = Dot(newLoc).scale(1.5) # keep the color
                    animation = ReplacementTransform(originalDot.visualDot,newDot)
                    originalDot.visualDot = newDot
                    dotsAnims.append(animation)


                # packets moving
                if cRequest[1].__func__ == network.Network.sendPacketDirectCall:
                    fromNodeLocation = self.fixNodeCoord(cRequest[2].getLocation())
                    toNodeLocation = self.fixNodeCoord(cRequest[3].getLocation())
                    


                    packetVis = Dot(fromNodeLocation).scale(0.5)
                    #dotsAnims.append(FadeIn(packetVis))
                    packetsAnims.append(packetVis.animate.move_to(toNodeLocation))
                    packetsAnims.append(Wait(intervalInVisualisation))
                    #packetsAnims.append(FadeOut(packetVis))
            
                self.requests.pop(0)

            if len(dotsAnims) > 0:
                anim_group = AnimationGroup(*dotsAnims,run_time=intervalInVisualisation)
                packetsAnimGroup  = AnimationGroup(*packetsAnims,run_time=intervalInVisualisation*20)
                self.play(anim_group,packetsAnimGroup)
                print (len(intervalAnims), i)

            if i == 50:
                return
            
            
            

            




    def counter(self):
        number = DecimalNumber().set_color(WHITE).scale(3)
        self.add(number.move_to(RIGHT*3))   
        self.wait(2)
        # Play the Count Animation to count from 0 to 100 in 4 seconds
        self.play(Count(number, 0, 100), run_time=3)
        self.wait(1)
        number.generate_target()
        self.play(
            number.animate.move_to(3.2*UP + 5.9* RIGHT).scale(0.4),
            run_time=2
        )
        time = Text("Time: ").scale(3*0.35).next_to(number,LEFT).shift(0.05 *UP)
        self.add(time)

        
        newTime = DecimalNumber(number=0).set_color(WHITE).scale(3).shift(3.2*UP + 5.9* RIGHT).scale(0.4)
        self.play(Transform(number,newTime))
        
    
        




        






    # this works out how much we need to s
    def specs(self):
        xCoords = []
        yCoords = []
        issues = 0
        for node in self.nodes:
            hL = node.historicLocation
            for i in hL:
                try:
                    xCoords.append(i.location.location[0])
                    yCoords.append(i.location.location[1])
                except:
                    issues += 1

        minX = min(xCoords)
        maxX = max(xCoords)
        maxY = max(yCoords)
        minY = min(yCoords)
        return minX,minY,maxX,maxY
        
        



class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(number,  **kwargs)
        # Set start and end
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        # Set value of DecimalNumber according to alpha
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)






















# cli interface
def parser():
    parser = argparse.ArgumentParser(description='SIMULATOR CLI TOOL')
    parser.add_argument('-d', '--directory', help='<Required> arg to pass the directory, see readme', required=True)
    parser.add_argument('-m','--model',help='arg that decides the model, pass: normal, NAN',required=False,default='direct')
    parser.add_argument('-v','--visualise',help='arg whether to create a visualising .mp3 in exec path',type=bool,required=False,default=False)
    parser.add_argument('-l','--logging',help='arg whether to show state of network post execution in stdout',type=bool,required=False,default=False)
    
    args = vars(parser.parse_args())
    
    dataDirectory = args['directory']
    model = args['model']
    visualise = args['visualise']
    logging = args['logging']

    buildSim(dataDirectory,model,visualise,logging)


def buildSim(dataDirectory,model,visualise,logging):
    if model == 'direct':
        n = network.Network()
        s = simulator.Simulator(network=n,length=800,time=0.0,output=True,interval=0.25,display=visualise) # for the dartmouth dataset

    else:  
        ### TODO when not direct model
        ...

    getNodes(s,n,dataDirectory)
    s.run()
    if logging == True:
        print (s.showState())

        
    #print ("Unexecuted requests: " + str(len(s.requests)))

    scene = networkVisualiser(s)
    scene.render()
    
    
    


# plaintext directory, gets nodes and packets and adds them to sim/net
def getNodes(sim,net,directory):
    # creating nodes and adding to sim/network
    failedAdds = 0 # how many nodes have packets to send to non-existent nodes
    ptDirectory = directory
    directory = os.fsencode(directory)
    nodeArr = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        
        if filename.isnumeric(): # removing chance for DS_store etc
            # nodes
            # open position file, add the requests to 
            positionFilePath = f'{ptDirectory}/{filename}/{filename}.position.csv'
            nodeUID = int(filename)
            newNode = node.Node(nodeUID)
            nodeArr.append(newNode)
    net.nodeContainer = nodeArr
    
    # taking existing nodes and adding packets and location movement
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.isnumeric(): # removing chance for DS_store etc
            # nodes
            # open position file, add the requests to 
            positionFilePath = f'{ptDirectory}/{filename}/{filename}.position.csv'
            nodeUID = filename
            newNode = sim.findNode(int(nodeUID))
            with open(positionFilePath,'r') as f:
                lines = f.read().splitlines()
                for line in lines:
                    line = line.split(',')
                    sim.request(int(float(line[0])),newNode.updateLocation,location.Location([float(line[1]),float(line[2]),float(line[3])]))


    #print (len(sim.requests))
    # taking existing nodes and adding packets and location movement
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.isnumeric(): # removing chance for DS_store etc      
            # packets
            # open node packet data
            newNode = sim.findNode(int(filename))
            dataFilePath = f'{ptDirectory}/{filename}/{filename}.data.csv'            
            with open(dataFilePath,'r') as f:
                lines = f.read().splitlines()
                for line in lines:
                    line = line.split(',')
                    dest = int(line[3].split('.')[-1]) #destination node
                    destNode = sim.findNode(dest)
                    if destNode == False: # if we can't find the destination node in the sim
                        #print (f"ERROR: tried to add a packet where the destination ({dest}) doesn't exist")
                        failedAdds +=1
                    else:
                        p = packet.Packet(int(float(line[0])),newNode,destNode)
                        sim.request(0,newNode.addPacket,p)
                        sim.request(int(float(line[1])),net.sendPacketDirect,newNode,destNode,p)
    
    
    
parser()














