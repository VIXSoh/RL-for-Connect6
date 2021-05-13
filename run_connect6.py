# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 16:54:17 2021

@author: joony
"""

from connect6 import *
import matplotlib.pyplot as plt


def initializeConnect6(gameSize=19) :
    game = CONNECT6(gameSize)
    return game

def startConnect6(game, gameSize, player="both", AIsCall=None) :
    game = game
    print("Game start! type any non-numeric to exit.")
    currentRound = 0
    turnsTaken = 0
    while turnsTaken < 1:
        
        if player is "both" or player is game.getLastSide():
            x = int(input("Indicate X coordinate (0 ~ " + str(game.getSize()-1) + ") : "))
            y = int(input("Indicate Y coordinate (0 ~ " + str(game.getSize()-1) + ") : "))
        else : # when both are ai or when it is AI's turn
            x = AIsCall[0][0]
            y = AIsCall[0][1]
        
        doable = game.check(x, y)
        if doable :
            game.add( x, y, game.getLastSide())
            game.updateMax()
            turnsTaken += 1
        else :
            pass
    
    game.changeSide()
    
    return game, currentRound
    
def runConnect6(game, currentRound, gameSize, player="both", AIsCall=None, graphOn = False) : 
    sideDone = False
    finished = False
    game = game
    currentRound = currentRound
    while not sideDone and not finished :
        sideTaken = 0
        while not finished :
            currentRound += 1
            side = game.getLastSide()
            #print("current round is " + str(currentRound) + " and the side is " + str(side))
            turnsTaken = 0
            while turnsTaken < 2:
                
                if player is "both" or player is game.getLastSide():
                    print("current round is " + str(currentRound) + " and the turn is " + str(turnsTaken) + ". Take the next move " + str(side) + ".")
                    blkx, blky, whtx, whty = returnPan(game.getPan(), game.getSize())
                    
                    fig = plt.figure()
                    ax1 = fig.add_subplot(111)
                    
                    ax1.set_facecolor('grey')
                    plt.xlim([-1,gameSize])
                    plt.ylim([-1,gameSize])
                    plt.xticks(np.arange(0, gameSize, 1))
                    plt.yticks(np.arange(0, gameSize, 1))
                    plt.grid(color='b', linestyle='-', zorder=0)
                    ax1.scatter(blkx, blky, s=10, c='k', marker="o", zorder=3)
                    ax1.scatter(whtx, whty, s=10, c='w', marker="o", zorder=3)
                    plt.show()
                
                emptyIndex = np.where(game.getPan() == 0)[0]
                if len(emptyIndex) == 0:
                    print("error is here")
                game.updateStatus()
                if game.isDone() :
                    finished = True
                    break
                    
                
                if player is "both" or player is game.getLastSide():
                    x = int(input("Indicate X coordinate (0 ~ " + str(game.getSize()-1) + ") : "))
                    y = int(input("Indicate Y coordinate (0 ~ " + str(game.getSize()-1) + ") : "))
                elif player is not game.getLastSide(): # when it is AI's turn
                    x = AIsCall[turnsTaken][0]
                    y = AIsCall[turnsTaken][1]
                else : # when both are ai
                    x = AIsCall[turnsTaken][0]
                    y = AIsCall[turnsTaken][1]
                
                plt.close()
                
                doable = game.check(x, y)
                if doable :
                    game.add( x, y, side)
                    game.updateMax()
                    game.updateStatus()
                    turnsTaken += 1
                    sideTaken += 1
                else :
                    pass
                
                if game.isDone() :
                    finished = True
                    break
                if sideTaken > 1 :
                    sideDone = True
                    game.changeSide()
                    gameReal = game.isRealGame()
                    return game, currentRound, finished, gameReal
            game.changeSide()
        
        game.changeSide()
        if graphOn :
            blkx, blky, whtx, whty = returnPan(game.getPan(), game.getSize())
            
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            
            ax1.set_facecolor('grey')
            plt.xlim([-1,gameSize])
            plt.ylim([-1,gameSize])
            plt.xticks(np.arange(0, gameSize, 1))
            plt.yticks(np.arange(0, gameSize, 1))
            plt.grid(color='b', linestyle='-', zorder=0)
            ax1.scatter(blkx, blky, s=10, c='k', marker="o", zorder=3)
            ax1.scatter(whtx, whty, s=10, c='w', marker="o", zorder=3)
            plt.show()
        
        print("Game has finished!")
        if game.isRealGame() :     
            print("The winner is : " + game.getLastSide())
            print("And the winner won by connecting " + str(game.getMax()))
        else : 
            print("draw!")
        
        gameReal = game.isRealGame()
    
    return game, currentRound, finished, gameReal