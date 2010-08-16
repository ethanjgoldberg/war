#!/usr/bin/python

from game import Game
import movables as mo
import sys

from players import *

GAME = Game()

order_list = [e.Order,e.Order]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage:", sys.argv[0], "<setupfile> <outfile>"
        sys.exit()
        
    GAME.Setup(sys.argv[1], order_list)
    
    with open(sys.argv[2], 'w') as outfile:
        won = False
        for i in range(2000):
            GAME.Write(outfile)
            GAME.Move()
            GAME.Collide()
            winner = GAME.Win()
            if winner and not won:
                outfile.writelines(["> Team ", str(winner), " has won the battle."])
                won = True
