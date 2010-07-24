from Orders import Orders
import math, sys

BUL_POW = 20
SHIP_POWER = 40
SHIP_FUEL = 10

BULL, SHI1, SHI2 = range(3)

#            SYMB    ID RAD
movables = {"BULL": (0, 1),
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
        self.i, self.radius = movables[what]
        self.parent = None
        
    def Move(self, GAME):
        self.position += self.velocity

    def Write(self):
        print int(self.position.real), int(self.position.imag), int(self.direction), self.radius, self.i

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
        
class Ship(Movable):
    def __init__(self, s, v, d, o, t):
        Movable.__init__(self, s, v, d, "SHI"+t)
        self.direction = d
        self.Order = o
        self.orders = Orders(0, 0, 0, False)
        self.power = SHIP_POWER
        self.fuel = SHIP_FUEL

    def Move(self, GAME):
        self.Recharge()
        
        self.orders = self.Order()
        
        self.direction += self.orders.left
        self.direction -= self.orders.right
        self.Thrust(self.orders.thrust)
        
        Movable.Move(self, GAME)
        self.Fire(GAME, self.orders.fire)

    def Recharge(self):
        self.power += 1

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
