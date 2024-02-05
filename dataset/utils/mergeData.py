import os, shutil
import pandas as pd

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
            #print (lines)
            newFile = []
            for line in lines:
                print (coords)
                pTime = int(line.split(',')[1])
                cData = pd.read_csv(coords, delimiter=",",header=None)
                closestTime = cData.iloc[(cData[0].astype(int)-pTime).abs().argsort()[:1]]
                locData = ((closestTime).to_string(index=False,header=None))
                newLine = f'{line},{','.join(locData.split(' ')[1:])}\n'
                newFile.append(newLine)
            with open(path +f'/{filename}/data', 'w') as newData:
                for l in newFile:
                    newData.write(l)


              

            
            