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
        self.food = cf.life_amount_per_food

    def update(self):
        if t.proba(cf.food_grow_proba):
            potential_pos = [t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (1, 0)),
                             t.Vadd(self.pos, (-1, 0))]
            t.shuffle(potential_pos)
            for pos in potential_pos:
                if isInGrid(pos) and vr.grid.getAt(tuple(pos)).variant == cf.BASE:
                    vr.grid.putAt(Food(pos), tuple(pos))
                    break

    def draw(self):
        pg.draw.rect(vr.window, cf.food_color, [self.pos[1] * cf.cell_size, self.pos[0] * cf.cell_size, cf.cell_size, cf.cell_size])

class Wall:
    def __init__(self, pos):
        self.id = u.getNewId()

        self.variant = cf.WALL
        self.pos = tuple(pos)
        self.food = 2

    def update(self):
        pass

    def draw(self):
        pg.draw.rect(vr.window, (50, 50, 50), [self.pos[1] * cf.cell_size, self.pos[0] * cf.cell_size, cf.cell_size, cf.cell_size])

