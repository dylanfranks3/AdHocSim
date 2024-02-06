#!/usr/bin/env python
from src import *
import argparse, os


#global s
#global n
# cli interface
def parser():
    parser = argparse.ArgumentParser(description='SIMULATOR CLI TOOL')
    parser.add_argument('-d', '--directory', help='<Required> arg to pass the directory, see readme', required=True)
    parser.add_argument('-m','--model',help='<Required> arg that decides the model, pass: normal, NAN',required=True)
    parser.add_argument('-v','--visualise',help='<Required> arg whether to create a visualising .mp3 in exec path',type=bool,required=True)
    args = vars(parser.parse_args())
    
    dataDirectory = args['directory']
    model = args['model']
    visualise = args['visualise']

    buildSim(dataDirectory,model,visualise)


def buildSim(dataDirectory,model,visualise):
    if model == 'direct':
        n = network.Network()
        s = simulator.Simulator(network=n,length=773,time=0.0,output=True,interval=0.25) # for the dartmouth dataset

    else:  
        ### TODO when not direct model
        pass
    getNodes(s,n,dataDirectory)
   
    
    s.run()

    #for i in  (s.requests):
   #     print (i)
    print (len(s.requests))
    print (s.showState())
    #print ("Unexecuted requests: " + str(len(s.requests)))
    
    
    


# plaintext directory, gets nodes and packets and adds them to sim/net
def getNodes(sim,net,directory):
    # creating nodes and adding to sim/network
    failedAdds = 0 # how many nodes have packets to send to non-existent nodes
    ptDirectory = directory
    directory = os.fsencode(directory)
    nodeArr = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        
        if filename.isnumeric(): # removing chance for DS_store etc
            # nodes
            # open position file, add the requests to 
            positionFilePath = f'{ptDirectory}/{filename}/{filename}.position.csv'
            nodeUID = int(filename)
            newNode = node.Node(nodeUID)
            nodeArr.append(newNode)
    net.nodeContainer = nodeArr
    
    # taking existing nodes and adding packets and location movement
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.isnumeric(): # removing chance for DS_store etc
            # nodes
            # open position file, add the requests to 
            positionFilePath = f'{ptDirectory}/{filename}/{filename}.position.csv'
            nodeUID = filename
            newNode = sim.findNode(int(nodeUID))
            with open(positionFilePath,'r') as f:
                lines = f.read().splitlines()
                for line in lines:
                    line = line.split(',')
                    sim.request(int(float(line[0])),newNode.updateLocation,location.Location([float(line[1]),float(line[2]),float(line[3])]))


    #print (len(sim.requests))
    # taking existing nodes and adding packets and location movement
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.isnumeric(): # removing chance for DS_store etc      
            # packets
            # open node packet data
            newNode = sim.findNode(int(filename))
            dataFilePath = f'{ptDirectory}/{filename}/{filename}.data.csv'            
            with open(dataFilePath,'r') as f:
                lines = f.read().splitlines()
                for line in lines:
                    line = line.split(',')
                    dest = int(line[3].split('.')[-1]) #destination node
                    destNode = sim.findNode(dest)
                    if destNode == False: # if we can't find the destination node in the sim
                        #print (f"ERROR: tried to add a packet where the destination ({dest}) doesn't exist")
                        failedAdds +=1
                    else:
                        p = packet.Packet(int(float(line[0])),newNode,destNode)
                        sim.request(0,newNode.addPacket,p)
                        sim.request(int(float(line[1])),net.sendPacketDirect,newNode,destNode,p)

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













