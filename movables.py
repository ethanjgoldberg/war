import orders
import math, sys

BUL_POW = 20
SHIP_POWER = 400
SHIP_FUEL = 100
SHIP_SENSORS = 500
SHIP_TURN = 3

#            SYMB    ID RAD
mo_stats = {"SENS": (-1, 0),
            "BULL": (0, 1),
            "SHI1": (1, 100),
            "SHI2": (2, 100)}

def ei(x):
    x = math.radians(x)
    return math.cos(x) + (math.sin(x) * 1j)
def roundc(c):
    return round(c.real) + round(c.imag) * 1j

class Movable:
    def __init__(self, s, v, d, what):
        self.pos = s
        self.vel = v
        self.d = d
        self.i, self.rad = mo_stats[what]
        self.parent = None
        
    def Move(self, GAME):
        self.pos += self.vel

    def Vitals(self, dv):
        return (self.i, roundc(self.vel - dv), int(self.d), self.rad, int(self.power), int(self.fuel))

    def Write(self, f):
        f.writelines([str(int(self.pos.real))+' ',
                     str(int(self.pos.imag))+' ',
                     str(int(self.d))+' ',
                     str(self.rad)+' ',
                     str(self.i)+'\n'])

class Bullet(Movable):
    def __init__(self, s, v, l, p):
        Movable.__init__(self, s, v, 0, "BULL")
        self.life = l
        self.parent = p

    def Move(self, GAME):
        Movable.Move(self, GAME)
        self.life -= 1
        if not self.life:
            GAME.movables.remove(self)

class Sensors(Movable):
    def __init__(self, sh, r):
        Movable.__init__(self, sh.pos, sh.vel, 0, "SENS")
        self.rad = r
            
class Ship(Movable):
    def __init__(self, s, v, d, t, o):
        Movable.__init__(self, s, v, d, "SHI"+str(t))
        self.d = d
        self.Order = o[t-1]
        self.ords = orders.Orders(0, 0, 0)
        self.power = SHIP_POWER
        self.fuel = SHIP_FUEL
        self.sensors = SHIP_SENSORS

    def Move(self, GAME):
        self.Recharge()
        
        self.ords = self.Order(GAME.Sense(self, self.sensors))

        if self.ords.turn > 0:
            self.d += min(self.ords.turn, SHIP_TURN)
        elif self.ords.turn < 0:
            self.d += max(self.ords.turn, -SHIP_TURN)
        self.d %= 360
        self.Thrust(self.ords.thrust)
        
        Movable.Move(self, GAME)
        self.Fire(GAME, self.ords.fire)

    def Recharge(self):
        self.power += 2

    def Thrust(self, t):
        if t > self.fuel or t <= 0:
            return
        self.fuel -= t * 0.01
        self.vel += t * ei(self.d) * 0.01
        
    def Fire(self, GAME, l):
        if l > self.power or l <= 0:
            return
        self.power -= l
        GAME.AddMovable(Bullet(self.pos, self.vel + (BUL_POW * ei(self.d)), l, self))
