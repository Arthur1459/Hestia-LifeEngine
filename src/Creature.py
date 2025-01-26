import config as cf
import vars as vr
import tools as t
import utils as u
import pygame as pg
from utils import keepInGrid, isInGrid
from Brain import NeuralNetwork

class Cell:
    def __init__(self, pos, body_id=None):
        self.id = u.getNewId()
        self.variant = cf.BASE
        self.alive, self.life = True, 100
        self.pos = tuple(pos)
        self.children = []
        self.father = None
        self.body_id = body_id

    def row(self):
        return self.pos[1]
    def line(self):
        return self.pos[0]
    def canMoveToward(self, dir):
        line, row = self.pos
        dline, drow = dir
        target = (line + dline, row + drow)
        if isInGrid(target) and (vr.grid.getAt(target).variant in (cf.BASE, cf.FOOD) or vr.grid.getAt(target).body_id == self.body_id) and all([child.canMoveToward(dir) for child in self.children]): return True
        else: return False
    def MoveToward(self, dir):
        vr.grid.clearAt(self.pos)

        if self.alive:
            self.pos = keepInGrid(t.Vadd(self.pos, dir))
            for child in self.children:
                child.MoveToward(dir)

            self.life += -1
            if vr.grid.getAt(self.pos).variant == cf.FOOD:
                self.life += vr.grid.getAt(self.pos).food

            vr.grid.putAt(self, self.pos)

    def die(self):
        self.alive = False
        if self.father is not None: self.father.children.remove(self)
        vr.grid.clearAt(self.pos)
        for child in self.children:
            child.die()

    def update(self):
        if self.life <= 0 and self.alive:
            self.die()

    def draw(self):
        pg.draw.rect(vr.window, 'white', [self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size, cf.cell_size])
    def getGlobalLife(self, mean=False):
        life_tot = self.life
        for child in self.children:
            life_tot += child.getGlobalLife()
        return life_tot if mean is False else life_tot * t.inv(1 + self.getNbTotalChildren())
    def getNbTotalChildren(self):
        nb_child = len(self.children)
        for child in self.children:
            nb_child += child.getNbTotalChildren()
        return nb_child

class Body(Cell):
    def __init__(self, pos, genetic=None):
        super().__init__(pos)
        self.variant = cf.BODY
        self.body_id = self.id

        if genetic is None:
            self.motricity_brain = NeuralNetwork(2, 3, (4,))
            self.behavior_brain = NeuralNetwork(2, 6, (3,))
        else:
            self.motricity_brain = NeuralNetwork(copy_from=genetic['motricity'])
            self.behavior_brain = NeuralNetwork(copy_from=genetic['behavior'])

    def update(self):
        super().update()
        for child in self.children:
            child.update()

        behavior_input = (self.getGlobalLife(mean=True), self.getNbTotalChildren())
        reproduce_treshold, reproduce_decision, grow_decision, grow_treshold, grow_type_decision, grow_type_treshold = self.behavior_brain.predict(behavior_input)

        can_arm, pos_arm = self.canGenerateArm()
        if can_arm and t.proba(1):
            self.children.append(Arm(pos_arm, self, self.body_id))

        can_reproduce, reproduce_pos = self.canReproduce()
        if can_reproduce and reproduce_decision > reproduce_treshold:
            self.life = self.life * 0.8
            new_born = Body(reproduce_pos, genetic={'motricity': self.motricity_brain, 'behavior': self.behavior_brain})
            new_born.motricity_brain.Mutate()
            new_born.behavior_brain.Mutate()
            new_born.life = self.life
            vr.grid.putAt(new_born, reproduce_pos)

        if abs(grow_decision) > 0.5 * grow_treshold:
            grow_type_decision = abs(grow_type_decision)
            if grow_type_decision < 0.5 * grow_type_treshold: grow_type = cf.ARM
            else: grow_type = cf.REPRODUCTOR
            # elif grow_type_decision < 2.5 * grow_type_treshold: grow_type = EYES
            #else: grow_type = cf.ARM
            try:
                _ = t.rndChoose(self.children).Grow(grow_type)
            except:
                pass

        self.life += -0.1
        self.life = min(100., self.life)
        # Pos for next step
        direction = self.getDirection()
        if self.canMoveToward(direction): self.MoveToward(direction)
        else: self.MoveToward((0, 0))

    def canGenerateArm(self):
        potential_pos = [t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (1, 0)), t.Vadd(self.pos, (-1, 0))]
        t.shuffle(potential_pos)
        for pos in potential_pos:
            if isInGrid(pos) and vr.grid.getAt(tuple(pos)).variant == cf.BASE:
                return True, tuple(pos)
        return False, None
    def canReproduce(self):
        for child in self.children:
            free_pos_found, free_pos = child.getReproducePos()
            if free_pos_found:
                return True, tuple(free_pos)
        return False, None

    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, 'blue', [x, y, length, length])
    def getDirection(self):

        motricity_input = (self.getGlobalLife(mean=True)/100, self.getNbTotalChildren())
        decision = self.motricity_brain.predict(motricity_input)
        threshold, dir_decision_1, dir_decision_2 = decision

        threshold = 0.5 * threshold
        direction = (0, 0)
        if dir_decision_1 > threshold and abs(dir_decision_2) < abs(threshold) :
            direction = (1, 0)
        elif dir_decision_1 < -threshold and abs(dir_decision_2) < abs(threshold) :
            direction = (-1, 0)
        elif dir_decision_2 > threshold and abs(dir_decision_1) < abs(threshold) :
            direction = (0, 1)
        elif dir_decision_2 < -threshold and abs(dir_decision_1) < abs(threshold) :
            direction = (0, -1)
        return direction

