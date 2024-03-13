from AdHocSim.network import Network
from AdHocSim.nanNode import *
from AdHocSim import packet, location



class NANNetwork(Network):
    def __init__(self):
        super().__init__()
        self.clusters = None # to be setup()
        self.randomFactor = random.uniform(0,1)
        
    
    def setup(self):
        # give each node a random ranking 
        for i in self.nodeContainer:
            i.randomFactor = self.randomFactor
            i.masterRank = i.randomFactor*i.masterRank

        # initially put them into clusters
        self.makeInitialClusters()

    def clusterUpdate(self,gC):
        aM = max(gC,key= lambda x: x.masterPreference) # get the item that's most willing to be master
        aM.updateType(NANNodeType.AM)

        reasonableDist = 2*self.calcMeanDist(gC)/len(gC)

        for node in gC:
            closestNodes = [i for i in gC if ((location.Location.distance(i.location,node.location) <= reasonableDist) and i !=node)]
            closestNodesTypes = [i.type for i in closestNodes]
            if node.type == NANNodeType.M:
                if max([i.masterRank for i in closestNodes]) >= node.masterRank:
                    node.updateType(NANNodeType.NMS)
            elif node.type == NANNodeType.NMS:
                if max([i.masterRank for i in closestNodes]) <= node.masterRank:
                    node.updateType(NANNodeType.M)
                elif max([i.masterRank for i in closestNodes]) >= node.masterRank:
                    node.updateType(NANNodeType.NMNS)
            elif node.type == NANNodeType.NMNS:
                if max([i.masterRank for i in closestNodes]) <= node.masterRank:
                    node.updateType(NANNodeType.M)
                elif max([i.masterRank for i in closestNodes]) >= node.masterRank:
                    node.updateType(NANNodeType.NMS)
                
                


        




    def updater(self):
        # work on the roles
        
        for node in self.nodeContainer:
            node.masterRank = self.masterPreference*self.randomFactor

        for cluster in self.clusters:
            self.clusterUpdate(cluster)

        
        





        
        

    


    #overriding
    # sending packets directly between nodes
    def sendPacketDirect(self, src: NANNode, dest: NANNode, packet: packet.Packet):
        src.removePacket(packet)
        latency = self.calculateLatency()
        self.simulator.request(
            latency, dest.addPacket, packet
        )  # add the packet to the recipetent
        self.simulator.request(
            latency,
            self.sendPacketDirectCall,
            src,
            dest,
            src.getLocation(),
            dest.getLocation(),
        )  # tell the sim, here is the nodes and use this to build vis

        # TODO work out how much power it actually uses
        amount = packet.size / 10
        src.addPower(amount)

    def calcMeanDist(self,arr):
        totalDistance = 0
        distancesCalced = 0
        
        for n1 in arr:
            for n2 in arr:
                if n1 != n2:
                    dist = location.Location.distance(n1.location,n2.location)
                    totalDistance+=dist; distancesCalced+=1
        
        meanD = totalDistance/distancesCalced
        return meanD

        
    def makeInitialClusters(self):
        meanD = self.calcMeanDist(self.nodeContainer)
        added = []
        clusters = []
        # go through the nodecontainer and create clusters of nodes where the distance <= mean distance
        for n in self.nodeContainer:
            if n not in added:
                added.append(n)
                currentCluster = [n]
                for remaining in [r for r in self.nodeContainer if r not in added]:
                    if location.Location.distance(n.location,remaining.location) <= meanD/3:
                        currentCluster.append(remaining)
                        added.append(remaining)
                clusters.append(currentCluster)

        if len(added) != len(self.nodeContainer):
            print ("inital cluster adding wrong!!!")

        self.clusters = clusters

        print (clusters)





        





    

