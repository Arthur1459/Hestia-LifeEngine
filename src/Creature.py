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
        self.alive, self.life = True, 150
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
        if isInGrid(target) and vr.grid.getAt(target).variant != cf.WALL and (vr.grid.getAt(target).variant in cf.CAN_MOVE_ON or (vr.grid.getAt(target).variant in cf.BELONG_CREATURE and vr.grid.getAt(target).body_id == self.body_id)) and all([child.canMoveToward(dir) for child in self.children]): return True
        else: return False
    def MoveToNextStep(self, dir):
        vr.grid.clearAt(self.pos)

        if self.alive:
            new_pos = keepInGrid(t.Vadd(self.pos, dir))
            if t.distance(new_pos, self.pos) < 2:
                self.pos = new_pos
            for child in self.children:
                child.MoveToNextStep(dir)

            self.life += -cf.food_moving_lost
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
        self.life += -cf.food_general_lost
        if (self.life <= 0 and self.alive) or (self.father is not None and self.father.alive is False):
            self.die()
        if self.father is not None:
            if self.life > 100:
                self.father.life += self.life - 100
                self.life = 100

    def draw(self):
        pg.draw.rect(vr.window, cf.base_color, [self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size, cf.cell_size])
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
        vr.creatures[self.body_id] = u.rndColor()
        self.vision_processed = ()

        if genetic is None:
            self.motricity_brain = NeuralNetwork(8, 3, (4,))
            self.behavior_brain = NeuralNetwork(6, 6, (3,))
            self.eyes_brain = NeuralNetwork(36, 4, (12,))
            self.vision_brain = NeuralNetwork(1, 4, (4,))
        else:
            self.motricity_brain = NeuralNetwork(copy_from=genetic['motricity'])
            self.behavior_brain = NeuralNetwork(copy_from=genetic['behavior'])
            self.eyes_brain = NeuralNetwork(copy_from=genetic['eye'])
            self.vision_brain = NeuralNetwork(copy_from=genetic['vision'])

    def update(self):
        super().update()
        for child in self.children:
            child.update()

        self.processVision()

        behavior_input = t.MakeVectorIn1D((self.getGlobalLife(mean=True), self.getNbTotalChildren(), self.vision_processed))
        reproduce_treshold, reproduce_decision, grow_decision, grow_treshold, grow_type_decision, grow_type_treshold = self.behavior_brain.predict(behavior_input)

        can_arm, pos_arm = self.canGenerateArm()
        if can_arm and t.proba(1):
            self.children.append(Arm(pos_arm, self, self.body_id))

        can_reproduce, reproduce_pos = self.canReproduce()
        if can_reproduce and abs(reproduce_decision) > reproduce_treshold and self.life > 100:
            self.life = self.life - 100
            new_born = Body(reproduce_pos, genetic={'motricity': self.motricity_brain, 'behavior': self.behavior_brain, 'eye': self.eyes_brain, 'vision': self.vision_brain})
            new_born.life = self.life
            new_born.motricity_brain.Mutate()
            new_born.behavior_brain.Mutate()
            new_born.vision_brain.Mutate()
            new_born.eyes_brain.Mutate()
            new_born.life = self.life
            vr.grid.putAt(new_born, reproduce_pos)

        grow_type_treshold = abs(grow_type_treshold)
        if abs(grow_decision) > 0.5 * grow_treshold:
            if grow_type_decision < 0. * grow_type_treshold: grow_type = cf.ARM
            elif grow_type_decision < 3. * grow_type_treshold: grow_type = cf.REPRODUCTOR
            elif grow_type_decision < 5. * grow_type_treshold: grow_type = cf.SPIKE
            elif grow_type_decision < 7 * grow_type_treshold: grow_type = cf.EYES
            else: grow_type = cf.ARM
            try:
                _ = t.rndChoose(self.children).Grow(grow_type, genetic=None if (grow_type != cf.EYES) else self.eyes_brain)
            except:
                pass

        self.life = min(cf.max_body_food_storage, self.life)
        # Pos for next step
        direction = self.getDirection()
        if self.canMoveToward(direction):
            self.MoveToNextStep(direction)
        else: self.MoveToNextStep((0, 0))


    def canGenerateArm(self):
        potential_pos = [t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (1, 0)), t.Vadd(self.pos, (-1, 0))]
        t.shuffle(potential_pos)
        for pos in potential_pos:
            if isInGrid(pos) and vr.grid.getAt(tuple(pos)).variant in (cf.BASE, cf.FOOD):
                return True, tuple(pos)
        return False, None
    def canReproduce(self):
        for child in self.children:
            free_pos_found, free_pos = child.getReproducePos()
            if free_pos_found:
                return True, tuple(free_pos)
        return False, None

    def processVision(self):
        eyes_vision = self.getVision()
        nb_eyes = len(eyes_vision)
        vision_info = t.MakeVectorIn1D((nb_eyes, eyes_vision))
        if self.vision_brain.nb_inputs < len(vision_info):
            self.vision_brain.NewInput(amount=len(vision_info) - self.vision_brain.nb_inputs)
        if self.vision_brain.nb_inputs > len(vision_info):
            vision_info = vision_info + [0 for _ in range(self.vision_brain.nb_inputs - len(vision_info))]
        self.vision_processed = self.vision_brain.predict(vision_info)  # all information transform in a 4D vector

    def getVision(self):
        vision = []
        for child in self.children:
            eye_message = child.getVision()
            for msg in eye_message:
                vision.append(msg)
        return vision

    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, cf.body_color, [x, y, length, length])
    def getDirection(self):

        motricity_input = t.MakeVectorIn1D((self.getGlobalLife(mean=True)/100, self.getNbTotalChildren(), self.line()/vr.grid.lines(), self.row()/vr.grid.rows(), self.vision_processed))
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
        pg.draw.rect(vr.window, cf.arm_color, [x, y, length, length])
    def update(self):
        super().update()

        for child in self.children:
            child.update()

    def Grow(self, grow_type, genetic=None):
        have_grew = False
        for child in t.Shuffle(self.children):
            if child.variant == cf.ARM:
                have_grew = child.Grow(grow_type, genetic=genetic)
        if have_grew is False:
            can_grow, pos_grow = self.canGrow()
            if can_grow:
                have_grew = True
                self.life = self.life * 0.8
                if   grow_type == cf.ARM:          new_child = Arm(pos_grow, self, self.body_id)
                elif grow_type == cf.REPRODUCTOR:  new_child = Reproductor(pos_grow, self, self.body_id)
                elif grow_type == cf.SPIKE:        new_child = Spike(pos_grow, self, self.body_id)
                elif grow_type == cf.EYES:         new_child = Eye(pos_grow, self, self.body_id, vision_brain=genetic)
                else:                              new_child = Arm(pos_grow, self, self.body_id)
                self.children.append(new_child)
        return have_grew

    def canGrow(self):
        potential_pos = [t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (1, 0)), t.Vadd(self.pos, (-1, 0))]
        for pos in t.Shuffle(potential_pos):
            if isInGrid(pos) and vr.grid.getAt(tuple(pos)).variant in (cf.BASE, cf.FOOD):
                return True, tuple(pos)
        return False, None

    def getReproducePos(self):
        for child in self.children:
            if child.variant in (cf.ARM, cf.REPRODUCTOR):
                free_pos_found, free_pos = child.getReproducePos()
                if free_pos_found:
                    return True, tuple(free_pos)
        return False, None

    def getVision(self):
        vision = []
        for child in self.children:
            if child.variant == cf.ARM:
                arm_vision = child.getVision()
                if len(vision) > 0:
                    vision.append(arm_vision)
            if child.variant == cf.EYES:
                vision.append(child.getVision())
        return vision

