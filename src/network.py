class Network():
    def __init__(self,nodeContainer):
        self.nodeContainer = nodeContainer
        self.simulatorRequests = None # this is set within simulator
        
        

    # TODO modules
    def calculateLatency(self,node1=None,node2=None):
        #TODO
        return 3
    
    def createNewUID(self):
        return max(i.uid for i in self.nodeContainer) + 1
            
    
    #sending packets directly between nodes
    def sendPacketDirect(self,src,dest,packet):
        src.removePacket(packet)
        latency = self.calculateLatency() 
        
        self.simulatorRequests.append([latency,dest.addPacket,packet])

    def addNode(self,node):
        node.uid = self.createNewUID()
        self.nodeContainer.append(node)
        






