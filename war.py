#!/usr/bin/python

from game import Game
import movables as mo
import sys

GAME = Game()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage:", sys.argv[0], "<setupfile> <outfile>"
        sys.exit()
    with open(sys.argv[1], 'r') as setupfile:
        for line in setupfile.readlines():
            if line[0] == '\n':
                pass
            elif line[0] == '#':
                pass
            else:
                GAME.AddMovable(apply(mo.Ship, [eval(x) for x in line.split()]))
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
