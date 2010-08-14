import orders
import math, sys

BUL_POW = 20
SHIP_POWER = 400
SHIP_FUEL = 1000
SHIP_SENSORS = 500

BULL, SHI1, SHI2 = range(3)

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
        self.position = s
        self.velocity = v
        self.direction = d
        self.i, self.radius = mo_stats[what]
        self.parent = None
        
    def Move(self, GAME):
        self.position += self.velocity

    def Vitals(self, dv):
        return (self.i, roundc(self.velocity - dv), self.direction, self.radius)

    def Write(self, f):
        f.writelines([str(int(self.position.real))+' ',
                     str(int(self.position.imag))+' ',
                     str(int(self.direction))+' ',
                     str(self.radius)+' ',
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
        Movable.__init__(self, sh.position, sh.velocity, 0, "SENS")
        self.radius = r
            
class Ship(Movable):
    def __init__(self, s, v, d, t):
        Movable.__init__(self, s, v, d, "SHI"+str(t))
        self.direction = d
        self.Order = orders.order_list[t-1]
        self.ord = orders.Orders(0, 0, 0)
        self.power = SHIP_POWER
        self.fuel = SHIP_FUEL
        self.sensors = SHIP_SENSORS

    def Move(self, GAME):
        self.Recharge()
        
        self.ord = self.Order(GAME.Sense(self, self.sensors))

        self.direction += self.ord.turn
        self.Thrust(self.ord.thrust)
        
        Movable.Move(self, GAME)
        self.Fire(GAME, self.ord.fire)

    def Recharge(self):
        self.power += 10

    def Thrust(self, t):
        if t > self.fuel or t <= 0:
            return
        self.fuel -= t
        self.velocity += t * ei(self.direction)
        
    def Fire(self, GAME, l):
        if l > self.power or l <= 0:
            return
        self.power -= l
        GAME.AddMovable(Bullet(self.position, self.velocity + (BUL_POW * ei(self.direction)), l, self))
