This directory is part of a larger set of work for my Warwick Third Year Project (Dissertation). Here I model, create data and simulate Ad-Hoc networks. 

### Dataset 
/dataset contains related datasets based off a [MANET dataset of outdoor experments for comparing differnet routing algorithms](https://ieee-dataport.org/open-access/crawdad-dartmouthoutdoor). /dataset/outdoor-run-20031017 contains the cleaned data which has been processed by:
1. Removed nodes with no gps data
2. Moving the trace data from ARPL.data.parsed to a csv with columns: SRC, DEST, TIME, SIZE. 

For the program to run successfully, network trace (dataset) must also include data of this form for each node.
TODO explain more

### Running the program
TODO


### Network model

- Simulator(class)
    - do ur things

- Network(class)
    - Attributes:
        - node container -> list of node(class)
        - time (wrt. start time of sim) -> float 
        - length of sim -> float
        - output(whether to show std.out) -> bool 
        - interval (how long each time interval is) -> float
    - Modules:
        - nextInterval()
            - check if time + interval > length of sim
            - time += interval
            - iterate nodes
        - statisitcal ones

- NANNetwork(class, parent network):
    - Attributes (append as above):
    - Modules:
        - tell nodes to do things with their roles (pass the NANNetwork instance to the function so it can acess data about the nodes)
        - More analytical (calcRolePercentage)
        


- Node(class)
    - Attributes:
        - location (x,y,z) -> class
        - trace -> path to dataset
            - use [this](https://arc.net/l/quote/tiraorhu)
        - index (current in dataset) -> integer
        - data recieved, data sent -> dictionary/json

    - Modules:
        - updateLocation
            - change index as well

- NANNode(class, parent Node):
    - Attributes:
        - masterPreference -> float

        - 
    - Modules:
        - Related NAN modules TODO


- Location(class)
    - Attributes:
        - pos = [x,y,z]
    - Modules:
        - updateLocation(newLocation)
        - static: distane(pos1,pos2)



### What i want the 'direct' program to do:
1. Create nodes
2. create network
3. create sim
4. add location movements of nodes to requests
5. add packets at time 0 to source of nodes
6. add requests of packet sending 

