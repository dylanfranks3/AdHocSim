from AdHocSim.network import Network
from AdHocSim.nanNode import *
from AdHocSim import packet, location



class NANNetwork(Network):
    def __init__(self):
        super().__init__()
        self.clusters = None # to be setup()
        self.randomFactor = random.uniform(0,1)
        self.communicatingDistance = 50 # the radius of communication
    
    
    def setup(self):
        # give each node a random ranking 
        for i in self.nodeContainer:
            i.randomFactor = random.uniform(0,1)
            i.masterRank = i.randomFactor*i.masterRank

        # initially put them into clusters
        self.makeClusters()

    def clusterUpdate(self,gC):
        # if we're at the end of the simulation, store the type
        if self.simulator.time == self.simulator.length:
            print ("time")
            for node in gC:
                node.historicType[-1][1] = self.simulator.length - node.historicType[-1][1]
            return 
        

        aM = max(gC,key= lambda x: x.masterPreference) # get the item that's most willing to be master
        if aM.type!=NANNodeType.AM:
            aM.updateType(NANNodeType.AM,self.simulator.time,self.simulator.interval)
        
        for node in gC:
            # add the constant power of always listening 
            node.powerUsed += node.constantPower

            # the cost of sending frames every interval of sim
            discoveryFrame = ((8*31)/250000)*38*(len(gC)-1)*self.simulator.interval
            syncFrame = ((8*31)/250000)*38*(len(gC)-1)*self.simulator.interval
            if node.type == NANNodeType.AM or node.type == NANNodeType.M:
                node.addPower(syncFrame+discoveryFrame)
            elif node.type == NANNodeType.NMS:
                node.addPower(syncFrame)
            
                

        
            # changing the node types
            closestNodes = [i for i in gC if ((location.Location.distance(i.location,node.location) <= self.communicatingDistance) and i != node)] # get the nodes that are 'nearby'
            large = [i.masterRank for i in closestNodes] # the masterRank of all nodes near the current
            if len(large) > 0:
                large = max([i.masterRank for i in closestNodes]) # highest master rank in current cluster
                if node.type == NANNodeType.M:
                    if large >= node.masterRank:
                        node.updateType(NANNodeType.NMS,self.simulator.time,self.simulator.interval)
                elif node.type == NANNodeType.NMS:
                    if large <= node.masterRank:
                        node.updateType(NANNodeType.M,self.simulator.time,self.simulator.interval)
                    elif large >= node.masterRank:
                        node.updateType(NANNodeType.NMNS,self.simulator.time,self.simulator.interval)
                elif node.type == NANNodeType.NMNS:
                    if large <= node.masterRank:
                        node.updateType(NANNodeType.M,self.simulator.time,self.simulator.interval)
                    elif large >= node.masterRank:
                        node.updateType(NANNodeType.NMS,self.simulator.time,self.simulator.interval)
                    
    



        




    def updater(self):
        def powerUsedAsADec(n):
            if n.totalPower-n.powerUsed == 0:
                print ("used all the power - there's a problem")
            else:
                return (n.totalPower-n.powerUsed)/n.totalPower
        # work on the roles
        for node in self.nodeContainer:
            node.masterRank = node.masterPreference*random.uniform(0,1)*powerUsedAsADec(node)

        self.makeClusters()
        for cluster in self.clusters:
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


    # make clusters based on whether nodes are <= communicating distance, hence the scc
    def makeClusters(self):
        edges = {i:[j for j in self.nodeContainer if j!=i and location.Location.distance(i.location,j.location)<self.communicatingDistance] for i in self.nodeContainer}
        vertices = [i for i in self.nodeContainer]
        scc = self.strongly_connected_components_iterative(vertices,edges)
        self.clusters = [list(cluster) for cluster in scc]


    # referenced: https://github.com/alviano/python/blob/master/rewrite_aggregates/scc.py
    @staticmethod
    def strongly_connected_components_iterative(vertices, edges):
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






        

