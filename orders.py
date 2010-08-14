class Orders:
    def __init__(self, tu, th, f):
        self.turn = tu
        self.thrust = th
        self.fire = f

DIST, PHASE, ID, VELOCITY, DIRECTION, RADIUS = range(6)

def Order1(sensors):
    my = [m for m in sensors if m[DIST] == 0][0]
    my_team = my[ID]
    your_team = 3 - my_team
    targets = [m for m in sensors if m[ID] == your_team]
    if not targets:
        return Orders(1, .01, 0)
    for target in targets:
        if abs(my[DIRECTION] - target[PHASE]) < 10:
            
            return Orders(0,0,target[DIST])
    return Orders(1, 0, 0)

def Order2(sensors):
    return Orders(0,0,0)

order_list = [Order1, Order2]
