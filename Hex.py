#           Last Update April 30th 2019      #
#############################################

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
        x = centerX + r * math.cos(theta)
        y = centerY + r * math.sin(theta)
        return x,y
    
    #Return Random Points inside the Hexagon
    def randomPoints(self,numberOfPoints = 1, distanceD2D = 0):
        x, y = self.randomPointInCircle(self.circumradius, 0, 0)
        while((not self.isInside(x,y))):
            x, y = self.randomPointInCircle(self.circumradius, 0, 0)
        if numberOfPoints == 1:
            return (x,y)
        x2, y2 = self.randomPointInCircle(distanceD2D, x, y,1)
        while((not self.isInside(x2,y2))):
            x2, y2 = self.randomPointInCircle(distanceD2D, x, y,1)
        return (x,y),(x2,y2)
    
    #Move the point i.e. simulate a device move
    def movePoint(self, user, car = False, time = 10):
        if (car == True):
            speed = 0.0014 #meter/ms
        else:
            speed = 0.0313 #meters/ms
        distance = speed * time
        x,y = self.randomPointInCircle(distance, user[0], user[1], 1)
        if(self.isInside(x,y)):
            return (x,y)
        else:
            print("User Exited Base Station's Cell, A new user turned on his device")
            return self.randomPoints()

    #Move the point i.e. simulate a device move
    def movePair(self, T, R, car = False, time = 10):
        if (car == True):
            speed = 0.0014 #meter/ms
        else:
            speed = 0.0313 #meters/ms
        distance = speed * time
        x,y = self.randomPointInCircle(distance, T[0], T[1], 1)
        #If Trans. left cell generate new pair
        if(not(self.isInside(x,y))):
            print("D2D pair Exited Base Station's Cell, A new pair turned on their devices")
            return self.randomPoints(2,distance)
        xTravel = x-T[0]
        yTravel = y-T[1]
        x2 = R[0] + xTravel
        y2 = R[1] + yTravel
        if(not(self.isInside(x2,y2))):
            print("D2D pair Exited Base Station's Cell, A new pair turned on their devices")
            return self.randomPoints(2,distance)
        ## Proof of distance ##
        #d = math.sqrt(pow(x2-x,2)+pow(y2-y,2))
        #print("Distance: ", d)
        return (x,y),(x2,y2)
