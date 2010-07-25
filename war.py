#!/usr/bin/python

from Game import Game
import Movables as m
from Orders import Orders
import sys

GAME = Game()

def Order():
    return Orders(0, 0, 0, 0)
def Order2():
    return Orders(0, 1, 10, 20)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage:", sys.argv[0], "<outfile>"
        sys.exit()
    with outfile as open(sys.argv[1], 'w'):
        GAME.AddMovable(m.Ship(200 + 200j, 0j, 0, Order, '1'))
        GAME.AddMovable(m.Ship(350 + 350j, 0j, 0, Order2, '2'))
        won = False
        for i in range(500):
            GAME.Write(outfile)
            GAME.Move()
            GAME.Collide()
            winner = GAME.Win()
            if winner and not won:
                outfile.writelines(["> Team ", str(winner), "has won the battle."])
                won = True