class Arm(Cell):
    def __init__(self, pos, father, body_id):
        super().__init__(pos)
        self.variant = cf.ARM
        self.father = father
        self.life = self.father.life
        self.body_id = body_id
    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, 'grey', [x, y, length, length])
    def update(self):
        super().update()

        self.life += -0.1

        for child in self.children:
            child.update()

    def Grow(self, grow_type):
        have_grew = False
        for child in t.Shuffle(self.children):
             have_grew = child.Grow(grow_type)
        if have_grew is False:
            can_grow, pos_grow = self.canGrow()
            if can_grow:
                have_grew = True
                self.life = self.life * 0.6
                if   grow_type == cf.ARM:          new_child = Arm(pos_grow, self, self.body_id)
                elif grow_type == cf.REPRODUCTOR:  new_child = Reproductor(pos_grow, self, self.body_id)
                else:                           new_child = Arm(pos_grow, self, self.body_id)
                self.children.append(new_child)
        return have_grew

    def canGrow(self):
        potential_pos = [t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (1, 0)), t.Vadd(self.pos, (-1, 0))]
        for pos in t.Shuffle(potential_pos):
            if isInGrid(pos) and vr.grid.getAt(tuple(pos)).variant == cf.BASE:
                return True, tuple(pos)
        return False, None

    def getReproducePos(self):
        for child in self.children:
            free_pos_found, free_pos = child.getReproducePos()
            if free_pos_found:
                return True, tuple(free_pos)
        return False, None

class Reproductor(Cell):
    def __init__(self, pos, father, body_id):
        super().__init__(pos)
        self.variant = cf.REPRODUCTOR
        self.father = father
        self.life = self.father.life
        self.body_id = body_id
    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, (250, 190, 80), [x, y, length, length])
    def update(self):
        super().update()
        for child in self.children:
            child.update()

    def getReproducePos(self):
        potential_pos = [t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (1, 0)),
                         t.Vadd(self.pos, (-1, 0))]
        t.shuffle(potential_pos)
        for pos in potential_pos:
            if isInGrid(pos):
                if vr.grid.getAt(tuple(pos)).variant == cf.BASE:
                    return True, tuple(pos)
        return False, None
