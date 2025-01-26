import config as cf
import vars as vr
import tools as t
import utils as u
import pygame as pg
from Creature import Cell
from Environement import Food

class Grid:
    def __init__(self, from_Grid=None, size=(cf.grid_size, cf.grid_size)):
        self.id = u.getNewId()

        self.size = size if (from_Grid is None) else from_Grid.size # (lines, rows)
        self.grid = {(line, row): NewCell((line, row)) for line in range(self.lines()) for row in range(self.rows())}
        self.add_initial_elements()

        self._to_clear = []
    def update(self):
        for cell_pos in self.grid:
            cell = self.getAt(cell_pos)
            try:
                if cell.variant == cf.BASE:
                    if t.proba(0.01):
                        vr.grid.putAt(Food(cell_pos), cell_pos)
                else:
                    cell.update()
            except AttributeError:
                print(f"## {self.getAt(cell).__class__} at {cell} have no 'update' method ! ##")

        self.draw()
        return

    def add_initial_elements(self):
        for pos in self.grid:
            if t.proba(cf.food_init_percentage):
                self.putAt(Food(pos), pos)

    def draw(self):
        for cell in self.grid:
            self.getAt(cell).draw()

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

