from copy import copy
import Movables
from cmath import phase
from math import degrees

def m_dist(m1, m2):
    return abs(m1.position - m2.position)

def collide(m1, m2):
    return m1 != m2 and m1 != m2.parent and m1.parent != m2 and m_dist(m1, m2) < m1.radius + m2.radius

def m_polar(m1, m2):
    return (int(m_dist(m1, m2)), int(degrees(phase(m1.position - m2.position))) % 360)

class Game:
    def __init__(self):
        self.movables = []
        
    def Move(self):
        for m in self.movables:
            m.Move(self)

    def Collide(self):
        mo = copy(self.movables)
        for n in self.movables:
            for m in self.movables:
                if collide(m, n):
                    mo.remove(m)
        self.movables = mo

    def Sense(self, pos, dist):
        t = Movables.Sensors(pos, dist)
        sensed = [m_polar(m, t) + m.Vitals() for m in self.movables if m.id != 0 and collide(m, t)]
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
