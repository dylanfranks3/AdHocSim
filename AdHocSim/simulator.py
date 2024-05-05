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
        self.output = output  # verbose output 
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
        firstPass = False
        secondPass = False
        print (len(self.requests))
        while not (firstPass and secondPass):  # to make sure all current requests get processed
            change = False
            for index, request in enumerate(self.requests):
                if float(request[0]) == float(self.time):  # if the current time is equal to the request start time
                    change = True
                    request[1](*request[2:])
                    self.requests.pop(index)
                    self.historicRequests.append(request)
           
            if change:
                firstPass,secondPass = False,False
            if not change and not firstPass:
                firstPass = True
            if not change and firstPass:
                secondPass = True

    def incrementTime(self):
        self.time = round(self.time+ self.interval,2)
        #print ("Node has this: ",self.network.nodeContainer[0].data)

        
    def readablePacket(
        self, packet: packet.Packet
    ):  # readable packet in context of the sim
        return [packet.size, packet.src.uid, packet.dest.uid]

    def run(self):  # call this to run the sim
        while self.time <= self.length:
            print (self.time)
            print ("managing requests")
            self.network.updater()
            self.manageRequests()  # process requests that are currently scheduled
            
            self.incrementTime()  # increase the time by self.interval
        

    def findNode(self, guid: int):  # find a node given a uid
        for gNode in self.network.nodeContainer:
            if gNode.uid == guid:
                return gNode
        return False

    
    def showState(self):
        # future feature
        return
        