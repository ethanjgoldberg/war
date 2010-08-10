#!/usr/bin/python

from Game import Game
import Movables as m
from Orders import Orders
import sys

GAME = Game()

def Order(sensors):
    print sensors
    my = [m for m in sensors if m[0][0] == 0][0][1]
    if my[2] == 20:
        return Orders(0,0,0,0)
    return Orders(0, 1, 0, 0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage:", sys.argv[0], "<outfile>"
        sys.exit()
    with open(sys.argv[1], 'w') as outfile:
        GAME.AddMovable(m.Ship(-100 + -100j, 0j, 0, Order, '1'))
        GAME.AddMovable(m.Ship(100 + 100j, 0j, 0, Order, '2'))
        won = False
        for i in range(500):
            GAME.Write(outfile)
            GAME.Move()
            GAME.Collide()
            winner = GAME.Win()
            if winner and not won:
                outfile.writelines(["> Team ", str(winner), " has won the battle."])
                won = True
