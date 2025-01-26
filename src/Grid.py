import config as cf
import vars as vr
import tools as t
import utils as u
import pygame as pg
from Creature import Cell, Body
from Environement import Food, Wall

class Grid:
    def __init__(self, from_Grid=None, size=(cf.grid_size, cf.grid_size)):
        self.id = u.getNewId()

        self.size = size if (from_Grid is None) else from_Grid.size # (lines, rows)
        self.grid = {(line, row): NewCell((line, row)) for line in range(self.lines()) for row in range(self.rows())}
        self.add_initial_elements()

        self._to_clear = []
    def update(self):
        nb_bodies = 0
        vr.id_updated = {}
        for cell_pos in self.grid:
            cell = self.getAt(cell_pos)
            if cell.id in vr.id_updated: continue
            else: vr.id_updated[cell.id] = True
            try:
                if cell.variant == cf.BASE:
                    if t.proba(0.005):
                        vr.grid.putAt(Food(cell_pos), cell_pos)
                elif t.proba(0.005) and vr.nb_bodies < cf.nb_creatures_treshold and cell.variant in cf.CAN_MOVE_ON:
                    vr.grid.putAt(Body(cell_pos), cell_pos)
                else:
                    cell.update()
                    if cell.variant == cf.BODY: nb_bodies += 1
            except AttributeError:
                print(f"## ERROR during updating {self.getAt(cell_pos).__class__} at {cell_pos} ! ##")
        vr.nb_bodies = nb_bodies
        self.draw()
        return

    def add_initial_elements(self):
        for pos in self.grid:
            if t.proba(cf.food_init_percentage):
                self.putAt(Food(pos), pos)
        for line in range(self.lines()):
            self.putAt(Wall((line, 0)), (line, 0))
            self.putAt(Wall((line, self.rows() - 1)), (line, self.rows() - 1))
        for row in range(self.rows()):
            self.putAt(Wall((0, row)), (0, row))
            self.putAt(Wall((self.lines() - 1, row)), (self.lines() - 1, row))

        middle_row = self.rows()//2
        middle_line = self.lines()//2
        half_gap = 2
        for line in range(0, middle_line - half_gap):
            self.putAt(Wall((line, middle_row)), (line, middle_row))
        for line in range(middle_line + 2*half_gap, self.lines()):
            self.putAt(Wall((line, middle_row)), (line, middle_row))
        for row in range(0, middle_row - half_gap):
            self.putAt(Wall((middle_line, row)), (middle_line, row))
        for row in range(middle_row + 2*half_gap, self.rows()):
            self.putAt(Wall((middle_line, row)), (middle_line, row))

    def draw(self):
        for cell_pos in self.grid:
            cell = self.getAt(cell_pos)
            cell.draw()
            if cf.highlight_creatures:
                if cell.variant in cf.BELONG_CREATURE:
                    pg.draw.rect(vr.window, vr.creatures[cell.body_id], [cell.row() * cf.cell_size, cell.line() * cf.cell_size, cf.cell_size, cf.cell_size])

    def rows(self):
        return self.size[1]
    def lines(self):
        return self.size[0]
    def putAt(self, obj, pos):
        self.grid[pos] = {obj.id: obj}
    def clearAt(self, pos):
        self.grid[pos] = NewCell(pos)
    def getAt(self, pos):
        return self.grid[pos][next(iter(self.grid[pos]))]

def NewCell(pos):
    cell = Cell(pos)
    return {cell.id: cell}

def GridPrint(grid):
    print({pos: grid.grid[pos].__class__ for pos in grid.grid})

