import pygame as pg
import tools as t
import utils as u
import vars as vr
import config as cf
import time
from Grid import Grid, GridPrint
from Creature import Cell, Body

def init():

    pg.init()
    pg.display.set_caption(cf.game_name)

    # screen initialisation
    if not cf.fullscreen:
        vr.window = pg.display.set_mode(vr.window_size)
    else:
        vr.window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        vr.window_size = vr.window.get_size()

    u.initInputs()

    vr.grid = Grid()

    test_cell1 = Body((5, 5))
    test_cell2 = Body((2, 4))
    test_cell3 = Body((7, 8))
    vr.grid.putAt(test_cell1, test_cell1.pos)
    vr.grid.putAt(test_cell2, test_cell2.pos)
    vr.grid.putAt(test_cell3, test_cell3.pos)

    return

def main():
    init()

    vr.running = True

    while vr.running:

        u.resetInputs()
        while time.time() - vr.t < cf.update_rate:
            u.getInputs()
        vr.t = time.time()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                vr.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                print("Cursor : ", pg.mouse.get_pos())

        # Main Loop #
        #GridPrint(vr.grid)
        always_do_pre()
        if vr.pause is False:
            update()
        always_do_post()
        pg.display.update()
        # --------- #

    return

def update():
    pre_update()

    vr.grid.update()

    post_update()
    return

def pre_update():
    vr.nb_updates += 1
    vr.cursor = pg.mouse.get_pos()
    vr.window.fill('black')

def post_update():
    return

def always_do_pre():
    if vr.inputs['ESC']: vr.running = False
    if vr.inputs['SPACE'] and u.canKey(): vr.pause = False if vr.pause else True

def always_do_post():
    pg.draw.rect(vr.window, 'black', [0, vr.win_height - 20, vr.win_width, 20])
    u.Text("Generation " + str(vr.nb_updates), (10, vr.win_height - 18), 14, 'orange' if vr.pause else 'green')

if __name__ == "__main__":
    main()