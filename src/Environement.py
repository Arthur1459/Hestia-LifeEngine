import config as cf
import vars as vr
import tools as t
import utils as u
import pygame as pg
from utils import keepInGrid, isInGrid

class Food:
    def __init__(self, pos):
        self.id = u.getNewId()

        self.variant = cf.FOOD
        self.pos = tuple(pos)
        self.food = 2

    def update(self):
        if t.proba(1):
            potential_pos = [t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (1, 0)),
                             t.Vadd(self.pos, (-1, 0))]
            t.shuffle(potential_pos)
            for pos in potential_pos:
                if isInGrid(pos) and vr.grid.getAt(tuple(pos)).variant == cf.BASE:
                    vr.grid.putAt(Food(pos), tuple(pos))
                    break

    def draw(self):
        pg.draw.rect(vr.window, (10, 150, 0), [self.pos[1] * cf.cell_size, self.pos[0] * cf.cell_size, cf.cell_size, cf.cell_size])

