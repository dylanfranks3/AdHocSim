import os, shutil
import pandas as pd

path = "/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData"
directory = os.fsencode(path)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.isnumeric():
        shutil.move(f'/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData/{filename}/position.log.parsed.csv',f'/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData/{filename}/{filename}.position.csv')