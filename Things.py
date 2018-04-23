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


class Thing(ShowBase):
    def __init__(self, base, x, y, z, scale, modelPath):
        self.x = x
        self.y = y
        self.z = z
        self.base = base
        self.model = self.base.loader.loadModel(modelPath)
        self.model.reparentTo(render)
        self.model.setScale(scale, scale, scale)
        self.model.setFluidPos(self.x, self.y, self.z)


class Monster(ShowBase):
    def __init__(self, base, x, y, z, scale, modelPath, pusher, traverser):
        self.x = x
        self.y = y
        self.z = z
        self.gun = (200, 10, "frowney", 2)
        self.shot = 0
        self.health = 20
        self.base = base
        self.model = self.base.loader.loadModel(modelPath)
        self.model.reparentTo(render)
        self.model.setScale(scale, scale, scale)
        self.model.setFluidPos(self.x, self.y, self.z)
        self.model.setBillboardPointWorld()
        taskMgr.doMethodLater(0.2, self.move, "move")
        # Create a collision node for this object.
        cNode = CollisionNode('monster')
        # Attach a collision sphere solid to the collision node.
        cNode.addSolid(CollisionSphere(0, 0, 0, 5))

        anp = self.model.attachNewNode(ActorNode('actor'))
        fromObject = anp.attachNewNode(CollisionNode('colNode'))
        fromObject.node().addSolid(CollisionSphere(0, 0, 0, 5))

        pusher = PhysicsCollisionHandler()
        pusher.addCollider(fromObject, anp)

        traverser.addCollider(fromObject, pusher)

    def move(self, task):
        if Bullet.distance(self.x, self.y, self.z,
                           base.camera.getX(),
                           base.camera.getY(),
                           base.camera.getZ()) > 200:
            self.x -= 1 * math.sin(math.atan2((self.base.camera.getX() - self.model.getX()),
                                              (self.base.camera.getY() - self.model.getY())) * (180 / math.pi))
            self.y -= 1 * math.cos(math.atan2((self.base.camera.getX() - self.model.getX()),
                                              (self.base.camera.getY() - self.model.getY())) * (180 / math.pi))
            self.model.setFluidPos(self.x, self.y, self.z)

        return task.cont

    def createBullet(self):
        self.shot += 1
        if (self.shot % self.gun[0] == 0 or
            self.shot % self.gun[0] == 25 or
                self.shot % self.gun[0] == 50):
            Bullet.Bullet(self.base,
                          self.gun[2],
                          (self.model.getX(),
                           self.model.getY(),
                           self.model.getZ()),
                          -1 * math.atan2((self.base.camera.getX() - self.model.getX()),
                                          (self.base.camera.getY() - self.model.getY())) * (180 / math.pi),
                          math.atan2((self.base.camera.getZ() - self.model.getZ()), Bullet.distanceXY(self.model.getX(),
                                                                                                      self.model.getY(), self.base.camera.getX(),
                                                                                                      self.base.camera.getY())) * (180 / math.pi),
                          self.gun[1],
                          self.gun[3])

    def shoot(self, task):
        self.createBullet()
        return task.cont

    def checkHit(self, task):
        bullets = Bullet.Bullet.bullets
        newList = []
        for bullet in range(len(bullets)):
            if 10 > Bullet.distance(bullets[bullet].x,
                                    bullets[bullet].y,
                                    bullets[bullet].z,
                                    self.model.getX(),
                                    self.model.getY(),
                                    self.model.getZ()):
                self.takeDamage(bullets[bullet].damage)
                bullets[bullet].model.removeNode()
                continue
            newList.append(bullets[bullet])
        Bullet.Bullet.bullets = newList
        return task.cont

    def takeDamage(self, damage):
        self.health -= damage
        print("Monster:", self.health)
