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
        self.historicType:list[NANNodeType] = [NANNodeType.M]
        self.randomFactor = None
        self.masterPreference:float = random.uniform(0,1)
        self.masterRank:float = random.uniform(0,1)
        self.powerUsed:float = random.uniform(0,10000) # give it a random amount of power used
        

    def addPower(self,usage:float):
        self.powerUsed += usage

    def updateType(self,newType):
        self.historicType.append(newType)
        self.type = newType
        


