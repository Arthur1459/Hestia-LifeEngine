from math import cos, sin, radians, degrees
from random import random

def Vcl(f1, v1, f2, v2):
    return [f1 * v1[i] + f2 * v2[i] for i in range(min(len(v1), len(v2)))]

def Vdiff(v1, v2):
    return [v1[i] - v2[i] for i in range(min(len(v1), len(v2)))]

def Vadd(v1, v2):
    return [v1[i] + v2[i] for i in range(min(len(v1), len(v2)))]

def Vmul(v, f):
    return [value * f for value in v]

def VxV(v1, v2):
    return [v1[i] * v2[i] for i in range(min(len(v1), len(v2)))]

def normalise(v):
    return Vmul(v, inv(norm(v)))

def inv(x): return 1/x if x != 0 else 0

def norm(x):
    return sum([v**2 for v in x])**0.5

def distance(x1, x2):
    return norm(Vdiff(x2, x1))

def Vdir(x1, x2):
    v = Vdiff(x2, x1)
    return Vmul(v, inv(norm(v)))

def makeSeg(a, b):
    return lambda t: (b[0] + (t - 1) * (b[0] - a[0]), b[1] + (t - 1) * (b[1] - a[1]))

def cross_product(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def s(x): return 1 if x > 0 else (-1 if x < 0 else 0)

def VintRounded(v):
    return [round(val) for val in v]

def VmaxControl(v, max_abs=1):
    return [min(max_abs, abs(val)) * s(val) for val in v]

def rndInt(a, b):
    return a + int(random() * (b - a))
