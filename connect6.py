# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 14:09:37 2021

@author: joony
"""

import numpy as np

def getX(size, position) :
    return position % size

def getY(size, position) :
    return position // size 

def getPosition(size, x, y) :
    return y * size + x

def sequenceCalculation(directionNumberX, directionNumberY, size, x, y):
    returnPosition = -1
    
    x += directionNumberX
    y += directionNumberY
    
    if (x < 0) or (x >= size) :
        return returnPosition        
    if (y < 0) or (y >= size) :
        return returnPosition
    
    return getPosition(size, x, y)

def getSequentialPosition(position, size, direction):
    x = getX(size, position)
    y = getY(size, position)
    directionNumberX = 0
    directionNumberY = 0
    
    if direction == "left":
        directionNumberX = -1
    elif direction == "leftTop" :
        directionNumberX = -1
        directionNumberY = 1
    elif direction == "top" :
        directionNumberY = 1
    elif direction == "rightTop" :
        directionNumberX = 1
        directionNumberY = 1
    elif direction == "right" :
        directionNumberX = 1
    elif direction == "rightBottom" :
        directionNumberX = 1
        directionNumberY = -1
    elif direction == "bottom" :
        directionNumberY = -1
    elif direction == "leftBottom" :
        directionNumberX = -1
        directionNumberY = -1
    else :
        print ("get sequential position error occured")
    
    nextSequence = sequenceCalculation(directionNumberX, directionNumberY, size, x, y)
    
    return nextSequence

def returnPan(pan, size) :
    blackx = []
    blacky = []
    whitex = []
    whitey = []
    
    for i in range(len(pan)) :
        x = getX(size, i)
        y = getY(size, i)
        if pan[i] == 1 :
            blackx.append(x)
            blacky.append(y)
        if pan[i] == 2 :
            whitex.append(x)
            whitey.append(y)
    
    return blackx, blacky, whitex, whitey

class  CONNECT6:
    def __init__(self, size = 19):
        self.size = size
        self.Pan = np.zeros(size*size, dtype = int)
        self.Done = False
        self.max = np.zeros(2, dtype = int)
        self.lastPosition = -1
        self.lastSide = "black"
        self.directions = ["left", "leftTop", "top", 
                           "rightTop", "right", "rightBottom", 
                           "bottom", "leftBottom"]
        self.sides = {"black": 1, "white":2}
        self.realGame = True
        
    def getPan(self):
        return self.Pan
    
    def isRealGame(self):
        return self.realGame
    
    def getMax(self):
        return self.max.max()
    
    def getSize(self):
        return self.size
    
    def getLastSide(self):
        return self.lastSide
    
    def changeSide(self):
        if self.lastSide == "black":
            self.lastSide = "white"
        else : 
            self.lastSide = "black"
    
    def add(self, x, y, side):
        position = getPosition(self.size, x, y)
        rock = 0
        if side == "black" :
            rock = 1
        else : 
            rock = 2
        self.Pan[position] = rock
        self.lastPosition = position
        self.lastSide = side
    
    def check(self, x, y):
        if (x < 0) or (x >= self.size):
            return False
        if (y < 0) or (y >= self.size):
            return False
        position = getPosition(self.size, x, y)
        if self.Pan[position] != 0 :
            return False
        return True
    
    def isDone(self):
        return self.Done
    
    def updateMax(self):
        rocks = np.zeros(8)
        for i in range(8):
            currentDirection = self.directions[i]
            reachedEnd = False
            currentPosition = self.lastPosition
            count = 0
            while not reachedEnd :
                count += 1
                if count > 30 : 
                    break
                nextPosition = getSequentialPosition(currentPosition, self.size, currentDirection)
                if nextPosition == -1 :
                    reachedEnd = True
                else : 
                    if self.Pan[nextPosition] == self.sides[self.lastSide] :
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
        if straights.max() > self.max[ self.sides[self.lastSide] - 1 ] :
            self.max[ self.sides[self.lastSide] - 1 ] = straights.max()
        
    def updateStatus(self):
        if self.max.max() >= 6 :
            self.Done = True
        if len(np.where(self.Pan == 0)[0]) == 0:
            self.Done = True
            self.realGame = False
    
    
        
            