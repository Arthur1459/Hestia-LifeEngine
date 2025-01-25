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
    def __init__(self, pos, body_id=None):
        self.id = u.getNewId()
        self.variant = BASE
        self.alive = True
        self.pos = tuple(pos)
        self.children, self.dead_children = [], []
        self.father = None
        self.body_id = body_id

    def row(self):
        return self.pos[1]
    def line(self):
        return self.pos[0]
    def canMoveToward(self, dir):
        line, row = self.pos
        dline, drow = dir
        target = (line + dline, row + drow)
        if isInGrid(target) and (vr.grid.getAt(target).variant == BASE or vr.grid.getAt(target).body_id == self.body_id) and all([child.canMoveToward(dir) for child in self.children]): return True
        else: return False
    def MoveToward(self, dir):
        vr.grid.clearAt(self.pos)
        for child in self.children:
            child.MoveToward(dir)
        self.pos = keepInGrid(t.Vadd(self.pos, dir))
        if self.alive:
            vr.grid.putAt(self, self.pos)

    def die(self):
        for child in self.children:
            child.die()
        self.father.dead_children.append(self)
        self.alive = False

    def update(self):
        for dead_children in self.dead_children:
            try:
                self.children.remove(dead_children)
            except:
                pass
        self.dead_children = []

    def draw(self):
        pg.draw.rect(vr.window, 'white', [self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size, cf.cell_size])

class Body(Cell):
    def __init__(self, pos):
        super().__init__(pos)
        self.variant = BODY
        self.body_id = self.id

        arm = Arm(t.Vadd(pos, (1, 0)), self, self.body_id) # TEST
        self.children = [arm] # Arm(t.Vadd(pos, (0, 1)), self), Arm(t.Vadd(pos, (-1, 0)), self), Arm(t.Vadd(pos, (0, -1)), self)

        self.brain = NeuralNetwork(2, 2, (4,))

    def update(self):
        super().update()
        self.evolve()
        direction = self.getDirection()
        if self.canMoveToward(direction): self.MoveToward(direction)
        else: self.MoveToward((0, 0))

    def evolve(self):
        self.brain.Mutate()
        for child in self.children:
            child.evolve()
        can_arm, pos_arm = self.canGenerateArm()
        if can_arm and t.proba(1):
            self.children.append(Arm(pos_arm, self, self.body_id))

    def canGenerateArm(self):
        potential_pos = [t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (1, 0)), t.Vadd(self.pos, (-1, 0))]
        t.shuffle(potential_pos)
        for pos in potential_pos:
            if isInGrid(pos) and vr.grid.getAt(tuple(pos)).variant == BASE:
                return True, tuple(pos)
        return False, None

    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, 'blue', [x, y, length, length])
    def getDirection(self):
        decision = self.brain.predict((self.pos[0] % (1 + self.pos[1]), self.pos[1] / (1 + self.pos[0])))
        direction = (0, 0)
        threshold = 0.1
        if decision[0] > threshold and abs(decision[1]) < threshold :
            direction = (1, 0)
        elif decision[0] < -threshold and abs(decision[1]) < threshold :
            direction = (-1, 0)
        elif decision[1] > threshold and abs(decision[0]) < threshold :
            direction = (0, 1)
        elif decision[1] < -threshold and abs(decision[0]) < threshold :
            direction = (0, -1)
        return direction

class Arm(Cell):
    def __init__(self, pos, father, body_id):
        super().__init__(pos)
        self.variant = ARM
        self.father = father
        self.body_id = body_id
    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, 'grey', [x, y, length, length])
    def evolve(self):
        if t.proba(0.8 * (t.inv(1 + len(self.children)) ** 2)):
            self.die()
            return
        for child in self.children:
            child.evolve()
        can_grow, pos_grow = self.canGrow()
        if can_grow and t.proba(1):
            self.children.append(Arm(pos_grow, self, self.body_id))

    def canGrow(self):
        potential_pos = [t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (1, 0)), t.Vadd(self.pos, (-1, 0))]
        t.shuffle(potential_pos)
        for pos in potential_pos:
            if isInGrid(pos) and vr.grid.getAt(tuple(pos)).variant == BASE:
                return True, tuple(pos)
        return False, None
