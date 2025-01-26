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

    return

def main():
    init()

    vr.running = True

    while vr.running:

        u.resetInputs()
        while time.time() - vr.t < cf.update_rate:
            pass
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
    u.getInputs()
    if vr.inputs['ESC']: vr.running = False
    if vr.inputs['SPACE'] and u.canKey(): vr.pause = False if vr.pause else True
    if vr.inputs['H'] and u.canKey(): cf.highlight_creatures = False if cf.highlight_creatures else True

    if vr.inputs['S'] and u.canKey(): cf.food_moving_lost = round(max(0., cf.food_moving_lost + 0.1), 1)
    if vr.inputs['X'] and u.canKey(): cf.food_moving_lost = round(max(0., cf.food_moving_lost - 0.1), 1)

    if vr.inputs['D'] and u.canKey(): cf.food_general_lost = round(max(0., cf.food_general_lost + 0.1), 1)
    if vr.inputs['C'] and u.canKey(): cf.food_general_lost = round(max(0., cf.food_general_lost - 0.1), 1)

    if vr.inputs['F'] and u.canKey(): cf.food_grow_proba = round(max(0., cf.food_grow_proba + 0.1), 1)
    if vr.inputs['V'] and u.canKey(): cf.food_grow_proba = round(max(0., cf.food_grow_proba - 0.1), 1)

def always_do_post():
    pg.draw.rect(vr.window, 'black', [0, vr.win_height - 20, vr.win_width, 20])
    u.Text("Generation " + str(vr.nb_updates), (8, vr.win_height - 18), 14, 'orange' if vr.pause else 'green')
    u.Text("Bodies " + str(vr.nb_bodies), (140, vr.win_height - 18), 14, (0, 70, 250))

    u.Text("loss : move= " + str(cf.food_moving_lost) + " | general= " + str(cf.food_general_lost), (220, vr.win_height - 18), 14, (150, 200, 0))
    u.Text("food spread : " + str(cf.food_grow_proba), (500, vr.win_height - 18), 14, (10, 100, 0))

if __name__ == "__main__":
    main()