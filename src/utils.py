import os
import sys

import pygame as pg

import vars as vr


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def Text(msg, coord, size, color):  # blit to the screen a text
    TextColor = pg.Color(color) # set the color of the text
    font = pg.font.Font(resource_path("rsc/pixel.ttf"), size)  # set the font
    return vr.window.blit(font.render(msg, True, TextColor), coord)  # return and blit the text on the screen

def initInputs():
    resetInputs()
    vr.inputs["SPACE"] = False
    vr.inputs["ESC"] = False

def getInputs():
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE] : vr.inputs["SPACE"] = True
    if keys[pg.K_ESCAPE]: vr.inputs["ESC"] = True

def resetInputs():
    vr.inputs = {key: False for key in vr.inputs}

def canKey(dt=0.2):
    if vr.t - vr.t_key > dt:
        vr.t_key = vr.t
        return True
    return False

def isInWindow(coord):
    if 0 <= coord[0] <= vr.win_width:
        if 0 <= coord[1] <= vr.win_height:
            return True
    return False

def makeSeg(a, b):
    return lambda t: (b[0] + (t - 1) * (b[0] - a[0]), b[1] + (t - 1) * (b[1] - a[1]))

def cross_product(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def drawSeg(seg):
    pg.draw.line(vr.window, (20, 20, 100), seg(0), seg(1), 4)

def getNewId():
    vr.id += 1
    return vr.id

class IdObj:
    def __init__(self, obj=None):
        self.Id = obj.id
        self.obj = obj
