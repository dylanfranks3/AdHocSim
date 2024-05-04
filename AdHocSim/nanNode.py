from AdHocSim.node import Node
from enum import Enum
import random
import numpy as np

# each node has a choice of the following roles:
# AM,M,NMS,NMNS, allocated by random m
class NANNodeType(Enum):
    M = 1
    AM = 2
    NMS = 3
    NMNS = 4


class NANNode(Node):
    def __init__(self,*awgs):
        super().__init__(*awgs)
        self.type:NANNodeType = NANNodeType.M # starts as master
        self.historicType:list[NANNodeType] = [[NANNodeType.M,0]]
        self.randomFactor = None 
        self.masterPreference:float = 0.8
        self.masterRank:float = 0.8
        self.totalPower = 2000 * 60 * 60 # the entire power a device has
        self.powerUsed:float = random.uniform(0,self.totalPower/1000) # start with a random usage amount (natural battery usage)
        self.constantPower = 0
        self.roleCost = 0
        self.stateChangeCost = 0
        self.transmissionCost = 0
        
    # this defines the constant power usage depending on state
    def addConstantPower(self,amount:float):
        self.constantPower = amount


    def updateType(self,newType,t,interval): #
        if self.type != newType:
            self.addPower(0.02 * 8.1) # the cost to change state
            self.stateChangeCost += 0.02 * 8.1
        # the cost of being in a specific state
        if newType == NANNodeType.NMNS:
            self.addConstantPower(0.6*interval)
        if newType in [NANNodeType.NMS,NANNodeType.M]:
            self.addConstantPower(40*interval)  # cost of recieving
        if newType == NANNodeType.AM: # anchor
            self.addConstantPower(80*interval) 
        
        
        self.historicType[-1] = [self.historicType[-1][0],t-self.historicType[-1][1]]
        self.historicType.append([newType,t])
        self.type = newType




    def addPower(self,usage:float):
        self.powerUsed += usage

    def unusedPower(self):
        if self.totalPower-self.powerUsed == 0:
            print ("used all the power - there's a problem")
        else:
            return (self.totalPower-self.powerUsed)/self.totalPower



