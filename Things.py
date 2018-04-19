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
import Bullet


class Doomguy(object):
    def __init__(self, base, xyz, hpr, node, pusher, traverser):
        self.base = base
        self.shot = 0
        self.guns = [(100, 1, "smiley", 10), (25, 10, "frowney", 2)]
        self.gun = 1
        self.mouseX = self.mouseY = 0
        self.x, self.y, self.z = xyz[0], xyz[1], xyz[2]
        self.h, self.p, self.r = hpr[0], hpr[1], hpr[2]
        self.node = node
        self.keyMap = {"left": 0, "right": 0, "forward": 0,
                       "backward": 0, "fast": 0, "jump": 0, "shoot": 0}
        self.fall = 0
        self.jump = 0
        self.health = 100
        # Create a collision node for this object.
        cNode = CollisionNode('doomGuy')
        # Attach a collision sphere solid to the collision node.
        cNode.addSolid(CollisionSphere(0, 0, 0, .75))
        cNode.addSolid(CollisionSphere(0, 0, 2, .75))
        cNode.addSolid(CollisionSphere(2, 0, 0, .75))
        cNode.addSolid(CollisionSphere(-2, 0, 0, .75))
        cNode.addSolid(CollisionSphere(0, 2, 0, .75))
        cNode.addSolid(CollisionSphere(0, -2, 0, .75))
        cNode.addSolid(CollisionSphere(0, 0, -10, 6))

        # Attach the collision node to the object's model.
        doomGuyC = self.node.attachNewNode(cNode)
        # Add the Pusher collision handler to the collision traverser.
        traverser.addCollider(doomGuyC, pusher)
        # Add the 'camera' collision node to the Pusher collision handler.
        pusher.addCollider(doomGuyC, self.node, base.drive.node())
        taskMgr.doMethodLater(0.2, self.move, "move")

    def createBullet(self, speed):
        self.shot += 1
        if self.shot % self.guns[self.gun][0] == 0:
            Bullet.Bullet(self.base,
                          self.guns[self.gun][2],
                          (self.base.camera.getX(),
                           self.base.camera.getY(),
                           self.base.camera.getZ()),
                          self.base.camera.getH(),
                          self.base.camera.getP(),
                          self.guns[self.gun][1],
                          self.guns[self.gun][3])

    def switchWeapon(self, direction):
        if direction == "up":
            if self.gun == len(self.guns) - 1:
                self.gun = 0
            else:
                self.gun += 1
        if direction == "down":
            if self.gun == 0:
                self.gun = len(self.guns) - 1
            else:
                self.gun -= 1

    def shoot(self, task):
        if self.keyMap["shoot"] > 0:
            self.createBullet(0.5)
        return task.cont

    def checkHit(self, task):
        bullets = Bullet.Bullet.bullets
        newList = []
        for bullet in range(len(bullets)):
            if 10 > Bullet.distance(bullets[bullet].x,
                                    bullets[bullet].y,
                                    bullets[bullet].z,
                                    self.base.camera.getX(),
                                    self.base.camera.getY(),
                                    self.base.camera.getZ()):
                self.takeDamage(bullets[bullet].damage)
                bullets[bullet].model.removeNode()
                continue
            newList.append(bullets[bullet])
        Bullet.Bullet.bullets = newList
        return task.cont

    def takeDamage(self, damage):
        self.health -= damage
        print(self.health)

    def setKey(self, key, value):
        self.keyMap[key] = value

    def move(self, task):
        x, y = 0, 0
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
        self.node.setH(base.camera.getH() + 8 * (self.mouseX - x))
        if -90 <= base.camera.getP() <= 90:
            self.node.setP(base.camera.getP() - 4 * (self.mouseY - y))
        else:
            if base.camera.getP() < -90:
                base.camera.setP(-90)
            if base.camera.getP() > 90:
                base.camera.setP(90)
        self.mouseX = x
        self.mouseY = y
        (x, y, z) = self.node.getPos()
        (h, p, r) = self.node.getHpr()
        if z < -100:
            self.node.setFluidPos(0, 0, 0)
            return task.cont

        (dx, dy, dz) = (0, 0, 0)
        (dh, dp, dr) = (0, 0, 0)

        dx = self.keyMap["forward"] - self.keyMap["backward"]

        dy = self.keyMap["left"] - self.keyMap["right"]

        if self.keyMap["jump"] > 0 and self.jump < 1:
            self.fall = 3
            self.jump = 1
            self.keyMap["jump"] = 0

        if self.keyMap["fast"] > 0:
            dx *= 2
            dy *= 2

        if self.fall >= -5:
            self.fall -= 0.2
        dz += self.fall

        (self.x, self.y, self.z) = self.x + dx, self.y + dy, self.z + dz
        (self.h, self.p, self.r) = self.h + dh, self.p + dp, self.r + dr

        self.node.setFluidPos(self.node, dx, dy, 0)
        self.node.setFluidZ(z + dz)
        if self.fall < -3:
            self.jump = 0
        return task.cont


class Thing(ShowBase):
    def __init__(self, base, x, y, z, scale, modelPath):
        self.x = x
        self.y = y
        self.z = z
        self.model = base.loader.loadModel(modelPath)
        self.model.reparentTo(render)
        self.model.setScale(scale, scale, scale)
        self.model.setFluidPos(self.x, self.y, self.z)
