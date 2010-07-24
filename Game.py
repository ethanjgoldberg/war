from copy import copy

def collide(m1, m2):
    return m1 != m2 and m1 != m2.parent and m1.parent != m2 and abs(m1.position - m2.position) < m1.radius + m2.radius

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