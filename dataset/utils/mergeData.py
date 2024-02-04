import os, shutil

path = "/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData"
directory = os.fsencode(path)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.isnumeric():
        #os.mkdir(f'/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData/{filename}')
        packets = path +f'/{filename}/10.0.0.{filename}.APRL.data.parsed.csv'
        coords = path +f'/{filename}/position.log.parsed.csv'
        with open(packets,'r+') as pFile:
            lines = pFile.read().splitlines()
            for line in lines:
                

            
            