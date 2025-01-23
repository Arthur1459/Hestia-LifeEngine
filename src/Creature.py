import config as cf
import vars as vr
import tools as t
import utils as u
import pygame as pg
from utils import keepInGrid, isInGrid
from random import randint

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
        for child in self.children:
            child.MoveToward(dir)
        vr.grid.clearAt(self.pos)
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
        hand = Arm(t.Vadd(arm.pos, (1, 0)), arm) # TEST
        fingers_children = [Arm(t.Vadd(hand.pos, (1, 0)), hand), Arm(t.Vadd(hand.pos, (0, 1)), hand), Arm(t.Vadd(hand.pos, (0, -1)), hand)]
        arm.children.append(hand)  # TEST
        hand.children = fingers_children
        self.children = [arm] # Arm(t.Vadd(pos, (0, 1)), self), Arm(t.Vadd(pos, (-1, 0)), self), Arm(t.Vadd(pos, (0, -1)), self)
    def update(self):
        direction = self.getDirection()
        if self.canMoveToward(direction): self.MoveToward(direction)
        else: self.MoveToward((0, 0))
    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, 'blue', [x, y, length, length])
        pg.draw.lines(vr.window, 'black', True, [(x + length/3, y + length/3), (x + 2*length/3, y + 2*length/3), (x + 2*length/3, y + length/3), (x + length/3, y + 2*length/3)], 6)
    def getDirection(self):
        direction = (0, 0)
        dir_choice = randint(-1, 1)
        if dir_choice == -1:
            direction = (randint(-1, 1), 0)
        elif dir_choice == 1:
            direction = (0, randint(-1, 1))
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
