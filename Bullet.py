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


def distance(x1, y1, z1, x2, y2, z2):
    return (((x1 - x2)**2) + ((y1 - y2)**2) + ((z1 - z2)**2))**0.5


def distanceXY(x1, y1, x2, y2):
    return (((x1 - x2)**2) + ((y1 - y2)**2))**0.5


def step(task):
    newList = []
    for bullet in range(len(Bullet.bullets)):
        Bullet.bullets[bullet].move(task)
        if (math.fabs(Bullet.bullets[bullet].x) > 4000 or
            math.fabs(Bullet.bullets[bullet].y) > 4000 or
                math.fabs(Bullet.bullets[bullet].z) > 4000):
            continue
            Bullet.bullets[bullet].model.removeNode()
            Bullet.bullets[bullet].model.unloadModel()
        newList.append(Bullet.bullets[bullet])
    Bullet.bullets = newList
    """for i in range(len(Bullet.queue.getEntries())):
        entry = Bullet.queue.getEntry(i)
        print(entry.getIntoNodePath())
        objectNodePath = entry.getFromNodePath().findNetTag('object')
        objectNode = entry.getFromNodePath()
        if not objectNodePath.isEmpty() and "Test" in repr(entry.getIntoNodePath()):
            objectNodePath.removeNode()
            objectNode.removeNode()"""
    return task.cont


class Bullet(object):
    bullets = []
    queue = CollisionHandlerQueue()

    def __init__(self, base, path, xyz, h, p, speed, damage, traverser):
        self.damage = damage
        self.model = base.loader.loadModel(path)
        self.model.reparentTo(render)
        self.model.setScale(1, 1, 1)
        self.model.setBillboardAxis()
        self.x, self.y, self.z = xyz[0], xyz[1], xyz[2]
        self.dx, self.dy, self.dz = math.sin(
            -h * (math.pi / 180)), math.cos(-h * (math.pi / 180)), math.sin(p * (math.pi / 180))
        self.speed = speed
        self.x += 20 * self.dx
        self.y += 20 * self.dy
        self.z += 20 * self.dz
        self.model.setFluidPos(self.x, self.y, self.z)
        self.model.setTag('object', '1')
        # Create a collision node for this object.
        cNode = CollisionNode('bullet')
        # Attach a collision sphere solid to the collision node.
        cNode.addSolid(CollisionSphere(0, 0, 0, 1))
        # Attach the collision node to the object's model.
        bulletC = self.model.attachNewNode(cNode)
        bulletC.show()
        bulletC.setCollideMask(BitMask32(0x10))
        traverser.setRespectPrevTransform(True)
        traverser.addCollider(bulletC, Bullet.queue)
        traverser.traverse(render)
        Bullet.bullets.append(self)

    def move(self, task):
        self.x += self.speed * self.dx
        self.y += self.speed * self.dy
        self.z += self.speed * self.dz
        self.model.setFluidPos(self.x, self.y, self.z)
