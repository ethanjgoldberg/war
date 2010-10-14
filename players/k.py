import orders as o # Necessary for Orders class.

import math

from random import randrange

def Order(sensors): # Order should take sensors as argument
    ords = o.Orders(0,0,0)
    
    my = [m for m in sensors if m.dist == 0][0] # Find ship being ordered
    
    my_team = my.id
    your_team = 1 - my_team # Find id of other team
    
    targets = [m for m in sensors if m.id == your_team] # get list of opposing ships
    my_ships = [m for m in sensors if m.id == my_team]
    
    if not targets:
        return o.Orders(0, 0, 0) # No opposing ships = we win!
    
    target = targets[0] # Pick a target at random.
    for t in targets:
        if abs(t.phase) < abs(target.phase): # Find the target closest to my direction.
            target = t 

    #f = open('/tmp/out.txt', 'a')
    #f.write("dist: %d" % t.dist)


    # randomness!
    #     r = randrange(2)
    #     if r is 0 :
    #       ords.turn = -target.phase # Turn towards the target.
    #       if abs(target.phase) < math.degrees(math.asin(float(target.rad) / float(target.dist))):
    #           if my.power * 20 < target.dist:
    #               ords.thrust = max(abs(target.vel), 15) # If we can't shoot 'em, chase 'em.
    #           else:
    #               ords.fire = target.dist / 20 # If we can shoot 'em, do.
    #     else:
    #       ords.turn = randrange(4)-2
    #       ords.thrust = 5
    
    close_ships = [m for m in my_ships if m.dist < 500 and m.dist != 0]
    
    #f.write("dist: %d\n" % len(close_ships))
    if len(close_ships) > 0:
        for s in close_ships: #GET AWAY
            ords.turn += s.phase
            ords.thrust += max(abs(30 - s.dist/10), 5)
    else:
        r = randrange(2)
        if r is 0 :
            ords.turn = -target.phase # Turn towards the target.
            if abs(target.phase) < math.degrees(math.asin(float(target.rad) / float(target.dist))):
                if my.power * 20 < target.dist:
                    ords.thrust = max(abs(target.vel), 15) # If we can't shoot 'em, chase 'em.
                else:
                    ords.fire = target.dist / 20 # If we can shoot 'em, do.
        else:
            ords.turn = randrange(4)-2
            ords.thrust = 5
    
    return ords
