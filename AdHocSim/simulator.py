import argparse, time
from manim import *
from manim.utils.file_ops import open_file as open_media_file

from AdHocSim import packet
from AdHocSim import nanNetwork
from AdHocSim.node import Node
from AdHocSim.nanNode import *

import matplotlib.pyplot as plt
import numpy as np

# from AdHocSim import packet,nanNetwork,network


class Simulator:
    def __init__(
        self,
        network,  #: network.Network|nanNetwork.NANNetwork,
        length: float,
        time: float,
        output: bool,
        interval: float,
    ):
        self.network = network
        self.length = length  # length of sim
        self.output = output  # verbose output TODO
        self.interval = interval  # how large the increment is in the simulation
        self.requests = (
            []
        )  # calls an instance of this class has to make, i.e. add a packet to a node
        self.time = time  # typically start at 0
        self.setup()
        self.historicRequests = []

    def setup(self):  # passing the sim to the net so that it can add requests
        self.network.simulator = self

    def request(self, delay: float, command, *awgs):
        self.requests.append([self.time + delay, command, *awgs])

    def manageRequests(self):
        while float(self.time) in [
            float(i[0]) for i in self.requests
        ]:  # to make sure all current requests get processed
            for index, request in enumerate(self.requests):
                if float(request[0]) == float(
                    self.time
                ):  # if the current time is equal to the request start time
                    request[1](*request[2:])
                    self.requests.pop(index)
                    self.historicRequests.append(request)

    def incrementTime(self):
        self.time += self.interval

    def readablePacket(
        self, packet: packet.Packet
    ):  # readable packet in context of the sim
        return [packet.size, packet.src.uid, packet.dest.uid]

    def run(self):  # call this to run the sim
        while self.time <= self.length:
            print (self.time)
            self.manageRequests()  # process requests that are currently scheduled
            self.network.updater()
            self.incrementTime()  # increase the time by self.interval
        if self.output:
            self.showState()

    def findNode(self, guid: int):  # find a node given a uid
        for gNode in self.network.nodeContainer:
            if gNode.uid == guid:
                return gNode
        return False

    
    # TODO maybe overload the print function
    def showState(self):
        

        


        
        
        return
        for index, node in enumerate(self.network.nodeContainer):
            print(f"NODE {node.uid}:")
            for k, v in node.data.items():
                print(f"{k}: {len(v)}")
            print (node.historicType)
            print (node.powerUsed)
            print (node.masterPreference)
            print ("")
            print ("")
            print ("")
            print ("")
            
            
            
            #print("")
            #print("SRC   | DEST  | SIZE")
            #for packet in node.socketWaiting:
            #    print(f"NODE{packet.src.uid} | NODE{packet.dest.uid} | {packet.size}")
            #print("")

            # TODO add more functionality showing packet logging
            # for k,v in node.data.items():
            #    print (f'{k} : {" ".join([" "self.readablePacket(i) for i in v])}')
            
        #print("---------------------------------------")
        