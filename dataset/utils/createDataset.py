import numpy as np
import os, csv,random, math


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

        #print (changeOfAngle)
        
        if len(allAngles) > 0:
            angle = (angle + 1.2*(sum(allAngles)/len(allAngles)))/2.1
        allAngles.append(angle)

        
        directionV = (np.cos(angle)*0.8,np.sin(angle)*0.8)
        #print (directionV,angle)
    
        current_position = (current_position[0] + directionV[0],current_position[1] + directionV[1])
        current_position = (max(0, min(current_position[0], x-1)),max(0, min(current_position[1], y - 1)))



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
    
        
    

    #print (walk[0],walk[-1])
    #quit()
    
    return walk

# Example usage

n = 800  # Number of steps in the random walk
m = 1000   # Number of rows in the grid
k = 1000   # Number of columns in the grid


path = "/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData"
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
        






