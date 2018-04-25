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
from panda3d.ai import *
from direct.gui.OnscreenText import OnscreenText


class Thing(ShowBase):
    def __init__(self, base, x, y, z, scale, modelPath):
        self.x = x
        self.y = y
        self.z = z
        self.base = base
        self.model = self.base.loader.loadModel(modelPath)
        self.model.setCollideMask(BitMask32(0x10))
        self.model.reparentTo(render)
        self.model.setScale(scale, scale, scale)
        self.model.setFluidPos(self.x, self.y, self.z)


class Monster(ShowBase):

    monsters = []

    def __init__(self, base, x, y, z, scale, modelPath, pusher, traverser):
        self.traverser = traverser
        self.dead = False
        self.corpse = False
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
        "self.model.setBillboardPointWorld()"
        """taskMgr.doMethodLater(0.2, self.move, "move")"""
        # Create a collision node for this object.
        cNode = CollisionNode('monster')
        # Attach a collision sphere solid to the collision node.
        cNode.addSolid(CollisionSphere(0, 0, 0, 0.5))

        self.monsterC = self.model.attachNewNode(cNode)

        traverser.addCollider(self.monsterC, pusher)

        pusher.addCollider(self.monsterC, self.model, base.drive.node())

        taskMgr.doMethodLater(0.1, self.shoot, "shoot")
        taskMgr.doMethodLater(0.2, self.checkHit, "checkHit")

        self.setAI()
        Monster.monsters.append(self)

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
                          self.gun[3],
                          self.traverser)

    def shoot(self, task):
        if not self.dead:
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
        if self.health <= 0 and self in Monster.monsters:
            self.dead = True
            Monster.monsters.remove(self)
        if len(Monster.monsters) == 0:
            textObject = OnscreenText(
                text='You WON', pos=(0, 0), scale=0.4)

    def setAI(self):
        # Creating AI World
        self.AIworld = AIWorld(render)

        self.AIchar = AICharacter("monster", self.model, 100, 5, 50)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()

        self.AIbehaviors.pursue(self.base.camera, 1)
        self.AIbehaviors.arrival(50)

        # AI World update
        taskMgr.add(self.AIUpdate, "AIUpdate")

    # to update the AIWorld
    def AIUpdate(self, task):
        self.model.setZ(-20)
        if self.dead and not self.corpse:
            self.corpse = self.model.getPos()
        if self.dead:
            self.model.setPos(self.corpse)
        self.AIworld.update()
        return task.cont
