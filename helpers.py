#           Last Update April 9th 2019      #
#############################################

import numpy as np, random, math

def channelGain(Nc, CU, Nrb):
    """
    Function that calculates the gain g_CB
    Arguments:
        Nc:     Number of CUs
        CU:     Cell Users locations (x,y)
        Nrb:    Number of Resource Blocks
    Return:
        g_CB:   matrix of size Nc x Nrb
    """
    g1 = np.random.rayleigh(1, [Nc, Nrb])
    g_CB = np.zeros([Nc, Nrb]) #gain
    for i in range(Nc):
        c = CU[i]
        d = (np.sqrt(pow(c[0],2) + pow(c[1],2)) / 1000)
        pL = 128.1 + 37.6 * np.log10(d)
        pl = pow(10,(pL / 10)) #Convert from dB to linear
        g_CB[i] = pow(g1[i],2) / pl
    return g_CB

def achievableRate(g_CB, Pc, BW, N0):
    """
    Function that calculates achievable rate
    r_d for all rates in g_CB
    Arguments:
        g_CB:   gains of C (type list)
        Pc:     Power constant
        BW:     BandWidth
        N0:     spectral density
    Return:
        rates:   list of size Nrb
    """
    rates = []
    for g in g_CB:
        r = BW * math.log2(1 + ((Pc * g) / N0))
        rates.append(r)
    return rates

def gainTB(Nd, Nrb, t):
    """
    Function that calculates g_TB
    Arguments:
        Nd:     Number of 
        Nrb:    Number of Resource Blocks
        t:  Transmitters
    Return:
        glist:  Gain from D2D Transmitter to Base Station
    """
    g = np.random.rayleigh(1,[Nd,Nrb])   #rayleigh fading
    gList = []
    for i in range(Nd):
        distance = (math.sqrt(pow(t[i][0],2) + pow(t[i][1],2)))/1000
        pl = 128.1 + 37.6*np.log10(distance)
        pl = pow(10,(pl/10))   #Convert from dB to linear
        gain = pow(g[i],2)/(pl)
        gList.append(list(gain))
    return np.asarray(gList)

def gainTR(Nrb, d):
    """
    Function that calculates g_TR 
    Arguments:
        Nrb:    Number of Resource Blocks
        d:      Distance between Transmitter and receiver
    Return:
        glist: Gain from D2D Transmitter to D2D receiver
    """
    g = np.random.rayleigh(1,[1,Nrb])   #rayleigh fading
    pl = 128.1 + 37.6*np.log10(d / 1000) #distance in Km
    pl = pow(10,(pl/10))  #Convert from dB to linear
    gain = (pow(g,2)/pl)
    gList = gain.tolist()
    return np.asarray(gList[0])

def gainCR(Nd, Nrb, CU, AlloRB, d2d_r):
    """
    Function that calculates g_CR
    Arguments:
        Nd:     Number of d2d pairs
        Nrb:    Number of Resource Blocks
        CU:     Cell Users locations (x,y)
        AlloRB: Allocated Resource Blocks
        d2d_r:  Receiver 
    Return:
        glist:  Gain from Cell User to D2D receiver
    """
    dist=[]     #Distance from Cell User to Receiver
    g = np.random.rayleigh(1,[Nd,Nrb])   # rayleigh fading
    for i in range(Nd):
        d = []
        for j in range(Nrb):
            Cx = CU[AlloRB[j]][0]
            Cy = CU[AlloRB[j]][1]
            Rx = recv[i][0]
            Ry = recv[i][1]
            distance =math.sqrt(pow((cell_x-d2d_x),2) + pow((cell_y-d2d_y),2))
            d.append(distance/1000)
        dist.append(d)
    gList = []
    for i in range(Nd):
        pl = 128.1 + 37.6*np.log10(dist[i])
        pl = pow(10,(pl/10))  #Convert from dB to linear
        gain = pow(g[i],2)/(pl)
        gList.append(list(gain))
    return np.asarray(gList)


def resourceBlockAllocation(Nc, Nrb, Pc, bw, N0, g_CB, Rbar):
    """
    Resource Block Allocation for CUs Function
    Arguments:
        Nc:                     Number of CUs
        Nrb:                    Number of Resource Blocks
        Pc:                     Power
        bw:                     Bandwidth
        N0:                     spectral density
        g_CB:                   gain
        Rbar:                   rate mean 
    Return:
        rbsAssignedToCU:        Resource Blocks assigned to each CU
        cuAssignedToRB:         CUs assigned to each Resource Block
        r:                      rate i.e. r_d
    """
    rbsAssignedToCU = [[] for x in range(Nc)] #list of Resource Blocks Assigned to CU[i]
    cuAssignedToRB = [-1 for x in range(Nrb)] #CU Assigned to RB[i]
    assignedCUs = [] #CUs assigned a Resource Block
    r = [] #rate
    l = [] #lambda
    for g,R in zip(g_CB, Rbar):
        rate = achievableRate(g, Pc, bw, N0)
        r.append(rate)
        l.append(rate / R)
    l = np.transpose(l)

    for i in range(Nrb): #Assign RBs to CUs
        lOfRBi = np.argsort(l[i]) #Lambda row of RB[i] indirectly sorted
        j = Nc - 1 #Index of Index of CU with highest lambda
        while(lOfRBi[j] in assignedCUs): #While the selected CU is already assigned a block, get the next CU
            j -= 1
        if((not rbsAssignedToCU[lOfRBi[j]]) and (i > 0)): #If CU[i] was not assigned a RB and i>0
            assignedCUs.append(cuAssignedToRB[i - 1]) #Add the CU assigned to the last RB to the Assigned list
        rbsAssignedToCU[lOfRBi[j]].append(i) #Add RB[i] to the list of assigned RBs to the CU
        cuAssignedToRB[i] = lOfRBi[j] #Assign the CU to RB[i]
    return rbsAssignedToCU, cuAssignedToRB, r

def getCUrate(Nc,rbsAssignedToCU,r):
    """
    A function that returns the rate of each CU 
    (i.e CU[i]'s rate is sum of the rates r[CUi][RBs])
    Arguments:
        Nc:                     Number of CUs
        rbsAssignedToCU:        Resource Blocks assigned to each CU
        r:                      rate i.e. r_d
    Return:
        cuRate:                 list of rates 
    """
    cuRate = np.asarray([0 for x in range(Nc)]) #CU[i] rate (sum of the rates r[CUi][RBs])
    for i in range(Nc):
        if(not rbsAssignedToCU[i]):
            cuRate[i] = 1
        else:
            for y in rbsAssignedToCU[i]:
                cuRate[i] += r[i][y]
    return cuRate


def cuGainCB(Nrb,cuAssignedToRB, g_CB):
    """
    A function that returns the g_CB for each C 
    Arguments:
        Nrb:                    Number of Resource Blocks
        cuAssignedToRB:         CUs assigned to each Resource Block
        g_CB:                   gain matrix
    Return:
        gcBs:                   list of gains
    """
    gcBs = []
    for i in range(Nrb):
        gcBs.append(g_CB[cuAssignedToRB[i]][i])
    return gcBs
