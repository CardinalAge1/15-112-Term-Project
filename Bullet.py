from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionNode, CollisionSphere
from panda3d.core import Point3
import sys
import math
import os
import random
from direct.task.Task import Task
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
import time
from panda3d.core import NodePath
from panda3d.physics import *
from direct.gui.DirectGui import DirectFrame, DirectLabel


def step(task):
    newList = []
    for bullet in range(len(Bullet.bullets)):
        Bullet.bullets[bullet].move(task)
        if (math.fabs(Bullet.bullets[bullet].x) > 4000 or
            math.fabs(Bullet.bullets[bullet].y) > 4000 or
                math.fabs(Bullet.bullets[bullet].z) > 4000):
            continue
        newList.append(Bullet.bullets[bullet])
    Bullet.bullets = newList
    return task.cont


class Bullet(object):
    bullets = []

    def __init__(self, base, path, xyz, h, p, speed):
        self.model = base.loader.loadModel(path)
        self.model.reparentTo(render)
        self.model.setScale(1, 1, 1)
        self.model.setBillboardAxis()
        self.x, self.y, self.z = xyz[0], xyz[1], xyz[2]
        self.dx, self.dy, self.dz = math.sin(
            -h * (math.pi / 180)), math.cos(-h * (math.pi / 180)), math.sin(p * (math.pi / 180))
        self.speed = speed
        self.x += 10 * self.dx
        self.y += 10 * self.dy
        self.z += 10 * self.dz
        self.model.setFluidPos(self.x, self.y, self.z)
        Bullet.bullets.append(self)

    def move(self, task):
        self.x += self.speed * self.dx
        self.y += self.speed * self.dy
        self.z += self.speed * self.dz
        self.model.setFluidPos(self.x, self.y, self.z)
