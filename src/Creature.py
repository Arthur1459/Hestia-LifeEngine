import config as cf
import vars as vr
import tools as t
import utils as u
import pygame as pg
from utils import keepInGrid, isInGrid
from random import randint
from Brain import NeuralNetwork

BASE = 0
BODY = 1
ARM = 2

class Cell:
    def __init__(self, pos):
        self.id = u.getNewId()
        self.variant = BASE
        self.pos = tuple(pos)
        self.children = []
        self.father = None

    def row(self):
        return self.pos[1]
    def line(self):
        return self.pos[0]
    def canMoveToward(self, dir):
        line, row = self.pos
        dline, drow = dir
        target = (line + dline, row + drow)
        if isInGrid(target) and (vr.grid.getAt(target).variant == BASE or vr.grid.getAt(target) == self.father or (vr.grid.getAt(target) in self.children)) and all([child.canMoveToward(dir) for child in self.children]): return True
        else: return False
    def MoveToward(self, dir):
        vr.grid.clearAt(self.pos)
        for child in self.children:
            child.MoveToward(dir)
        self.pos = keepInGrid(t.Vadd(self.pos, dir))
        vr.grid.putAt(self, self.pos)
    def update(self):
        pass
    def draw(self):
        pg.draw.rect(vr.window, 'white', [self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size, cf.cell_size])

class Body(Cell):
    def __init__(self, pos):
        super().__init__(pos)
        self.variant = BODY

        arm = Arm(t.Vadd(pos, (1, 0)), self) # TEST
        self.children = [arm] # Arm(t.Vadd(pos, (0, 1)), self), Arm(t.Vadd(pos, (-1, 0)), self), Arm(t.Vadd(pos, (0, -1)), self)

        self.brain = NeuralNetwork(2, 2, ())

    def update(self):
        self.brain.Mutate()
        direction = self.getDirection()
        if self.canMoveToward(direction): self.MoveToward(direction)
        else: self.MoveToward((0, 0))
    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, 'blue', [x, y, length, length])
        pg.draw.lines(vr.window, 'black', True, [(x + length/3, y + length/3), (x + 2*length/3, y + 2*length/3), (x + 2*length/3, y + length/3), (x + length/3, y + 2*length/3)], 6)
    def getDirection(self):
        decision = self.brain.predict((self.pos[0] % (1 + self.pos[1]), self.pos[1] / (1 + self.pos[0])))
        direction = (0, 0)
        if decision[0] > 1 and abs(decision[1]) < 1 :
            direction = (1, 0)
        elif decision[0] < -1 and abs(decision[1]) < 1 :
            direction = (-1, 0)
        elif decision[1] > 1 and abs(decision[0]) < 1 :
            direction = (0, 1)
        elif decision[1] < -1 and abs(decision[0]) < 1 :
            direction = (0, -1)
        return direction

class Arm(Cell):
    def __init__(self, pos, father):
        super().__init__(pos)
        self.variant = ARM
        self.father = father
    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, 'grey', [x, y, length, length])
        pg.draw.circle(vr.window, 'black', [x + length/2, y + length/2], cf.cell_size/4, 5)
