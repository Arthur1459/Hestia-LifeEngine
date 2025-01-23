import config as cf
import vars as vr
import tools as t
import utils as u
import pygame as pg

BASE = 'base'

class Cell:
    def __init__(self, pos):
        self.id = u.getNewId()
        self.variant = BASE
        self.pos = pos

    def row(self):
        return self.pos[1]
    def line(self):
        return self.pos[0]
    def update(self):
        self.draw()
    def draw(self):
        pg.draw.rect(vr.window, 'white', [self.row() * cf.cell_size + 1, self.line() * cf.cell_size + 1, cf.cell_size - 2, cf.cell_size - 2])
