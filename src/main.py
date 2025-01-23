import pygame as pg
import tools as t
import utils as u
import vars as vr
import config as cf
import time

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
        pre_update()
        if vr.pause is False:
            update()
        post_update()
        # --------- #

    return

def update():
    vr.nb_updates += 1
    vr.cursor = pg.mouse.get_pos()

    return

def pre_update():
    vr.window.fill('black')

def post_update():
    if vr.inputs['SPACE'] and u.canKey(): vr.pause = False if vr.pause else True
    u.Text("generation : " + str(vr.nb_updates), (10, vr.win_height - 24), 14, 'orange')
    pg.display.update()
    return

if __name__ == "__main__":
    main()