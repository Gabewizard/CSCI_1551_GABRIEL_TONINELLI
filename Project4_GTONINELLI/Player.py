# GABRIEL F. TONINELLI - PROJECT4 - PLAYER CLASS

from panda3d.core import Filename
from direct.task import Task
from CollideObjectBase import SphereCollideObject

class Spaceship(SphereCollideObject):
    def __init__(self, loader, parent, traverser, pusher):
        self.model = loader.loadModel("Assets/Dumbledore/Dumbledore.x")
        tex = loader.loadTexture("Assets/Dumbledore/spacejet_C.png")
        self.model.setTexture(tex, 1)
        self.model.setScale(10)
        self.model.setPos(0, 0, 0)
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)

        # DYNAMIC COLLISION (Player is movable)
        super().__init__(self.model, "Player", radius=6, parent=parent, traverser=traverser, pusher=pusher, is_dynamic=True)

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

    def move_forward(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_forward, "move-forward")
        else:
            taskMgr.remove("move-forward")

    def apply_forward(self, task):
        direction = self.model.getQuat().getForward()
        self.model.setFluidPos(self.model.getPos() + direction * 20)  # Reduced speed
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
        self.model.setP(self.model.getP() + 0.5)  # Increased sensitivity
        return Task.cont

    def pitch_down(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_pitch_down, "pitch-down")
        else:
            taskMgr.remove("pitch-down")

    def apply_pitch_down(self, task):
        self.model.setP(self.model.getP() - 0.5)  # Increased sensitivity
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
