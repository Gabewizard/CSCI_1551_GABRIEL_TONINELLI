# GABRIEL F. TONINELLI - PROJECT5 

from panda3d.core import Filename, Vec3, TransparencyAttrib
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from CollideObjectBase import SphereCollideObject
from SpaceJamClasses import Missile

class Spaceship(SphereCollideObject):
    def __init__(self, loader, parent, traverser, pusher):
        self.loader = loader
        self.parent = parent
        self.traverser = traverser
        self.pusher = pusher

        self.model = loader.loadModel("Assets/Dumbledore/Dumbledore.x")
        tex = loader.loadTexture("Assets/Dumbledore/spacejet_C.png")
        self.model.setTexture(tex, 1)
        self.model.setScale(10)
        self.model.setPos(0, 0, 0)
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)

        super().__init__(self.model, "Player", radius=6, parent=parent, traverser=traverser, pusher=pusher, is_dynamic=True)

        self.reloadTime = 0.1
        self.missileDistance = 5200
        self.missileBay = 1

        self.firing = False

        self.set_key_bindings()

    def set_key_bindings(self):
        base.accept("w", self.move_forward, [True])
        base.accept("w-up", self.move_forward, [False])
        base.accept("s", self.move_backward, [True])
        base.accept("s-up", self.move_backward, [False])
        base.accept("a", self.turn_left, [True])
        base.accept("a-up", self.turn_left, [False])
        base.accept("d", self.turn_right, [True])
        base.accept("d-up", self.turn_right, [False])
        base.accept("arrow_up", self.pitch_up, [True])
        base.accept("arrow_up-up", self.pitch_up, [False])
        base.accept("arrow_down", self.pitch_down, [True])
        base.accept("arrow_down-up", self.pitch_down, [False])
        base.accept("q", self.roll_left, [True])
        base.accept("q-up", self.roll_left, [False])
        base.accept("e", self.roll_right, [True])
        base.accept("e-up", self.roll_right, [False])

        base.accept("space", self.start_firing)
        base.accept("space-up", self.stop_firing)

    def start_firing(self):
        self.firing = True
        taskMgr.add(self.fire_loop, "auto-fire-loop")

    def stop_firing(self):
        self.firing = False
        taskMgr.remove("auto-fire-loop")

    def fire_loop(self, task):
        if self.firing:
            self.Fire()
            return task.again
        return task.done

    def Fire(self):
        if self.missileBay:
            print("Missile Fired")
            aim = render.getRelativeVector(self.model, Vec3.forward())
            aim.normalize()
            fireSolution = aim * self.missileDistance
            inFront = aim * 150
            travVec = fireSolution + self.model.getPos()
            posVec = self.model.getPos() + inFront

            self.missileBay -= 1
            tag = "Missile-" + str(Missile.missileCount + 1)

            missile = Missile(self.loader, "Assets/Phaser/phaser.egg", tag, render, base.camera, posVec, 3, self.traverser, self.pusher)

            Missile.intervals[tag] = missile.model.posInterval(4.0, travVec, posVec, fluid=1)
            Missile.intervals[tag].start()

            taskMgr.doMethodLater(self.reloadTime, self.Reload, 'reload')
        else:
            if not taskMgr.hasTaskNamed('reload'):
                taskMgr.doMethodLater(self.reloadTime, self.Reload, 'reload')

    def Reload(self, task):
        self.missileBay = 1
        print("Reload Complete")
        return task.done

    def CheckIntervals(self, task):
        for missile in list(Missile.intervals.keys()):
            if not Missile.intervals[missile].isPlaying():
                Missile.collisionNodes[missile].removeNode()
                Missile.fireModels[missile].removeNode()
                del Missile.intervals[missile]
                del Missile.fireModels[missile]
                del Missile.collisionNodes[missile]
                del Missile.collisionSolids[missile]
                break
        return task.cont

    def EnableHUD(self):
        self.crosshair = OnscreenImage(
            image="Hud/Reticle3b.png",
            pos=(0.00, 0, 0.275),  
            scale=(0.065, 1, 0.05)
        )
        self.crosshair.setTransparency(TransparencyAttrib.MAlpha)

    def move_forward(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_forward, "move-forward")
        else:
            taskMgr.remove("move-forward")

    def apply_forward(self, task):
        direction = self.model.getQuat().getForward()
        self.model.setFluidPos(self.model.getPos() + direction * 20)
        return Task.cont

    def move_backward(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_backward, "move-backward")
        else:
            taskMgr.remove("move-backward")

    def apply_backward(self, task):
        direction = self.model.getQuat().getForward()
        self.model.setFluidPos(self.model.getPos() - direction * 30)
        return Task.cont

    def turn_left(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_turn_left, "turn-left")
        else:
            taskMgr.remove("turn-left")

    def apply_turn_left(self, task):
        self.model.setH(self.model.getH() + 1.0)
        return Task.cont

    def turn_right(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_turn_right, "turn-right")
        else:
            taskMgr.remove("turn-right")

    def apply_turn_right(self, task):
        self.model.setH(self.model.getH() - 1.0)
        return Task.cont

    def pitch_up(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_pitch_up, "pitch-up")
        else:
            taskMgr.remove("pitch-up")

    def apply_pitch_up(self, task):
        self.model.setP(self.model.getP() + 0.5)
        return Task.cont

    def pitch_down(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_pitch_down, "pitch-down")
        else:
            taskMgr.remove("pitch-down")

    def apply_pitch_down(self, task):
        self.model.setP(self.model.getP() - 0.5)
        return Task.cont

    def roll_left(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_roll_left, "roll-left")
        else:
            taskMgr.remove("roll-left")

    def apply_roll_left(self, task):
        self.model.setR(self.model.getR() + 1.0)
        return Task.cont

    def roll_right(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_roll_right, "roll-right")
        else:
            taskMgr.remove("roll-right")

    def apply_roll_right(self, task):
        self.model.setR(self.model.getR() - 1.0)
        return Task.cont
