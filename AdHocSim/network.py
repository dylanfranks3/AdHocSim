import random
from AdHocSim import node, simulator, location, packet


class Network:
    def __init__(self):
        self.nodeContainer: list[node.Node] = None
        self.simulator: simulator.Simulator = None  # this is set within simulator

    def calculateLatency(self, gPacket:packet.Packet):
        return round(gPacket.size/250000*4)/4 # round to the nearest 0.25

    def createNewUID(self):  # probably not necessary rn
        return max(i.uid for i in self.nodeContainer) + 1

    # sending packets directly between nodes
    def sendPacketDirect(self, src: node.Node, dest: node.Node, packet: packet.Packet):
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

    def sendPacketDirectCall(
        self,
        src: node.Node,
        dest: node.Node,
        srcLoc: location.Location,
        destLoc: location.Location,
    ):
        pass

    def addNode(self, node, uid):
        self.nodeContainer.append(node)

    def updater(self):
        pass
