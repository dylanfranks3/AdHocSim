import numpy as np
import os, csv,random, math, argparse


# cli interface
def parser():
    parser = argparse.ArgumentParser(description='SIMULATOR CLI TOOL')
    parser.add_argument('-d', '--directory', help='<Required> arg to pass the directory, see readme', required=True)
    parser.add_argument('-m','--model',help='arg that decides the model, pass: normal, NAN',required=False,default='direct')
    parser.add_argument('-v','--visualise',help='arg whether to create a visualising .mp3 in exec path',type=bool,required=False,default=False)
    parser.add_argument('-l','--logging',help='arg whether to show state of network post execution in stdout',type=bool,required=False,default=False)
    
    args = vars(parser.parse_args())
    
    dataDirectory = args['directory']
    model = args['model']
    visualise = args['visualise']
    logging = args['logging']

    buildSim(dataDirectory,model,visualise,logging)


def random_walk_2d(n, x,y): # creating a random walk of a node across a 2d plane
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





path = input("What is the path that you'd like to create the new dataset in?: ")
nodeCount = input("How many nodes would you like to create?: ")
xSize = input("What is the width of the simulation?: ")
ySize = input("What is the height of the simulation?: ")
runningTime = input("What is the running time of the simulation")

os.mkdir(path)





directory = os.fsencode(path)
t = True
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.isnumeric():
        newPath = path + f'/{filename}/{filename}.position.csv'
        if t == True: t = False
        else: t = True
        with open(newPath, mode='w', newline='') as file:
            #print (newPath)
            writer = csv.writer(file)
            time = 0.0
            random_walk = random_walk_2d(n, m, k)
            for position in random_walk:
                x, y = position
                writer.writerow([time, x, y, 0])
                time += 1
        






