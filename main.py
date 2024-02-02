#!/usr/bin/env python
from src import *


n1 = node.Node([1,2,3],"",1)
n2 = node.Node([1,2,4],"",1)

p1 = packet.Packet(5,n1,n2)
p2 = packet.Packet(10,n2,n1)

myNetwork = network.Network([n1,n2])

n1.addPacket(p1)
n2.addPacket(p2)

s = simulator.Simulator(myNetwork,10,0,True,0.1)

s.network.sendPacketDirect(n1,n2,p1)

s.run()













