#!/usr/bin/env python
from src import *
import argparse, os, math
from manim import *
from manim.utils.file_ops import open_file as open_media_file 
from minimumBoundingBox import MinimumBoundingBox, rotate_points

class networkVisualiser(Scene):
    def __init__(self, simulation, **kwargs):
        self.simulation = simulation
        self.requests = self.simulation.historicRequests
        self.requests.sort(key=lambda x: x[0])
        self.nodes = self.simulation.network.nodeContainer
        self.timeScale = 30 # n times faster than the real sim
        super().__init__(**kwargs)
        

    
    def construct(self):
        self.makeSimulation()
        quit()
        self.plane()
        self.counter()
        self.wait(1)

    
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
        self.wait(2)

    def fixCoords(self):
        dots = []
        boundingBox = MinimumBoundingBox([(i.location.location.location[0],i.location.location.location[1]) for i in self.nodes])
        tl,tr,br,bl = (i for i in boundingBox.corner_points) # getting the smallest box around all these points
        
        xDist = tr[0] - tl[0]
        yDist = tr[1] - tl[1]
        angle = -math.atan(yDist/xDist) #find the angle that the top left point of the rectangle has and the top right and rotate all these points accordingly
        
        newPointsRotated = rotate_points(tl,angle,[(i.location.location.location[0],i.location.location.location[1]) for i in self.nodes])
        tl,tr,br,bl = rotate_points(tl,angle,(tl,tr,br,bl))

        newXDist = 
        

    def makeSimulation(self):
        # lets define how big the space is 6x6 realistacally for simplicity
        self.fixCoords()

        

        quit()

        finishedTime = self.requests[-1][0]
        # iterate through each interval of the sim
        intervalInVisualisation = self.timeScale*self.simulation.interval/finishedTime # how long each interval is in the visualisation
        for i in range(0,math.ceil(finishedTime/self.simulation.interval) + 1):
            while self.requests[0][0] <= i:
                cRequest = self.requests[0]
                #if cRequest[1].__func__ == node.Node.


            self.wait(intervalInVisualisation)


            


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
        s = simulator.Simulator(network=n,length=773,time=0.0,output=True,interval=0.25,display=visualise) # for the dartmouth dataset

    else:  
        ### TODO when not direct model
        ...

    getNodes(s,n,dataDirectory)
    s.run()
    if logging == True:
        print (s.showState())

        
    print ("Unexecuted requests: " + str(len(s.requests)))

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














