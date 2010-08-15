from copy import copy
import movables
from cmath import phase
from math import degrees

def m_dist(m1, m2):
    return abs(m1.position - m2.position)

def collide(m1, m2):
    return m1 != m2 and m1 != m2.parent and m1.parent != m2 and m_dist(m1, m2) < m1.radius + m2.radius

def d(a, b):
    return degrees(phase(a.position - b.position)) % 360

def m_polar(m1, m2):
    return (int(m_dist(m1, m2)),
            int(m2.direction - d(m1,m2)))

class Game:
    def __init__(self):
        self.movables = []
        
    def Move(self):
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
        sensed = [m_polar(m, sh) + m.Vitals(sh) for m in self.movables if m.i != 0]
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
