import os, shutil
import pandas as pd

path = "/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData"
directory = os.fsencode(path)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename == '1':
        packets = path +f'/{filename}/10.0.0.{filename}.APRL.data.parsed.csv'
        data = pd.read_csv(packets, delimiter=",",header=None,usecols=[0,2,3])
        data.to_csv(packets,header=False,index=False)
