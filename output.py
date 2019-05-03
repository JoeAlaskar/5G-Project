#           Last Update April 30th 2019      #
#############################################

import pylab as pl
import numpy as np
import sys,math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def plotThroughputvd2d(celltp,d2dtp,combinedtp,nds):
    pl.figure()
    pl.plot(nds, np.asarray(celltp) / 1e6, label="Cell Users")
    pl.scatter(nds, np.asarray(celltp) / 1e6, marker=">")
    pl.plot(nds, np.asarray(d2dtp) / 1e6, label="D2D Pairs")
    pl.scatter(nds, np.asarray(d2dtp) / 1e6, marker=">")
    pl.plot(nds, np.asarray(combinedtp) / 1e6, label="Both")
    pl.scatter(nds, np.asarray(combinedtp) / 1e6, marker=">")
    pl.xlabel("No. of D2D Pairs")
    pl.ylabel("Throughput (Mbits/sec)")
    pl.legend(loc="upper left")
    pl.grid(True)
    pl.savefig("nd2d.eps", transparent=True)
    pl.show()

def plotThroughput(celltp,d2dtp,combinedtp,nds, xlabelString, name = "plot"):
    pl.figure()
    pl.plot(nds, np.asarray(celltp) / 1e6, label="Cell Users")
    pl.scatter(nds, np.asarray(celltp) / 1e6, marker=">")
    pl.plot(nds, np.asarray(d2dtp) / 1e6, label="D2D Pairs")
    pl.scatter(nds, np.asarray(d2dtp) / 1e6, marker=">")
    pl.plot(nds, np.asarray(combinedtp) / 1e6, label="Both")
    pl.scatter(nds, np.asarray(combinedtp) / 1e6, marker=">")
    pl.xlabel(xlabelString)
    pl.ylabel("Throughput (Mbits/sec)")
    pl.legend(loc="upper left")
    pl.grid(True)
    name = name + ".eps"
    pl.savefig(name, transparent=True)
    pl.show()



def printProgress(Nd,Ndvariation):
    now = Ndvariation.index(Nd)
    max = len(Ndvariation)
    sys.stdout.write("\r")
    progress = int(100* ((now+1)/ max))
    percent = "{:2}".format(progress)
    sys.stdout.write(" " + percent + " % ")
    [sys.stdout.write("*") for x in range(now+1)]
    sys.stdout.flush()

def plotHex(Rc, Nc, Nd, cellUsers, d2dT, d2dR, g, name = "fig"):
    radius = Rc * math.sqrt(3)/2
    fig = plt.figure(1)
    ax = plt.subplot(111)
    ax.scatter(0, 0, color="#000000", zorder=10, s=10, label="BS")
    #Plot the CU points
    for i in range(Nc):
        if(i==0):
            plt.scatter(cellUsers[i][0], cellUsers[i][1], color="#3232FF", zorder=3, s=15, label="CU")
        plt.scatter(cellUsers[i][0], cellUsers[i][1], color="#3232FF", zorder=3, s=15)
    #Plot the D2D pairs
    for i in range(Nd):
        a = d2dT[i]
        b = d2dR[i]
        if(i==0):
            ax.scatter(a[0], a[1], color="#FFA500", zorder=3, s=15, label="Transmitter")
            ax.scatter(b[0], b[1], color="#FF0000", zorder=3, s=15, label="Receiver")
            x = [a[0],b[0]]
            y = [a[1],b[1]]
            ax.plot(x, y, color="#000000", zorder=2, linewidth = 1)
        else:
            ax.scatter(a[0], a[1], color="#FFA500", zorder=3, s=15)
            ax.scatter(b[0], b[1], color="#FF0000", zorder=3, s=15)
            x = [a[0],b[0]]
            y = [a[1],b[1]]
            ax.plot(x, y, color="#000000", zorder=2, linewidth = 1)
    #Plot Hexagon
    ax.add_patch(mpatches.Polygon(g.getVerts(), facecolor = "#D3D3D3", edgecolor = "#000000"))

    plt.xlim(-Rc,Rc)
    plt.ylim(-radius-10, radius+10)
    ax.set_aspect('equal')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=5)
    name = name + ".eps"
    plt.savefig(name, transparent=True)
    plt.clf()