class Reproductor(Cell):
    def __init__(self, pos, father, body_id):
        super().__init__(pos)
        self.variant = cf.REPRODUCTOR
        self.father = father
        self.life = self.father.life
        self.body_id = body_id
    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, cf.reproductor_color, [x, y, length, length])
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
                if vr.grid.getAt(tuple(pos)).variant in (cf.BASE, cf.FOOD):
                    return True, tuple(pos)
        return False, None

class Spike(Cell):
    def __init__(self, pos, father, body_id):
        super().__init__(pos)
        self.variant = cf.SPIKE
        self.father = father
        self.life = self.father.life
        self.body_id = body_id
    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, cf.spike_color, [x, y, length, length])
    def update(self):
        super().update()
        for child in self.children:
            child.update()

        potential_pos = [t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (1, 0)),
                         t.Vadd(self.pos, (-1, 0))]
        for pos in potential_pos:
            if isInGrid(pos):
                cell_touch = vr.grid.getAt(tuple(pos))
                if cell_touch.variant in cf.SPIKE_KILLABLE:
                    if cell_touch.body_id != self.body_id:
                        self.life += cell_touch.life
                        cell_touch.die()

class Eye(Cell):
    def __init__(self, pos, father, body_id, vision_brain):
        super().__init__(pos)
        self.variant = cf.EYES
        self.father = father
        self.life = self.father.life
        self.body_id = body_id
        self.vision = {}
        self.vision_brain = vision_brain
        self.vision_message = (0, 0, 0)
    def draw(self):
        x, y, length = self.row() * cf.cell_size, self.line() * cf.cell_size, cf.cell_size
        pg.draw.rect(vr.window, cf.eyes_color, [x, y, length, length])
    def update(self):
        super().update()
        for child in self.children:
            child.update()

    def getVision(self):
        self.vision = {}
        potential_pos = [t.Vadd(self.pos, (-2, 0)),
                         t.Vadd(self.pos, (-1, -1)), t.Vadd(self.pos, (-1, 0)), t.Vadd(self.pos, (-1, 1)),
                         t.Vadd(self.pos, (0, -2)), t.Vadd(self.pos, (0, -1)), t.Vadd(self.pos, (0, 1)), t.Vadd(self.pos, (0, 2)),
                         t.Vadd(self.pos, (1, -1)), t.Vadd(self.pos, (1, 0)), t.Vadd(self.pos, (1, 1)),
                         t.Vadd(self.pos, (2, 0))] # 12 points
        for pos in potential_pos:
            if isInGrid(pos):
                cell_touch = vr.grid.getAt(tuple(pos))
                if cell_touch.variant in cf.BELONG_CREATURE:
                    if cell_touch.body_id != self.body_id:
                        self.vision[tuple(pos)] = cell_touch.variant
                    else:
                        self.vision[tuple(pos)] = cf.MYBODY
                else:
                    self.vision[tuple(pos)] = cell_touch.variant
            else:
                self.vision[tuple(pos)] = cf.WALL

        brain_input = []
        for vision_pos in self.vision:
            brain_input.append(vision_pos[0])
            brain_input.append(vision_pos[1])
            brain_input.append(self.vision[vision_pos])
        self.vision_message = self.vision_brain.predict(brain_input)
        return self.vision_message[:]
