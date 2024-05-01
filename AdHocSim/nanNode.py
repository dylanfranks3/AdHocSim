from AdHocSim.node import Node
from enum import Enum
import random


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
        self.state:str = 'sleep' # if we're in a 'sleep'/'listen'/'transmit' state, start as 'sleep'
        self.historicType:list[NANNodeType] = [[NANNodeType.M,0]]
        self.randomFactor = None 
        self.masterPreference:float = random.uniform(0,1)
        self.masterRank:float = random.uniform(0,1)
        self.constantPower:float = 0 # the constant power that gets added each n seconds
        self.totalPower = 2000 * 60 * 60 # the entire power a device has
        self.powerUsed:float = random.uniform(0,self.totalPower/500)

    # this defines the constant power usage depending on state
    def addConstantPower(self,amount:float):
        self.constantPower = amount






    def updateType(self,newType,t,interval): #
        if self.type != newType:
            self.addPower(0.02 * 8.1) # the cost to change state
        # the cost of being in a specific state
        if newType == NANNodeType.NMNS:
            self.addConstantPower(0.6*interval)
        if newType in [NANNodeType.NMS,NANNodeType.M,NANNodeType.AM]:
            self.addConstantPower(40*interval)  # cost of recieving
        
        self.historicType[-1] = [self.historicType[-1][0],t-self.historicType[-1][1]]
        self.historicType.append([newType,t])
        self.type = newType




    def addPower(self,usage:float):
        self.powerUsed += usage


    


