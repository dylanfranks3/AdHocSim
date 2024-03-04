#!/usr/bin/env python
import numpy as np
import os, csv,random, math

class Dataset:
    @staticmethod
    def createRandomIntegers(size, mean, value_range):
        """
        Creates an array of random integers with a specified mean
        
        Parameters:
        - size: the size of the array
        - mean: the desired mean of the array
        - value_range: a tuple indicating the range (min, max) of the values

        """
        min_val, max_val = value_range
        random_integers = np.random.randint(min_val, max_val + 1, size=size)
        

        adjustment_factor = mean - np.mean(random_integers)
        random_integers = np.round(random_integers + adjustment_factor).astype(int)
        
        random_integers[random_integers < min_val] = min_val
        random_integers[random_integers > max_val] = max_val
        
        return random_integers

    
    # creating a random walk of a node across a 2d plane
    @staticmethod
    def random_walk_2d(n, x,y): 
        # Initialize an array to store the random walk positions
        current_position = [np.random.randint(x), np.random.randint(y)]
        allAngles = []
        k = 4
        angle = np.random.uniform(0,2*np.pi)

        walk = []
        change = [False,0]

        for _ in range(n):
            changeOfAngle = np.random.uniform(-k/10,k/10)
            angle += changeOfAngle

            
            if len(allAngles) > 0:
                angle = (angle + 1.2*(sum(allAngles)/len(allAngles)))/2.1
            allAngles.append(angle)

            
            directionV = (np.cos(angle)*0.8,np.sin(angle)*0.8)
        
            current_position = (current_position[0] + directionV[0],current_position[1] + directionV[1])
            current_position = (max(0, min(current_position[0], x-1)),max(0, min(current_position[1], y - 1)))


            # how to deal with a node near the perimeter

            if current_position[0] >= x - x/random.randint(50,1000) or current_position[0] <= x/random.randint(50,1000) and change[0] == False:
                allAngles = [math.pi/random.randint(20,30) + math.pi - i  for  i in allAngles]
                change[0] = True

            if current_position[1] >= y - y/random.randint(50,1000) or current_position[1] <= y/random.randint(50,1000) and change[0] == False:
                allAngles = [math.pi/random.randint(20,30) - i  for  i in allAngles]
                change[0] = True

            if change[0] == True:
                change[1] += 1
            if change[0] == True and change[1] > 50:
                change[0] = False
                change[1] = 0
                
                                
            walk.append(current_position)
        
        return walk



    # makes dirs for each node
    @staticmethod
    def createNodeDirectories(gPath,gNodeCount):
        for i in range(1,gNodeCount+1):
            os.mkdir(f'{gPath}/{i}/')


    @staticmethod
    def createPacketData(gPath,gTime,gThroughput,gNodeCount,gPacket):
        nodeNos = [i for i in range(1,gNodeCount+1)]
        
        for i in nodeNos:

            # how many unique nodes a single node will communicate to across the sim
            match gThroughput:
                case 'low':
                    uniqueComs = math.ceil(gNodeCount/10)
                    uniqueNodesPerSec = random.uniform(0.4,0.2)
                case 'med':
                    uniqueComs = math.ceil(gNodeCount/8)
                    uniqueNodesPerSec = random.normalvariate(0.7,0.25)
                case 'high':
                    uniqueComs = math.ceil(gNodeCount/5)
                    uniqueNodesPerSec = random.normalvariate(1.6,0.3)

            nodeNosSansCurrent = nodeNos.copy()
            nodeNosSansCurrent.remove(i) # you can't send packets to yourself, duh
            choiceOfNodes = random.sample(nodeNosSansCurrent,k=uniqueComs)
            amountToChoose = Dataset.createRandomIntegers(gTime+1,uniqueNodesPerSec,(math.floor(0.8*uniqueNodesPerSec),math.ceil(1.2*uniqueNodesPerSec)))
            with open(f'{gPath}/{i}/{i}.data.csv', mode='w+', newline='') as file:
                writer = csv.writer(file)
                for time in range(0,gTime):
                    messagesToSend = []
                    # given we want to talk to so many unique people per second, let's get some subset of nodes to communicate to that has a mean of this
                    
                    thisSecondsRecipetents = random.sample(choiceOfNodes,amountToChoose[time])

                    for recipitent in thisSecondsRecipetents:
                        # how many packets a given frame will be
                        match gPacket:
                            case 'low':
                                packetSize = round(random.normalvariate(2.5,1))
                            case 'med':
                                packetSize = round(random.uniform(3.2,1))
                            case 'high':
                                packetSize = round(random.uniform(4.3,1.1))

                        for _ in range(packetSize):
                            nothing = False
                            messagesToSend.append(['1300',str(time), str(f'11.0.0.{str(i)}'),f'11.0.0.{str(recipitent)}'])


                    random.shuffle(messagesToSend)
                    if messagesToSend:
                        writer.writerows(messagesToSend)


    # this takes the newly made dataset, goes through each numeric dir (node) and creates a position.csv with time and size and params
    @staticmethod
    def createLocationData(gPath,gTime,gX,gY,gNodeCount,gInterval):
        for i in range(1,gNodeCount+1):
            newPath = gPath + f'/{i}/{i}.position.csv'
            with open(newPath, mode='w+', newline='') as file:
                #print (newPath)
                writer = csv.writer(file)
                time = 0.0
                random_walk = Dataset.random_walk_2d(round(gTime-1/gInterval), gX, gY)
                for position in random_walk:
                    x, y = position
                    writer.writerow([time, x, y, 0]) # no 3D consideration
                    time += gInterval
            


def setup(gPath,gNodeCount,gInterval,gXSize,gYSize,gTime,gPacketSize,gThrougput):
    if not os.path.isdir(gPath): # if the directory the user wants to use doesn't exist, make it
        os.mkdir(gPath)

    Dataset.createNodeDirectories(gPath,gNodeCount)
    Dataset.createLocationData(gPath,gTime,gXSize,gYSize,gNodeCount,gInterval)
    Dataset.createPacketData(gPath,gTime,gThrougput,gNodeCount,gPacketSize)




