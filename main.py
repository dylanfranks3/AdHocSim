#!/usr/bin/env python
from src import *
import argparse



def parser():
    parser = argparse.ArgumentParser(description='SIMULATOR CLI TOOL')
    parser.add_argument('-d', '--directory', help='<Required> arg to pass the directory, see readme', required=True)
    parser.add_argument('-m','--model',help='<Required> arg that decides the model, pass: normal, NAN',required=True)
    parser.add_argument('-v','--visualise',help='<Required> arg whether to create a visualising .mp3 in exec path',type=bool,required=True)
    args = vars(parser.parse_args())
    print (args)

parser()
quit()

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













