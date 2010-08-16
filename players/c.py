import orders as o

def Order(sensors):
    ords = o.Orders(3,0,0)

    my = [m for m in sensors if m.dist == 0][0]
    y = 3 - my.id
    
    ts = [m for m in sensors if m.id == y and abs(m.phase) < 10]
    if ts:
        ords.fire = ts[0].dist
        ords.turn = 0
    return ords
