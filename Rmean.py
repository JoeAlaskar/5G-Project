#    keep track of the long-term average rate #
###############################################

import numpy as np, math, random

class Rmean(object):
    def __init__(self,n, wSize):
        self.R = [[1] * wSize] * n
        self.mean = [np.mean(r) for r in self.R]
    def add(self, rates):
        for r,newRate in zip(self.R,rates):
            r.pop(0)
            r.append(newRate)
        self.mean = [np.mean(r) for r in self.R]
        return self.mean
    def get(self):
        return self.mean
