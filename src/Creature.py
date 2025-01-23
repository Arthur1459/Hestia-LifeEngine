import config as cf
import vars as vr
import tools as t
import utils as u
import pygame as pg
from utils import keepInGrid, isInGrid
from random import randint

BASE = 0
BODY = 1

class Cell:
    def __init__(self, pos):
        self.id = u.getNewId()
        self.variant = BASE
        self.pos = pos

    def row(self):
        return self.pos[1]
    def line(self):
        return self.pos[0]
    def canMoveToward(self, dir):
        line, row = self.pos
        dline, drow = dir
        target = (line + dline, row + drow)
        if isInGrid(target) and vr.grid.getAt(target).variant == BASE and vr.next_grid.getAt(target).variant == BASE: return True
        else: return False
    def MoveToward(self, dir):
        #vr.next_grid.putAt(u.IdObj(), self.pos)
        pos = self.pos
        self.pos = keepInGrid(t.Vadd(self.pos, dir))
        vr.next_grid.putAt(self, self.pos)
        print(f"{pos} + {dir} = {self.pos}")
    def update(self):
        pass
    def draw(self):
        pg.draw.rect(vr.window, 'white', [self.row() * cf.cell_size + 1, self.line() * cf.cell_size + 1, cf.cell_size - 2, cf.cell_size - 2])

class Body(Cell):
    def __init__(self, pos):
        super().__init__(pos)
        self.variant = BODY
    def update(self):
        dir = (randint(-1, 1), randint(-1, 1))
        if self.canMoveToward(dir): self.MoveToward(dir)
        else: self.MoveToward((0, 0))
    def draw(self):
        x, y, length = self.row() * cf.cell_size + 1, self.line() * cf.cell_size + 1, cf.cell_size - 2
        pg.draw.rect(vr.window, 'blue', [x, y, length, length])
        pg.draw.lines(vr.window, 'black', True, [(x + length/3, y + length/3), (x + 2*length/3, y + 2*length/3), (x + 2*length/3, y + length/3), (x + length/3, y + 2*length/3)], 6)

