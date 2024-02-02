#!/usr/bin/env python
import pandas as pd

l = "./50/10.0.0.50.APRL.data.parsed.csv ./32/10.0.0.32.APRL.data.parsed.csv ./35/10.0.0.35.APRL.data.parsed.csv ./34/10.0.0.34.APRL.data.parsed.csv ./33/10.0.0.33.APRL.data.parsed.csv ./18/10.0.0.18.APRL.data.parsed.csv ./9/10.0.0.9.APRL.data.parsed.csv ./11/10.0.0.11.APRL.data.parsed.csv ./7/10.0.0.7.APRL.data.parsed.csv ./16/10.0.0.16.APRL.data.parsed.csv ./45/10.0.0.45.APRL.data.parsed.csv ./28/10.0.0.28.APRL.data.parsed.csv ./17/10.0.0.17.APRL.data.parsed.csv ./1/10.0.0.1.APRL.data.parsed.csv ./19/10.0.0.19.APRL.data.parsed.csv ./26/10.0.0.26.APRL.data.parsed.csv ./8/10.0.0.8.APRL.data.parsed.csv ./21/10.0.0.21.APRL.data.parsed.csv ./44/10.0.0.44.APRL.data.parsed.csv ./38/10.0.0.38.APRL.data.parsed.csv ./36/10.0.0.36.APRL.data.parsed.csv ./31/10.0.0.31.APRL.data.parsed.csv ./30/10.0.0.30.APRL.data.parsed.csv ./39/10.0.0.39.APRL.data.parsed.csv ./41/10.0.0.41.APRL.data.parsed.csv ./48/10.0.0.48.APRL.data.parsed.csv ./15/10.0.0.15.APRL.data.parsed.csv ./3/10.0.0.3.APRL.data.parsed.csv ./12/10.0.0.12.APRL.data.parsed.csv ./49/10.0.0.49.APRL.data.parsed.csv ./40/10.0.0.40.APRL.data.parsed.csv ./47/10.0.0.47.APRL.data.parsed.csv ./13/10.0.0.13.APRL.data.parsed.csv ./14/10.0.0.14.APRL.data.parsed.csv ./25/10.0.0.25.APRL.data.parsed.csv"
arr = l.split(" ")
arr = ["/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData" + i[1:] for i in arr]
for i in arr:
    data = pd.read_csv(i, header=None, delim_whitespace=True)
    

    data.drop(index = 0, inplace=False, axis=1)

