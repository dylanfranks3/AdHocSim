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

        for i in self.nodeContainer:
            print (i.socketWaiting)

    def updater(self):
        # work on the roles
        # set master preference based on 'relative' power usage
        #for n in self.nodeContainer:
        pass

    


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

        
    def makeInitialClusters(self):
        totalDistance = 0
        distancesCalced = 0
        clusters = []
        for n1 in self.nodeContainer:
            for n2 in self.nodeContainer:
                if n1 != n2:
                    dist = location.Location.distance(n1.location,n2.location)
                    totalDistance+=dist; distancesCalced+=1
        
        meanD = totalDistance/distancesCalced
        added = []
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





        





    

