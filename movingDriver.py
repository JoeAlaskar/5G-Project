import Hex, Rmean, helpers, allocation, output
import numpy as np
import json, math, os

#################### Table values ###############################
with open('config.json', 'r') as f:
    config = json.load(f)
Rc = config["Rc"]
Nc = config["Nc"]
Nd = config["Nd"]
Nrb = config["Nrb"]
distance = config["distance"]
Pd = config["Pd"]
pMax = config["pMax"]
N_dBm = config["N_dBm"]
bw = config["bw"]
tSNR_dB = config["tSNR_dB"]
time = config["time"]
rbPerD2DPair = config["rbPerD2DPair"]
################################################################
N0 = pow(10,(N_dBm / 10)) * pow(10,(-3))
N0 = N0 * bw
tSNR = pow(10,(tSNR_dB / 10))

g = Hex.Hex(Rc) #Generate Hex of radius RC
#cellUsers = [g.randomPoints() for i in range(Nc)] # Generate Cell Users
#Lists to save the throughts for different number of active D2D pairs
os.system('g++ -std=c++11 Hex.cpp -o hex')
arg = "./hex " + str(Rc) + " " + str(Nc)
os.system(arg)
cellUsers = []
with open("CUs.txt","r") as file:
    for line in file:
        temp = line.split(",")
        cellUsers.append((float(temp[0]),float(temp[1].rstrip('\n'))))
i = 0
d2dT = [] #Transmitter list
d2dR = [] #Receiver list
arg = "./hex " + str(Rc) + " " + str(Nd) + " " + str(distance)
os.system(arg)
with open("D2Ds.txt","r") as file:
    for line in file:
        temp = line.split(",")
        if (i%2 == 0):
            d2dT.append((float(temp[0]),float(temp[1].rstrip('\n'))))
        else:
            d2dR.append((float(temp[0]),float(temp[1].rstrip('\n'))))
        i = i+1

cellRates = []
d2dsRates = []
combinedRates = []

inCarIndex = range(0,8) #~1/3
walkingIndex = range(8,15)#~1/3

output.plotHex(Rc, Nc, Nd, cellUsers, d2dT, d2dR, g, "1")

print(" Started Simulation")

for i in range(10):
	output.printProgress(i,range(10)) #Print progress on console
	rCU, rD2D = allocation.resourceAllocation(Nc, Nd, Nrb, Pd, pMax, bw, N0, tSNR, distance, cellUsers, d2dT, d2dR, time,rbPerD2DPair)
	cellThroughput = np.mean(rCU) #mean Throughput for all CUs
	d2dTrhoughput = np.mean(rD2D) #mean Throughput for all D2D pairs
	cellRates.append(cellThroughput) #add Cell user throughput to the list
	d2dsRates.append(d2dTrhoughput) #add D2D pairs throughput to the list
	combinedRates.append(cellThroughput + d2dTrhoughput) #Throughput of both the CUs and the D2Ds
	for j in inCarIndex:
		cellUsers[j] = g.movePoint(cellUsers[j], True, 1000)
		d2dT[j], d2dR[j] = g.movePair(d2dT[j], d2dR[j], True, 1000)
	for j in walkingIndex:
		cellUsers[j] = g.movePoint(cellUsers[j], False, 1000)
		d2dT[j], d2dR[j] = g.movePair(d2dT[j], d2dR[j], False, 1000)

print("\n Plot Saved")
output.plotThroughput(cellRates,d2dsRates,combinedRates,range(10),"Time (s)") #Plot the results
output.plotHex(Rc, Nc, Nd, cellUsers, d2dT, d2dR, g, "2")

