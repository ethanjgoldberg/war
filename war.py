#!/usr/bin/python

from Game import Game
import Movables as mo
from Movables import movables
from Orders import Orders
import sys

GAME = Game()

DIST, PHASE, ID, VELOCITY, DIRECTION, RADIUS = range(6)

def Order(sensors):
    print sensors
    my = [m for m in sensors if m[DIST] == 0][0]
    my_team = my[ID]
    your_team = 3 - my_team
    try:
        target = [m for m in sensors if m[ID] == your_team][0]
    except:
        return Orders(1, 0, .01, 0)
    if abs(my[DIRECTION] - target[PHASE]) < 10:
        return Orders(0,0,0,target[DIST])
    return Orders(0, 1, 0, 0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage:", sys.argv[0], "<outfile>"
        sys.exit()
    with open(sys.argv[1], 'w') as outfile:
        GAME.AddMovable(mo.Ship(-100 + -100j, 0j, 0, Order, '1'))
        GAME.AddMovable(mo.Ship(100 + 100j, 0j, 0, Order, '2'))
        won = False
        for i in range(500):
            GAME.Write(outfile)
            GAME.Move()
            GAME.Collide()
            winner = GAME.Win()
            if winner and not won:
                outfile.writelines(["> Team ", str(winner), " has won the battle."])
                won = True
