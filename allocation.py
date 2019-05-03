#           Last Update April 31st 2019      #
#############################################

import Hex, Rmean, helpers
import numpy as np

def resourceAllocation(Nc, Nd, Nrb, Pd, pMax, bw, N0, tSNR, distance, cellUsers, d2dT, d2dR, time = 100, rbPerD2DPair = 1):
	rCU = [] #Cell user rate
	rD2D = [] #d2d pair rate
	cellRwindow = Rmean.Rmean(Nc, time) #R_d[n]
	d2dRwindow = Rmean.Rmean(Nd, time)
	for n in range(time): #for each frames
		gcB = helpers.channelGain(Nc, cellUsers, Nrb) #Channel Gain
		rbsAssignedToCU, cuAssignedToRB,r = helpers.resourceBlockAllocation(Nc, Nrb, pMax, bw, N0, gcB, cellRwindow.get()) #Please read helpers.py for info on the output (lines 126-128)
		#The next few line calculates the gains needed
		#################################################################
		gcBs = helpers.cuGainCB(Nrb, cuAssignedToRB,gcB)
		rates = helpers.getCUrate(Nc, rbsAssignedToCU,r)
		Rcell = cellRwindow.add(rates)
		rCU.append(np.sum(rates))
		g_dTB = helpers.gainTB(Nd, Nrb, d2dT)
		g_dTdR = helpers.gainTR(Nrb,distance)
		g_CdR = helpers.gainCR(Nd, Nrb, cellUsers, cuAssignedToRB, d2dR)
		g_CB = np.asarray(gcBs)
		#################################################################
		rates = [] # r_d
		for d in range(Nd):
			P_dT =  (((pMax * g_CB) / (tSNR * g_dTB[d])) - (N0 / g_dTB[d])) # Calculate the power
			P_dT = helpers.powerCheck(P_dT,pMax) # Every power value has to be between 0 and pMax
			r = (1 + ((P_dT * g_dTdR) / (N0 + (Pd * g_CdR[d]))))
			r = bw * np.log2(r)
			rates.append(list(r))
		lambdas = []
		for ratelist, Rd2d in zip(rates, d2dRwindow.get()): #Calculate the lambdas
			lambdas.append(ratelist / Rd2d)
		
		alloc = helpers.d2dAllocate(lambdas,rbPerD2DPair) #Get the optimal Assignment for D2D pair - RB
		d2dRates = [rates[x[1][0]][x[1][1]] for x in alloc] #list of D2D pairs throughput after the assignment
		d2dRwindow.add(d2dRates) #Update R_d[n]
		rD2D.append(np.sum(d2dRates)) #Throughput of all the D2D pairs
	return rCU, rD2D

def throughput(rbsAssignedToCU, cuAssignedToRB, rr, alloc, Nc, Nd, Nrb, Pd, pMax, bw, N0, tSNR, distance, cellUsers, d2dT, d2dR, time = 100):
    rCU = [] #Cell user rate
    rD2D = [] #d2d pair rate
    cellRwindow = Rmean.Rmean(Nc, time) #R_d[n]
    d2dRwindow = Rmean.Rmean(Nd, time)
    for n in range(time): #for each frames
        gcB = helpers.channelGain(Nc, cellUsers, Nrb) #Channel Gain
        #The next few line calculates the gains needed
        #################################################################
        gcBs = helpers.cuGainCB(Nrb, cuAssignedToRB,gcB)
        rates = helpers.getCUrate(Nc, rbsAssignedToCU,rr)
        Rcell = cellRwindow.add(rates)
        rCU.append(np.sum(rates))
        g_dTB = helpers.gainTB(Nd, Nrb, d2dT)
        g_dTdR = helpers.gainTR(Nrb,distance)
        g_CdR = helpers.gainCR(Nd, Nrb, cellUsers, cuAssignedToRB, d2dR)
        g_CB = np.asarray(gcBs)
        #################################################################
        rates = [] # r_d
        for d in range(Nd):
            P_dT =  (((pMax * g_CB) / (tSNR * g_dTB[d])) - (N0 / g_dTB[d])) # Calculate the power
            P_dT = helpers.powerCheck(P_dT,pMax) # Every power value has to be between 0 and pMax
            r = (1 + ((P_dT * g_dTdR) / (N0 + (Pd * g_CdR[d]))))
            r = bw * np.log2(r)
            rates.append(list(r))
        lambdas = []
        for ratelist, Rd2d in zip(rates, d2dRwindow.get()): #Calculate the lambdas
            lambdas.append(ratelist / Rd2d)
        
        d2dRates = [rates[x[1][0]][x[1][1]] for x in alloc] #list of D2D pairs throughput after the assignment
        d2dRwindow.add(d2dRates) #Update R_d[n]
        rD2D.append(np.sum(d2dRates)) #Throughput of all the D2D pairs
    return rCU, rD2D


