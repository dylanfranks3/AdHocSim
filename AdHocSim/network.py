import random
from .packet import Packet
from .node import Node
from .location import Location
from .simulator import Simulator
class Network():
    def __init__(self):
        self.nodeContainer: list[Node] = None
        self.simulator: Simulator  = None # this is set within simulator
        

    def calculateLatency(self,node1:Node=None,node2:Node=None):
        #TODO
        return 0
        return random.choice([i/4 for i in range(0,17)])
    

    def createNewUID(self): #probably not necessary rn
        return max(i.uid for i in self.nodeContainer) + 1


    #sending packets directly between nodes
    def sendPacketDirect(self,src:Node,dest:Node,packet:Packet):
        src.removePacket(packet)
        latency = self.calculateLatency() 
        self.simulator.request(latency,dest.addPacket,packet) # add the packet to the recipetent
        self.simulator.request(latency,self.sendPacketDirectCall,src,dest,src.getLocation(),dest.getLocation()) # tell the sim, here is the nodes and use this to build vis


    def sendPacketDirectCall(self,src:Node,dest:Node,srcLoc:Location,destLoc:Location):
        pass



    


    def addNode(self,node,uid):
        self.nodeContainer.append(node)







