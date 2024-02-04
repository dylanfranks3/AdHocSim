import os, shutil
import pandas as pd

path = "/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData"
directory = os.fsencode(path)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename!='1':
        packets = path +f'/{filename}/position.log.parsed.csv'
        data = pd.read_csv(packets, delimiter="\s+\s+",header=None)
        data.to_csv(packets,header=False,index=False)
