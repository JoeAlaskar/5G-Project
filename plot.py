#       Test function to plot a Hexagon     #
#       and the CUs - D2Ds inside           #
#############################################

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math, Hex

Rc = 500
Nc = 20
Nd = 20
distance = 20
g = Hex.Hex(Rc)
cellUsers = [g.randomPoints() for i in range(Nc)]
fig = plt.figure(1)
ax = plt.subplot(111)
ax.scatter(0, 0, color="#000000", zorder=10, s=10, label="BS")
for i in range(Nc):
	if(i==0):
		plt.scatter(cellUsers[i][0], cellUsers[i][1], color="#3232FF", zorder=3, s=15, label="CU")
	plt.scatter(cellUsers[i][0], cellUsers[i][1], color="#3232FF", zorder=3, s=15)


for i in range(Nd):
    a,b = g.randomPoints(2,distance)
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

circumradius = Rc
radius = circumradius * math.sqrt(3)/2
A = (circumradius,0)
B = (circumradius/2,math.sqrt(3)*circumradius/2)
C = (-circumradius/2,math.sqrt(3)*circumradius/2)
D = (-circumradius,0)
E = (-circumradius/2,-math.sqrt(3)*circumradius/2)
F = (circumradius/2,-math.sqrt(3)*circumradius/2)

hexo = [A,B,C,D,E,F]

#ax = fig.gca()
ax.add_patch(mpatches.Polygon(g.getVerts(), facecolor = "#D3D3D3", edgecolor = "#000000"))

plt.xlim(-circumradius,circumradius)
plt.ylim(-radius-10, radius+10)
ax.set_aspect('equal')
#plt.xlabel("distance (m)")
#plt.ylabel("distance (m)")
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
#plt.legend(loc="lower center")
plt.show()
