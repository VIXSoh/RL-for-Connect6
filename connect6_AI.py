# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 22:40:46 2021

@author: joony
"""
import numpy as np
from connect6 import *
import random
import pickle

def getPanIndex(panStatus, size) :
    panIndex = np.array2string(panStatus,
                           max_line_width = size*size+size,
                           separator = "")
    return panIndex

class  CONNECT6_AI:
    def __init__(self, size = 10, side = "white", ep = 0.8, decrease = 0.9, reward = 1, alpha = 0.5):
        self.size = size
        self.panValues = {}
        self.panIndexTrail = []
        self.indexTrail = []
        self.directions = ["left", "leftTop", "top", 
                           "rightTop", "right", "rightBottom", 
                           "bottom", "leftBottom"]
        #self.panCopy = np.zeros(size*size, dtype = int)
        self.side = side
        self.ep = ep
        self.decrease = decrease
        self.reward = reward
        self.rock = 2
        self.alpha = alpha
        if side == "black" :
            self.rock = 1
    
    
    
    def addToTrail(self, panIndex, index):
        self.panIndexTrail.append(panIndex)
        self.indexTrail.append(index)
        
    
    
    
    def followTrail(self, rewardSign) :
        trailSize = len(self.panIndexTrail)
        
        for i in range(trailSize) :
            t = trailSize - i - 1
            newVal = self.reward * self.decrease ** i * rewardSign
            currentPan = self.panIndexTrail[t]
            currentIndex = self.indexTrail[t]
            t2 = t + 1
            if i == 0 : 
                t2 = t
            prevPan = self.panIndexTrail[t2]
            prevIndex = self.indexTrail[t2]
            self.updatePanValues(currentPan, currentIndex, newVal, prevPan, prevIndex, i)
        self.resetTrail()
        
    def resetTrail(self):
        self.panIndexTrail = []
        self.indexTrail = []
            
    def updatePanValues(self, panIndex, index, newValue, prevPan, prevIndex, i):
        if panIndex not in self.panValues :
            self.panValues[panIndex] = np.zeros(self.size**2, dtype = float)
        if i == 0 :
            self.panValues[panIndex][index] += newValue
        else :   
            self.panValues[panIndex][index] += self.alpha * (newValue + self.decrease * self.panValues[prevPan][prevIndex] - self.panValues[panIndex][index])




    def playNext(self, panStatus, firstRun = False, training = False):
        move1 = 0
        move2 = 0
        move1 = self.calculateNext(panStatus, self.side, self.ep, training)
        panIndex = getPanIndex(panStatus, self.size)
        
        self.addToTrail(panIndex, move1)
        if not firstRun : 
            panStatus2 = np.copy(panStatus)
            panStatus2[move1] = self.rock
            strightSum, straightMax = self.findStraightSum(panStatus2, move1, self.side)
            if straightMax < 6 and len(np.where(panStatus2 == 0)[0]) > 0:
                panIndex = getPanIndex(panStatus2, self.size)
                move2 = self.calculateNext(panStatus2, self.side, self.ep, training)
                self.addToTrail(panIndex, move2)
        AIout = np.zeros([2,2],dtype = int)
        AIout[0][0] = getX(self.size, move1)
        AIout[0][1] = getY(self.size, move1)
        AIout[1][0] = getX(self.size, move2)
        AIout[1][1] = getY(self.size, move2)
        return AIout
        
        
    def calculateNext(self, panStatus, side, ep, training) :
        panIndex = getPanIndex(panStatus, self.size)
        maxPos = -1
        maxVal = 0
        emptyIndex = np.where(panStatus == 0)[0]
        if len(emptyIndex) == 0:
            print("error here")
        if panIndex in self.panValues :
            panVal = self.panValues[panIndex]
            maxVal = panVal.max()
            maxPos = panVal.argmax()
        else :
            maxPos0, maxVal = self.calculateValue(panStatus, side)
            randomChoice = random.choices(emptyIndex, k = 1)[0]
            maxPos = random.choices([randomChoice, maxPos0], k = 1)[0]
            #maxPos = randomChoice
        
        if training :
            restP = 1 - ep
            optionSize = len(emptyIndex)
            weights = np.zeros(optionSize)
            maxIndex = np.where(emptyIndex == maxPos)
            weights += restP / optionSize
            weights[maxIndex] += ep
            selection = random.choices(emptyIndex, weights = weights, k = 1)[0]
            return selection
        else : 
            return maxPos
    
    def calculateValue(self, panStatus, side) :
        emptyIndex = np.where(panStatus == 0)[0]
        maxSeq = -1
        maxIndex = 0 
        rock = self.rock
        
        for i in emptyIndex :
            straightSum, straightMax = self.findStraightSum(panStatus, i, side)
            if straightMax > maxSeq :
                maxSeq = straightMax
                maxIndex = i
        
        return maxIndex, maxSeq
    
    def findStraightSum(self, panStatus, pos, side):
        rock = self.rock
        rocks = np.zeros(8)
        for i in range(8):
            currentDirection = self.directions[i]
            reachedEnd = False
            currentPosition = pos
            count = 0
            while not reachedEnd :
                count += 1
                if count > 30 : 
                    break
                nextPosition = getSequentialPosition(currentPosition, self.size, currentDirection)
                if nextPosition == -1 :
                    reachedEnd = True
                else : 
                    if panStatus[nextPosition] == rock :
                        rocks[i] += 1
                        currentPosition = nextPosition
                        # print("next po, next col, last col")
                        # print(nextPosition)
                        # print( Pan[nextPosition])
                        # print(self.sides[self.lastSide])
                    else :
                        reachedEnd = True
        
        straights = np.zeros(4)
        for i in range(4) :
            straights[i] = rocks[i] + rocks[i + 4] + 1
        straightSum = straights.sum()
        straightMax = straights.max()
        return straightSum, straightMax
    
    def saveModel(self, fileName):
        with open(fileName, 'wb') as handle:
            pickle.dump(self.panValues, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def loadModel(self, fileName):
        with open(fileName, 'rb') as handle:
            self.panValues = pickle.load(handle)


# size = 10

# panStatus = np.zeros(size*size, dtype = int)

# a = CONNECT6_AI()

# a.playNext(panStatus)

# panStatus[0] = 2
# panStatus[1] = 2
# panStatus[3] = 1
# panStatus[10] = 1

# a.playNext(panStatus)
# print(a.panIndexTrail)
# print(a.indexTrail)
# print(a.panValues)

# a.followTrail()
# print(a.panIndexTrail)
# print(a.indexTrail)
# print(a.panValues)


# panIndex = np.array2string(panStatus,
#                            max_line_width = size*size+size,
#                            separator = "")
# panValue = np.zeros(size*size, dtype = float)
# panValue[44] = 100.23




# panValues[panIndex] = panValue


# size = 10
# print(panValues)