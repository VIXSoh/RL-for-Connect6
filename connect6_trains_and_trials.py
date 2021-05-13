# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 21:51:48 2021

@author: joony
"""


from run_connect6 import *
from connect6_AI import *
import os

def play(gameSize, player, AI, whiteAI, training = False, graphOn = False) :
    game = initializeConnect6(gameSize)
    gameReal = True
    
    if player is "black" or player is "both":
        game, currentRound = startConnect6(game, gameSize, player=player)
    else :
        pan = game.getPan()
        AI_move = AI.playNext(pan, firstRun = True, training = training)
        game, currentRound = startConnect6(game, gameSize, player=player, AIsCall=AI_move)
    
    finished = False
    
    while not finished :
        AI_move = np.zeros([2,2],dtype = int)
        pan = game.getPan()
        color = game.getLastSide()
        if color is not player :
            if color is "black" :
                AI_move = AI.playNext(pan, firstRun = False, training = training)
            else : 
                AI_move = whiteAI.playNext(pan, firstRun = False, training = training)
        
        game, currentRound, finished, gameReal = runConnect6(game, currentRound, gameSize, player = player, AIsCall = AI_move, graphOn =graphOn )
    
    return game, gameReal

def learn(game, bAI, wAI) :
    if game.getLastSide() is "black" :
        bAI.followTrail(1)
        wAI.followTrail(-1)
    else :
        wAI.followTrail(1)
        bAI.followTrail(-1)

def train(bAI, wAI, gameSize, n, training, graphOn, ite) :
    for i in range(n):
        print(ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite,ite)
        print(i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)
        trainGame, gameReal = play(gameSize, "None", bAI, wAI, training, graphOn)
        if gameReal :
            learn(trainGame, bAI, wAI)
        else :
            bAI.resetTrail()
            wAI.resetTrail()
            


################ play

gameSize=10

bAI = CONNECT6_AI(size = 10, side = "black", ep = 0.85, decrease = 0.9, reward = 1)
wAI = CONNECT6_AI(size = 10, side = "white", ep = 0.85, decrease = 0.9, reward = 1)

fileName = "blackAI"
bAI.loadModel(fileName)
fileName = "whiteAI"
wAI.loadModel(fileName)

for i in range(10) :
    for i in range(5) :
        train(bAI, wAI, gameSize, 7000, True, False, i)
        fileName = "blackAI"
        bAI.saveModel(fileName)
        fileName = "whiteAI"
        wAI.saveModel(fileName)
    os.system("cp *AI save")

# testGame, gameReal = play(gameSize, "white", bAI, wAI)
# learn(testGame, bAI, wAI)