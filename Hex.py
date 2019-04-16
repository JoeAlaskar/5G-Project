#           Last Update April 9th 2019      #
#############################################


#####To be Updated With Comments#####


import numpy as np, math, random

class Hex(object):
    def __init__(self, circumradius):
        self.circumradius = circumradius
        self.radius = circumradius * math.sqrt(3)/2
        self.A = (self.circumradius,0)
        self.B = (self.circumradius/2,math.sqrt(3)*self.circumradius/2)
        self.C = (-self.circumradius/2,math.sqrt(3)*self.circumradius/2)
        self.D = (-self.circumradius,0)
        self.E = (-self.circumradius/2,-math.sqrt(3)*self.circumradius/2)
        self.F = (self.circumradius/2,-math.sqrt(3)*self.circumradius/2)
    
    def getVerts(self):
        return [self.A,self.B,self.C,self.D,self.E,self.F]
    
    #Check if the point is inside the Hexagon
    def isInside(self, X,Y):
        x = abs(X)
        y = abs(Y)
        if (x > self.circumradius or y > self.radius):
            return 0
        cond = (self.circumradius * self.radius - self.circumradius * x - self.circumradius * y)>=0
        return cond
    
    #Generat a random point inside a circle
    def randomPointInCircle(self, rad, centerX, centerY, onCircumference = 0):
        theta = 2 * math.pi * random.random()
        if onCircumference == 1:
            r = rad
        else:
            r = rad * math.sqrt(random.randint(0, pow(10,3)) / float(pow(10,3)))
        x = fromX + r * math.cos(theta)
        y = fromY + r * math.sin(theta)
        return x,y

    #Return Random Points inside the Hexagon
    def randomPoints(self,numberOfPoints = 1, distanceD2D = 0):
        x, y = self.randomPointInCircle(self.circumradius-distanceD2D, 0, 0)
        while((not self.isInside(x,y))):
            x, y = self.randomPointInCircle(self.circumradius, 0, 0)
        if numberOfPoints == 1:
            return (x,y)
        x2, y2 = self.randomPointInCircle(distanceD2D, x, y,1)
        while((not self.isInside(x2,y2))):
            x2, y2 = self.randomPointInCircle(distanceD2D, x, y,1)
        return (x,y),(x2,y2)
