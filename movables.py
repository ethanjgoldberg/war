import orders
import cmath, math
import sensor

BUL_POW = 20
SHIP_POWER = 400
SHIP_FUEL = 100
SHIP_SENSORS = 500
SHIP_TURN = 3

#            SYMB    ID RAD
mo_stats = {"SENS": (-2, 0),
            "BULL": (-1, 1),
            "SHI0": (0, 100),
            "SHI1": (1, 100)}

def ei(x):
    x = math.radians(x)
    return cmath.exp(x*1j)
def roundc(c):
    return round(c.real) + round(c.imag) * 1j
def d(a, b):
    return math.degrees(cmath.phase(a.pos - b.pos)) % 360
def m_polar(m1, m2):
    return (int(m_dist(m1, m2)),
            int(m2.d - d(m1,m2)))
def m_dist(m1, m2):
    return abs(m1.pos - m2.pos)

class Movable:
    def __init__(self, s, v, d, what):
        self.pos = s
        self.vel = v
        self.d = d
        self.i, self.rad = mo_stats[what]
        self.parent = None
        
    def Move(self, GAME):
        self.pos += self.vel

    def Vitals(self, sh):
        if self != sh:
            return m_polar(self, sh) + (self.i, roundc((self.vel - sh.vel) * ei(-sh.d)), int(self.d - sh.d), self.rad, None, None, None)
        else:
            return (0, 0, self.i, 0j, 0, self.rad, int(self.power), int(self.fuel), self.message)

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
        self.Order = o[t]
        self.ords = orders.Orders(0, 0, 0)
        self.power = SHIP_POWER
        self.fuel = SHIP_FUEL
        self.message = {}

    def Move(self, GAME):
        self.Recharge()
        
        self.ords = self.Order(GAME.Sense(self))

        if self.ords.turn > 0:
            self.d += min(self.ords.turn, SHIP_TURN)
        elif self.ords.turn < 0:
            self.d += max(self.ords.turn, -SHIP_TURN)
        self.d %= 360
        self.Thrust(self.ords.thrust)
        
        Movable.Move(self, GAME)
        self.Fire(GAME, self.ords.fire)

        self.message = self.ords.message

    def Recharge(self):
        self.power += 2

    def Thrust(self, t):
        if t <= 0:
            return
        t = min(t, self.fuel)
        self.fuel -= t * 0.01
        self.vel += t * ei(self.d) * 0.01
        
    def Fire(self, GAME, l):
        if l <= 0:
            return
        l = min(l, self.power)
        self.power -= l
        GAME.AddMovable(Bullet(self.pos, self.vel + (BUL_POW * ei(self.d)), l, self))
