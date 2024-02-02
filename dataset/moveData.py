import os, shutil

path = "/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/outdoor-run-20031017-arpl/Trace"
directory = os.fsencode(path)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.isnumeric():
        #os.mkdir(f'/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData/{filename}')
        newPath = path +f'/{filename}/APRL/10.0.0.{filename}.APRL.data.parsed'
        shutil.copy(newPath,f'/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData/{filename}')
        shutil.copy(path +f'/{filename}/gps_tcpdump/full/position.log.parsed',f'/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData/{filename}')
    