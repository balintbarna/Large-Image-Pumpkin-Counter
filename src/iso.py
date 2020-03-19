#!/usr/bin/python
import numpy as np

data = []  

lines = [line.rstrip() for line in open("../output/iso.txt")] 
for i in range(len(lines)): # for all lines
	if len(lines[i]) > 0 and lines[i][0] != '#': # if not a comment or empty line
		csv = np.asarray(lines[i].split (': ')) # split into comma separated list
		data.append(float(csv[1]))

print("min: ",min(data))
print("max: ",max(data))
print("mean:",sum(data)/len(data))
