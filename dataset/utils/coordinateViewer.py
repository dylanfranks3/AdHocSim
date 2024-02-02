#!/usr/bin/env python
import csv



with open('APlocations.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    content = ""
    for row in csv_reader:
        try:
            content += f"({float(row[1])/10000},{float(row[2])/10000}),"
        except:
            pass
        
    print(content)