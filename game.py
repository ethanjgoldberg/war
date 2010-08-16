from copy import copy
import movables
from cmath import phase
from math import degrees
import math

def m_dist(m1, m2):
    return abs(m1.pos - m2.pos)

def dot(c1, c2=None):
    if c2 == None:
        return c1.real**2 + c1.imag**2
    return c1.real * c2.real + c1.imag * c2.imag

def plusorminus(a, b):
    return (a+b, a-b)

def collide(m1, m2):
    if m1 == m2 or m1 == m2.parent or m1.parent == m2:
        return False

    vab = m2.vel - m1.vel
    rab = m1.rad + m2.rad
    ab = m2.pos - m1.pos

    c = dot(ab) - rab*rab
    if c <= 0:
        print ab, dot(ab)
        return True

    a = dot(vab)
    b = 2*dot(vab, ab)

    disc = b*b - 4*a*c

    if disc < 0:
        return False

    if not a:
        return False
    bova = b / (2*a)
    sq = math.sqrt(disc)
    sqova = sq / (2*a)
    t = plusorminus(bova, sqova)

    ret = 0 < t[0] < 1 or 0 < t[1] < 1
    """if ret:
        print m1.Vitals(0j)
        print m2.Vitals(0j)
        print "vab:\t", vab
        print "rab:\t", rab
        print "ab:\t", ab
        print "a:\t", a
        print "b:\t", b
        print "c:\t", c
        print "disc:\t", disc
        print "t:\t", t
        print"""

    return ret

def d(a, b):
    return degrees(phase(a.pos - b.pos)) % 360

def m_polar(m1, m2):
    return (int(m_dist(m1, m2)),
            int(m2.d - d(m1,m2)))

class Sensor:
    def __init__(self, d, p, i, v, di, r, po, f):
        self.dist = d
        self.phase = p
        self.id = i
        self.vel = v
        self.d = di
        self.rad = r
        self.power = po
        self.fuel = f

class Game:
    def __init__(self):
        self.movables = []
        self.turn = 0

    def Setup(self, f, o):
        self.order_list = o
        with open(f, 'r') as setupfile:
            for line in setupfile.readlines():
                if line[0] == '\n':
                    pass
                elif line[0] == '#':
                    pass
                else:
                    self.AddMovable(apply(movables.Ship, [eval(x) for x in line.split()]+[self.order_list]))
    
    def Move(self):
        self.turn += 1
        for m in self.movables:
            m.Move(self)

    def Collide(self):
        mo = copy(self.movables)
        for n in mo:
            for m in mo:
                if collide(m, n):
                    try:
                        mo.remove(m)
                        mo.remove(n)
                    except ValueError:
                        pass
        self.movables = mo

    def Sense(self, sh, dist):
        t = movables.Sensors(sh, dist)
        sensed = [apply(Sensor, m_polar(m, sh) + m.Vitals(sh.vel)) for m in self.movables if m.i != 0]
        return sensed

    def AddMovable(self, m):
        self.movables.append(m)

    def Count(self, what):
        return len([m for m in self.movables if m.i == what])
    
    def Win(self):
        t1 = self.Count(1)
        t2 = self.Count(2)
        if t1 or t2:
            if not t2:
                return 1
            if not t1:
                return 2
        else:
            return 0
        
    def Write(self, f):
        f.write("\n")
        for m in self.movables:
            m.Write(f)
