import orders as o

import math

def Order(sensors):
    my = [m for m in sensors if m.dist == 0][0]
    y = 3 - my.id

    ords = o.Orders(3,0,0)
    
    ts = [m for m in sensors if m.id == y and abs(m.phase) < math.degrees(math.asin(float(m.rad) / float(m.dist)))]
    return ords
