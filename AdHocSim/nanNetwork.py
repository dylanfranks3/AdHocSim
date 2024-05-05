from AdHocSim.network import Network
from AdHocSim.nanNode import *
from AdHocSim import packet, location
import numpy as np


class NANNetwork(Network):
    def __init__(self):
        super().__init__()
        self.clusters = None # to be setup()
        self.randomFactor = 0.8
        self.communicatingDistance = 30  # the radius of communication
    
    
    def setup(self):
        # give each node a random ranking 
        for i in self.nodeContainer:
            i.randomFactor = 0.8
            i.masterRank = i.randomFactor*i.masterRank
        # initially put them into clusters
        self.makeClusters()


    def clusterUpdate(self,gC):
        # if we're at the end of the simulation, store the type
        if self.simulator.time == self.simulator.length:
            for node in gC:
                node.historicType[-1][1] = self.simulator.length - node.historicType[-1][1]
            return 
        
        # if it's by itself in the cluster, very sad...
        if len(gC) == 1:
            gC[0].updateType(NANNodeType.NMNS,self.simulator.time,self.simulator.interval)
            return 
        

        aM = max(gC,key= lambda x: x.masterPreference) # get the item that's most willing to be master
        if aM.type!=NANNodeType.AM:
            aM.updateType(NANNodeType.AM,self.simulator.time,self.simulator.interval)
            #aM.addPower(10000)
            
        for node in gC:
            self.routePacket(node,gC) # send all the packets around

            if node.type == NANNodeType.AM and node != aM: # if this isn't the only anchor
                node.type = NANNodeType.NMNS
            # add the constant power of always listening 
            
            # the cost of sending frames every interval of sim
            discoveryFrame = ((8*31)/250000)*38*(len(gC)-1)*self.simulator.interval
            syncFrame = ((8*31)/250000)*38*(len(gC)-1)*self.simulator.interval
            if node.type == NANNodeType.AM or node.type == NANNodeType.M:
                node.addPower(syncFrame+discoveryFrame)
                node.roleCost += syncFrame+discoveryFrame
            elif node.type == NANNodeType.NMS:
                node.addPower(syncFrame)
                node.roleCost += syncFrame
            
            # changing the node types
            closestNodes = [i for i in gC if ((location.Location.distance(i.location,node.location) <= self.communicatingDistance*10) and i != node)] # get the nodes that are 'nearby'
            #print (len(closestNodes),len(gC))
            large = [i.masterRank for i in closestNodes] # the masterRank of all nodes near the current
            masterRankHigher = any([i>node.masterRank for i in large]) # check if any master rank is higher than the current
            if len(large) > 0:
                if node.type == NANNodeType.M:
                    if masterRankHigher:
                        node.updateType(NANNodeType.NMS,self.simulator.time,self.simulator.interval)                        
                elif node.type == NANNodeType.NMS:
                    if masterRankHigher:
                        node.updateType(NANNodeType.NMNS,self.simulator.time,self.simulator.interval)
                    else:
                        node.updateType(NANNodeType.M,self.simulator.time,self.simulator.interval) 
                """ elif node.type == NANNodeType.NMNS:
                    if masterRankHigher:
                        node.updateType(NANNodeType.NMS,self.simulator.time,self.simulator.interval)
                    else:
                        node.updateType(NANNodeType.M,self.simulator.time,self.simulator.interval)  """
        
        


    def updater(self):
        # work on the roles
        for node in self.nodeContainer:
            node.time += self.simulator.interval # here we give it a time
           
            node.powerUsed += node.constantPower
            node.roleCost += node.constantPower
            
            #node.masterRank = node.masterPreference*(node.unusedPower()*0.8)
            node.masterRank *= node.masterPreference*(node.unusedPower())

        #print ("making clusters")
        self.makeClusters()
        for cluster in self.clusters:
            #print ("cluster update")
            self.clusterUpdate(cluster)
            



    #overriding parent method
    # sending packets directly between nodes
    def sendPacketDirect(self, src: NANNode, dest: NANNode, packet: packet.Packet):
        src.removePacket(packet)
        latency = self.calculateLatency(packet)
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

        amount = ((8*31 + packet.size)/250000)*38 # the energy cost of transmitting the packet
        src.addPower(amount)
        src.transmissionCost += amount


    # make clusters based on whether nodes are <= communicating distance, hence the scc
    def makeClusters(self):
        edges = {i:[j for j in self.nodeContainer if j!=i and location.Location.distance(i.location,j.location)<self.communicatingDistance] for i in self.nodeContainer}
        vertices = [i for i in self.nodeContainer]
        scc = self.strongly_connected_components_iterative(vertices,edges)
        self.clusters = [list(cluster) for cluster in scc]
        #print ([len(i) for i in self.clusters])


    # call this every interval to send the packets waiting to be sent in socket waiting
    def routePacket(self,node:Node,cluster:list[Node]):
        communicateNodes = [i for i in cluster if location.Location.distance(node.location,i.location) < self.communicatingDistance and i!=node]
        for i in node.socketWaiting:
            if i.dest in communicateNodes:
                self.sendPacketDirect(node,i.dest,i)
            else:
                minDistance = location.Location.distance(node.location,i.dest.location)
                minNode = node
                for nodeInCluster in communicateNodes:
                    nodeInClusterLoc = nodeInCluster.location
                    nodeLoc = node.location
                    if location.Location.distance(nodeLoc,nodeInClusterLoc) < minDistance:
                        minNode = nodeInCluster
                if minNode != node:
                    self.sendPacketDirect(node,minNode,i)


    # referenced: https://github.com/alviano/python/blob/master/rewrite_aggregates/scc.py
    @staticmethod
    def strongly_connected_components_iterative(vertices:Node, edges):
        identified = set()
        stack = []
        index = {}
        boundaries = []

        for v in vertices:
            if v not in index:
                to_do = [('VISIT', v)]
                while to_do:
                    operation_type, v = to_do.pop()
                    if operation_type == 'VISIT':
                        index[v] = len(stack)
                        stack.append(v)
                        boundaries.append(index[v])
                        to_do.append(('POSTVISIT', v))
                        # We reverse to keep the search order identical to that of
                        # the recursive code;  the reversal is not necessary for
                        # correctness, and can be omitted.
                        to_do.extend(
                            reversed([('VISITEDGE', w) for w in edges[v]]))
                    elif operation_type == 'VISITEDGE':
                        if v not in index:
                            to_do.append(('VISIT', v))
                        elif v not in identified:
                            while index[v] < boundaries[-1]:
                                boundaries.pop()
                    else:
                        # operation_type == 'POSTVISIT'
                        if boundaries[-1] == index[v]:
                            boundaries.pop()
                            scc = set(stack[index[v]:])
                            del stack[index[v]:]
                            identified.update(scc)
                            yield scc
