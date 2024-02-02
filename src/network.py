class Network():
    def __init__(self,nodeContainer):
        self.nodeContainer = nodeContainer
        self.simulatorRequests = None # this is set within simulator
        
        

    # TODO modules
    def calculateLatency(self,node1=None,node2=None):
        #TODO
        return 3
    
    #sending packets directly between nodes
    def sendPacketDirect(self,src,dest,packet):
        src.removePacket(packet)
        latency = self.calculateLatency() 
        
        self.simulatorRequests.append([latency,dest.addPacket,packet])




