import random
class Network():
    def __init__(self):
        self.nodeContainer = None
        self.simulator = None # this is set within simulator
        

    def calculateLatency(self,node1=None,node2=None):
        #TODO
        return 0
        return random.choice([i/4 for i in range(0,17)])
    

    def createNewUID(self): #probably not necessary rn
        return max(i.uid for i in self.nodeContainer) + 1


    #sending packets directly between nodes
    def sendPacketDirect(self,src,dest,packet):
        src.removePacket(packet)
        latency = self.calculateLatency() 
        self.simulator.request(latency,dest.addPacket,packet) # add the packet to the recipetent
        self.simulator.request(latency,self.sendPacketDirectCall,src,dest) # tell the sim, here is the nodes and use this to build vis


    def sendPacketDirectCall(self,src,dest):
        pass



    


    def addNode(self,node,uid):
        self.nodeContainer.append(node)







