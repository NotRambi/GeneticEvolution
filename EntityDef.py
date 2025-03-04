import random
import math

class entity:
    def __init__(self, name, parent, dna, age, x, y):
        self.name = name
        self.parent = parent
        self.dna = dna
        self.age = age
        self.days = 0
        self.alive = True
        self.color = None # rgb (0,255), se uguale tra partner aumenta probabilità di accoppiamento
        self.size = None # da 1 a 3, incide positivamente sulla probabilità di accoppiamento
        self.shape = None # 0 o 1, 0 = quadrato, 1 = cerchio, se diverso tra partner diminuisce probabilità di accoppiamento
        self.x = x
        self.y = y
        self.setColor()
        self.setSize()
        self.setShape()
    
    def getDNA(self):
        return self.dna
    
    def getName(self):
        return self.name
    
    def getParent(self):
        return self.parent
    
    def getAge(self):
        return self.age
    
    def getColor(self):
        return self.color
    
    def getSize(self):
        return self.size
    
    def getShape(self):
        return self.shape
    
    def getPos(self):
        return (self.x, self.y)
    
    def setColor(self):
        self.color = (self.dna[0], self.dna[1], self.dna[2])

    def setSize(self):
        self.size = self.dna[3]
    
    def setShape(self):
        self.shape = self.dna[4]

    def getOlder(self):
        self.days += 1
        if self.days % 365 == 0:
            self.days = 0
            self.age += 1
            probToDie = ((math.e ** (self.age * 0.02)) - 1)/100
            # numero random tra 0 e 1
            randomNum = random.random()
            if randomNum < probToDie:
                self.alive = False
        return self.alive
