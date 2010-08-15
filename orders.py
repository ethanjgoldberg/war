import math

class Orders:
    def __init__(self, tu, th, f):
        self.turn = tu
        self.thrust = th
        self.fire = f

DIST, PHASE, ID, VELOCITY, DIRECTION, RADIUS, POWER, FUEL = range(8)

def Order1(sensors):
    ords = Orders(0,0,0)
    my = [m for m in sensors if m[DIST] == 0][0]
    
    my_team = my[ID]
    your_team = 3 - my_team
    
    targets = [m for m in sensors if m[ID] == your_team]
    
    if not targets:
        return Orders(0, 0, 0)
    
    target = targets[0]
    for t in targets:
        if abs(t[PHASE]) < abs(target[PHASE]):
            target = t

    ords.turn = -target[PHASE]
    ords.thrust = (my[POWER] < target[DIST] and abs(target[PHASE]) < 10) * max(abs(target[VELOCITY]), 10)
    ords.fire = (my[POWER] >= target[DIST] and abs(target[PHASE]) < 10) * target[DIST] / 20
    return ords
    
def Order2(sensors):
    ords = Orders(1,0,0)

    my = [m for m in sensors if m[DIST] == 0][0]
    y = 3 - my[ID]
    
    ts = [m for m in sensors if m[ID] == y and abs(m[PHASE]) < 10]
    if ts:
        ords.fire = ts[0][DIST]
        ords.turn = 0
    return ords

order_list = [Order1, Order2]
