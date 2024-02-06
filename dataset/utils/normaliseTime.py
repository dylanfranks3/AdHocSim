import os, shutil
import pandas as pd

path = "/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData"
directory = os.fsencode(path)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.isnumeric(): #.isnumeric():
        dataP = path + f'/{filename}/{filename}.data.csv'
        positionP = path + f'/{filename}/{filename}.position.csv'
        data = pd.read_csv(dataP, delimiter=",",header=None)
        position = pd.read_csv(positionP, delimiter=",",header=None)
        data[1] -= 1066401492
        position[0] -= 1066401492
        data.to_csv(dataP,header=False,index=False)
        position.to_csv(positionP,header=False,index=False)

