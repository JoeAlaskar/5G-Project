import Hex, Rmean, helpers, allocation, output
import numpy as np
import json, os


#################### Table values ###############################
with open('config.json', 'r') as f:
    config = json.load(f)
Rc = config["Rc"]
Nc = config["Nc"]
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
Ndvariation = range(int(0.1*Nc), int(Nc+(0.1*Nc)), int(0.1*Nc))


g = Hex.Hex(Rc) #Generate Hex of radius RC
#ellUsers = [g.randomPoints() for i in range(Nc)] # Generate Cell Users
cellUsers = []
with open("CUs.txt","r") as file:
    for line in file:
        temp = line.split(",")
        cellUsers.append((float(temp[0]),float(temp[1].rstrip('\n'))))
#Lists to save the throughts for different number of active D2D pairs
cellRates = []
d2dsRates = []
combinedRates = []


print(" Started Simulation")

for Nd in Ndvariation: #Outer Loop for simulating with different number of Active d2D pairs
    output.printProgress(Nd,Ndvariation) #Print progress on console
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
    
    rCU, rD2D = allocation.resourceAllocation(Nc, Nd, Nrb, Pd, pMax, bw, N0, tSNR, distance, cellUsers, d2dT, d2dR, time, rbPerD2DPair)

    cellThroughput = np.mean(rCU) #mean Throughput for all CUs
    d2dTrhoughput = np.mean(rD2D) #mean Throughput for all D2D pairs
    cellRates.append(cellThroughput) #add Cell user throughput to the list
    d2dsRates.append(d2dTrhoughput) #add D2D pairs throughput to the list
    combinedRates.append(cellThroughput + d2dTrhoughput) #Throughput of both the CUs and the D2Ds
print("\n Plot Saved")
output.plotThroughputvd2d(cellRates,d2dsRates,combinedRates,Ndvariation) #Plot the results
