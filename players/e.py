import orders as o

def Order(sensors):
    ords = o.Orders(0,0,0)
    my = [m for m in sensors if m.dist == 0][0]
    
    my_team = my.id
    your_team = 3 - my_team
    
    targets = [m for m in sensors if m.id == your_team]
    
    if not targets:
        return o.Orders(0, 0, 0)
    
    target = targets[0]
    for t in targets:
        if abs(t.phase) < abs(target.phase):
            target = t

    ords.turn = -target.phase
    ords.thrust = (my.power < target.dist and abs(target.phase) < 10) * max(abs(target.vel), 10)
    ords.fire = (my.power >= target.dist and abs(target.phase) < 10) * target.dist / 20
    return ords
