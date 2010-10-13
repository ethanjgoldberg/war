import orders as o # Necessary for Orders class.

import math

def Order(sensors): # Order should take sensors as argument
    ords = o.Orders(0,0,0)
    
    my = [m for m in sensors if m.dist == 0][0] # Find ship being ordered
    
    my_team = my.id
    your_team = 1 - my_team # Find id of other team

    targets = [m for m in sensors if m.id == your_team] # get list of opposing ships

    if not targets:
        return o.Orders(0, 0, 0) # No opposing ships = we win!
    
    target = targets[0] # Pick a target at random.
    for t in targets:
        if abs(t.phase) < abs(target.phase): # Find the target closest to my direction.
            target = t 

    ords.turn = -target.phase # Turn towards the target.
    if abs(target.phase) < math.degrees(math.asin(float(target.rad) / float(target.dist))):
        if my.power * 20 < target.dist:
            ords.thrust = max(abs(target.vel), 10) # If we can't shoot 'em, chase 'em.
        else:
            ords.fire = target.dist / 20 # If we can shoot 'em, do.
    
    return ords
