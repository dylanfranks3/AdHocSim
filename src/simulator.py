import argparse,time
class Simulator:
    def __init__(self,network, length, time, output, interval):
        self.network = network
        self.length = length # length of sim
        self.output = output # verbose output TODO
        self.interval = interval # how large the increment is in the simulation
        self.requests = [] # calls an instance of this class has to make, i.e. add a packet to a node
        self.time = time # typically start at 0
        self.setup()


    def setup(self): # passing the sim to the net so that it can add requests
        self.network.simulator = self

    def request(self, delay, command, *awgs):
        self.requests.append([self.time+delay,command,*awgs])

    def manageRequests(self):
        while (float(self.time) in [float(i[0]) for i in self.requests]):
            for index,request in enumerate(self.requests):
                if float(request[0]) == float(self.time): # if the current time is equal to the request start time
                    request[1](*request[2:])
                    self.requests.pop(index)

        
       
    
                
            
    def incrementTime(self):
        self.time += self.interval

    def readablePacket(self,packet): # readable packet in context of the sim
        return [packet.size,packet.src.uid,packet.dest.uid]

    def run(self): # call this to run the sim
        while self.time <= self.length:
            self.manageRequests()
            self.incrementTime()
        
        
    def findNode(self,guid): # find a node given a uid
        for gNode in self.network.nodeContainer:
            if gNode.uid == guid: return gNode 
        return False


    def showState(self):

        print( 
f"""HIGH-LEVEL NETWORK:
No. of nodes: {len(self.network.nodeContainer)}
Time in simulation: {self.time}
Length of simulation: {self.length}
Interval in simulation: {self.interval}
Requests in simulation: {len(self.requests)}

---------------------------------------

NODES:""")
    
        for index,node in enumerate(self.network.nodeContainer):
            print (f'NODE {node.uid}:')
            for k,v in node.data.items():
                print (f'{k}: {len(v)}')
            print("")
            print ("SRC   | DEST  | SIZE")
            for packet in node.socketWaiting:                
                print (f'NODE{packet.src.uid} | NODE{packet.dest.uid} | {packet.size}')
            print ("")

            # TODO add more functionality showing packet logging 
            #for k,v in node.data.items():
            #    print (f'{k} : {" ".join([" "self.readablePacket(i) for i in v])}')
            

    print ("---------------------------------------")

