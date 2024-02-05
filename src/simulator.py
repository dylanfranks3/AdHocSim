class Simulator:
    def __init__(self,network, length, time, output, interval):
        self.network = network # network class
        self.length = length # length of sim
        self.output = output # verbose output TODO
        self.interval = interval # how large the increment is in the simulation
        self.requests = [] # calls an instance of this class has to make, i.e. add a packet to a node
        self.time = time
        self.network.simulatorRequests = self.requests

    def request(self, delay, command, *awgs):
        self.requests.append([self.time+delay,command,*awgs])

    def manageRequests(self):
        for index,request in enumerate(self.requests):
            if request[0] <= self.time: # if the current time is later or equal the request start time
                request[1](request[2])
                del self.requests[index]
            
    def incrementTime(self):
        self.time += self.interval

    def readablePacket(self,packet):
        return [packet.size,self.network.nodeContainer.index(packet.src),self.network.nodeContainer.index(packet.dest)]

    def run(self):
        while self.time <= self.length:
            self.manageRequests()
            self.incrementTime()
            self.showState()
        

    def showState(self):

        print (
f"""HIGH-LEVEL NETWORK:
No. of nodes: {len(self.network.nodeContainer)}
Time in simulation: {self.time}
Length of simulation: {self.length}
Interval in simulation: {self.interval}
Requests in simulation: {self.requests}

---------------------------------------

NODES:""")
        for index,node in enumerate(self.network.nodeContainer):
            print (f'NODE{index}:')
            print ("SRC   | DEST  | SIZE")
            for packet in node.socketWaiting:                
                print (f'NODE{self.network.nodeContainer.index(packet.src)} | NODE{self.network.nodeContainer.index(packet.dest)} | {packet.size}')
            print ("")

            # TODO add more functionality showing packet logging 
            #for k,v in node.data.items():
            #    print (f'{k} : {" ".join([" "self.readablePacket(i) for i in v])}')
            

        print ("---------------------------------------")

    