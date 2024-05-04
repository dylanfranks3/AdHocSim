from pandas import DataFrame
from datetime import datetime
import time
import os
from AdHocSim.nanNode import NANNodeType
import matplotlib.pyplot as plt
import numpy as np


def analytics(path,s):

    print ("\n"*5)
    noNodes = str(len(s.network.nodeContainer))
    pathToAnalytics = path+'/'+str(int(time.time()))+f'({str(noNodes)} Nodes)'
    os.mkdir(pathToAnalytics)

    n = s.network # get the network
     
    totalTimeInType(pathToAnalytics,s)
    calculateFairness(pathToAnalytics,s)
    calculateThroughput(pathToAnalytics,s)
    calculatePower(pathToAnalytics,s)

# creates a dict of all the nodes and their time in each role
def totalTimeInType(path,s):
    nodeContainer = s.network.nodeContainer
    noNodes = str(len(nodeContainer))
    d = {node.uid:[0,0,0,0] for node in nodeContainer}
    for node in nodeContainer:
        historicT = node.historicType
        for typeData in historicT:
            d[node.uid][typeData[0].value - 1] += typeData[1]

    allNodeTypes = d
    df = DataFrame.from_dict(allNodeTypes, orient='index',columns=["Master", "Anchor Master", "Non-Master Sync", "Non-Master Non-Sync"])
    df.to_csv(path+f'/timeInRoles.csv')


def calculateThroughput(path,s):
    interval = s.interval
    # dict of {interval1:{node1:[],node2:[]...},interval2}
    dataOut = {interval*i:{j.uid:0 for j in s.network.nodeContainer} for i in range(0,int((s.length+1)/interval))}
    nC = s.network.nodeContainer
    for node in nC:
        for d in node.data["SOUT"]:
            dataOut[d[1]][node.uid] += d[0].size
    
    givenT = 0
    # entire sim throughput
    for intervalTime in dataOut:
        count = 0 
        for n in dataOut[intervalTime]:
            count += 1
            givenT += dataOut[intervalTime][n]
    entireThroughput = (givenT/(count))/s.length

    # first half sim throughput
    givenT = 0
    for intervalTime in list(dataOut.keys())[:int(len(dataOut)/2)]:
        count = 0 
        for n in dataOut[intervalTime]:
            count += 1
            givenT += dataOut[intervalTime][n]
    firstHalfThroughput = (givenT/(count))/(s.length/2)

    # second half sim throughput
    givenT = 0
    for intervalTime in list(dataOut.keys())[int(len(dataOut)/2):]:
        count = 0 
        for n in dataOut[intervalTime]:
            count += 1
            givenT += dataOut[intervalTime][n]
    secondHalfThroughput = (givenT/(count))/(s.length/2)

    # get the throughput every 50 seconds
    throughput = {i:0 for i in range(50,int(s.length)+1,50)} 
    for i in range(50,int(s.length)+1,50):
        currentI = dataOut[i]
        throughputI = 0
        count = 0 
        for nT in currentI:
            count += 1
            throughputI += dataOut[i][nT]
        throughput[i] = (throughputI/count)/interval
            
    # add the 1st half and second half data 
    throughput.update({'1stHalf':firstHalfThroughput,'2ndHalf':secondHalfThroughput,'entireSim':entireThroughput})
    throughputDF = DataFrame(throughput, index=[0])
    noNodes = str(len(s.network.nodeContainer))
    throughputDF.index = [f'{noNodes}']
    throughputDF.to_csv(path+f'/throughput.csv') 

    
def calculatePower(path,s):
    noNodes = str(len(s.network.nodeContainer))

    power = {i.uid:{"Constant Role Power Usage":0,
             "Role Change Power Usage": 0,
             "Transmission Power Usage": 0} for i in  s.network.nodeContainer}
    
    for node in s.network.nodeContainer:
        power[node.uid]["Constant Role Power Usage"] = node.roleCost
        power[node.uid]["Role Change Power Usage"] = node.stateChangeCost
        power[node.uid]["Transmission Power Usage"] = node.transmissionCost


    pd = DataFrame.from_dict(power,orient='index')
    pd.to_csv(path+f'/power.csv')