def testingResourceAllocation(Nc, Nd, Nrb, Pd, pMax, bw, N0, tSNR, distance, cellUsers, d2dT, d2dR, time = 100, rbPerD2DPair = 1):
    rCU = [] #Cell user rate
    rD2D = [] #d2d pair rate
    cellRwindow = Rmean.Rmean(Nc, time) #R_d[n]
    d2dRwindow = Rmean.Rmean(Nd, time)
    gcB = helpers.channelGain(Nc, cellUsers, Nrb) #Channel Gain
    rbsAssignedToCU, cuAssignedToRB,rr = helpers.resourceBlockAllocation(Nc, Nrb, pMax, bw, N0, gcB, cellRwindow.get()) #Please read helpers.py for info on the output (lines 126-128)
    for n in range(time): #for each frames
        gcB = helpers.channelGain(Nc, cellUsers, Nrb) #Channel Gain
        rbsAssignedToCU, cuAssignedToRB,rr = helpers.resourceBlockAllocation(Nc, Nrb, pMax, bw, N0, gcB, cellRwindow.get()) #Please read helpers.py for info on the output (lines 126-128)
        #The next few line calculates the gains needed
        #################################################################
        gcBs = helpers.cuGainCB(Nrb, cuAssignedToRB,gcB)
        rates = helpers.getCUrate(Nc, rbsAssignedToCU,rr)
        Rcell = cellRwindow.add(rates)
        rCU.append(np.sum(rates))
        g_dTB = helpers.gainTB(Nd, Nrb, d2dT)
        g_dTdR = helpers.gainTR(Nrb,distance)
        g_CdR = helpers.gainCR(Nd, Nrb, cellUsers, cuAssignedToRB, d2dR)
        g_CB = np.asarray(gcBs)
        #################################################################
        rates = [] # r_d
        for d in range(Nd):
            P_dT =  (((pMax * g_CB) / (tSNR * g_dTB[d])) - (N0 / g_dTB[d])) # Calculate the power
            P_dT = helpers.powerCheck(P_dT,pMax) # Every power value has to be between 0 and pMax
            r = (1 + ((P_dT * g_dTdR) / (N0 + (Pd * g_CdR[d]))))
            r = bw * np.log2(r)
            rates.append(list(r))
        lambdas = []
        for ratelist, Rd2d in zip(rates, d2dRwindow.get()): #Calculate the lambdas
            lambdas.append(ratelist / Rd2d)
        
        alloc = helpers.d2dAllocate(lambdas,rbPerD2DPair) #Get the optimal Assignment for D2D pair - RB
        d2dRates = [rates[x[1][0]][x[1][1]] for x in alloc] #list of D2D pairs throughput after the assignment
        d2dRwindow.add(d2dRates) #Update R_d[n]
        rD2D.append(np.sum(d2dRates)) #Throughput of all the D2D pairs
    return rbsAssignedToCU, cuAssignedToRB, rr, alloc, rCU, rD2D
