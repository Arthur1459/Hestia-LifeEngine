import config as cf
import vars as vr
import tools as t
import utils as u
import pygame as pg
from Creature import Cell

class Grid:
    def __init__(self, from_Grid=None, size=(cf.grid_size, cf.grid_size)):
        self.id = u.getNewId()

        self.size = size if (from_Grid is None) else from_Grid.size # (lines, rows)
        self.grid = {(row, line): u.IdObj(Cell((line, row))) if (from_Grid is None) else from_Grid.grid[(row, line)] for line in range(self.lines()) for row in range(self.rows())}

        self._to_clear = []
    def update(self):
        vr.next_grid = Grid(size=self.size)  # Reset next_grid for update

        for cell in self.grid:
            try:
                self.grid[cell].obj.update() # update in next_grid
            except AttributeError:
                print(f"## {self.grid[cell].obj.__class__} at {cell} have no 'update' method ! ##")

        vr.grid = Grid(from_Grid=vr.next_grid) # overwrite grid with next_grid in current grid for next step

        #self.draw()
        return

    def draw(self):
        for row, line in self.grid:
            pg.draw.rect(vr.window, 'white', [row * cf.cell_size, line * cf.cell_size, cf.cell_size, cf.cell_size], 1)

    def rows(self):
        return self.size[1]
    def lines(self):
        return self.size[0]
    def putAt(self, obj, pos):
        self.grid[pos] = u.IdObj(obj.id, obj)
    def clearAt(self, pos):
        self.grid[pos] = u.IdObj()