def calculateFairness(path,s):
    interval = s.interval
    # dict of {interval1:{node1:[],node2:[]...},interval2}
    dataOut = {interval*i:{j.uid:0 for j in s.network.nodeContainer} for i in range(0,int((s.length+1)/interval))}
    nC = s.network.nodeContainer
    for node in nC:
        for p in node.data["SOUT"]:
            dataOut[p[1]][node.uid] += p[0].size


    # entire sim fairness
    nodeThroughput = [0 for i in range(len(nC))]
    for intervalTime in dataOut:
        for n in nC:
            
            nodeThroughput[n.uid-1] += dataOut[intervalTime][n.uid]
    
    numer = sum(nodeThroughput)**2
    denom = sum([i**2 for i in nodeThroughput])*len(nC)
    entireFairness = numer/denom
    

    # first half sim fairness
    nodeThroughput = [0 for i in range(len(nC))]
    for intervalTime in list(dataOut.keys())[:int(len(dataOut)/2)]:
        for n in nC:
            nodeThroughput[n.uid-1] += dataOut[intervalTime][n.uid]
    numer = sum(nodeThroughput)**2
    denom = sum([i**2 for i in nodeThroughput])*len(nC)
    firstHalfFairness = numer/denom


    # second half sim fairness
    nodeThroughput = [0 for i in range(len(nC))]
    for intervalTime in list(dataOut.keys())[int(len(dataOut)/2):]:
        for n in nC:
            nodeThroughput[n.uid-1] += dataOut[intervalTime][n.uid]
    numer = sum(nodeThroughput)**2
    denom = sum([i**2 for i in nodeThroughput])*len(nC)
    secondHalfFairness = numer/denom


    # get the fairness every 50 seconds
    fairness = {i:[0 for i in range(len(nC))] for i in range(50,int(s.length)+1,50)} 
    for i in range(50,int(s.length)+1,50):
        for n in nC:
            fairness[i][n.uid-1] += dataOut[i][n.uid]

    print (fairness)
    finalfairness = {}
    for k in fairness:
        numer = sum(fairness[k])**2
        denom = sum([i**2 for i in fairness[k]])*len(nC)
        finalfairness[k] = numer/denom

    
    # add the 1st half and second half data 
    finalfairness.update({'1stHalf':firstHalfFairness,'2ndHalf':secondHalfFairness,'entireSim':entireFairness})
    fairnessDF = DataFrame(finalfairness, index=[0])
    noNodes = str(len(s.network.nodeContainer))
    fairnessDF.index = [f'{noNodes}']
    fairnessDF.to_csv(path+f'/fairness.csv') 
    



def ccdf(nodes):
    nodes = {key: [x / sum(nodes[1]) for x in value] for key, value in nodes.items()}

    state_data = {i: [] for i in range(4)}
    for percentages in nodes.values():
        for idx, p in enumerate(percentages):
            state_data[idx].append(p)

    # Calculating CCDF for each state
    ccdf_data = {}
    for state, values in state_data.items():
        sorted_values = np.sort(values)
        ccdf = 1 - np.arange(len(sorted_values)) / len(sorted_values)
        ccdf_data[state] = (sorted_values, ccdf)


    role_names = ["Master", "Anchor Master", "Non-Master Sync", "Non-Master Non-Sync"]

    # Plotting the data
    plt.figure(figsize=(10, 6))
    for state, (values, ccdf) in ccdf_data.items():
        plt.step(values, ccdf, label=f'{role_names[state]}')

    plt.xlabel('Device Percentage Time in Role (as decimal)')
    plt.ylabel('Probability (as decimal) Time in Role > x')
    plt.title('CCDF of Node Roles in Network Simulation')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()


        








