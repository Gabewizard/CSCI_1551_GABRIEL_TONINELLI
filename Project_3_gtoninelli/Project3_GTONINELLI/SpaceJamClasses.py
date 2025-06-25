# GABRIEL F. TONINELLI - PROJECT3 - CSCI-1551

from panda3d.core import Filename, Vec3
from direct.task import Task

# UNIVERSE CLASS
class Universe:
    def __init__(self, loader, parent):
        model_path = "Assets/Universe/Universe.obj"
        tex_path = "Assets/Universe/starfield-in-blue.jpg"
        self.model = loader.loadModel(Filename.fromOsSpecific(model_path))
        self.texture = loader.loadTexture(Filename.fromOsSpecific(tex_path))
        self.model.setTexture(self.texture, 1)
        self.model.setScale(7500)
        self.model.setBin("background", 0)
        self.model.setDepthWrite(False)
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)

# SPACE STATION CLASS
class SpaceStation:
    def __init__(self, loader, parent):
        self.model = loader.loadModel("Assets/SpaceStation1B/spaceStation.x")
        tex = loader.loadTexture("Assets/SpaceStation1B/SpaceStation1_Dif2.png")
        self.model.setTexture(tex, 1)
        self.model.setScale(6)
        self.model.setPos(0, 300, 0)
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)

# SPACESHIP (PLAYER) CLASS
class Spaceship:
    def __init__(self, loader, parent):
        self.model = loader.loadModel("Assets/Dumbledore/Dumbledore.x")
        tex = loader.loadTexture("Assets/Dumbledore/spacejet_C.png")
        self.model.setTexture(tex, 1)
        self.model.setScale(10)
        self.model.setPos(0, 0, 0)
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)

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

    def move_forward(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_forward, "move-forward")
        else:
            taskMgr.remove("move-forward")

    def apply_forward(self, task):
        rate = 30
        direction = self.model.getQuat().getForward()
        self.model.setFluidPos(self.model.getPos() + direction * rate)
        return Task.cont

    def move_backward(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_backward, "move-backward")
        else:
            taskMgr.remove("move-backward")

    def apply_backward(self, task):
        rate = 30
        direction = self.model.getQuat().getForward()
        self.model.setFluidPos(self.model.getPos() - direction * rate)
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

# DRONE CLASS
class Drone:
    count = 0

    def __init__(self, loader, parent, pos, texture_path):
        Drone.count += 1
        self.model = loader.loadModel("Assets/DroneDefender/DroneDefender.x")
        tex = loader.loadTexture(Filename.fromOsSpecific(texture_path))
        self.model.setTexture(tex, 1)
        self.model.setScale(12)
        self.model.setPos(pos)
        self.model.setName(f"Drone{Drone.count}")
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)

# PLANET CLASS
class Planet:
    def __init__(self, loader, modelPath, parentNode, nodeName, texPath, posVec, scaleVec):
        self.model = loader.loadModel(Filename.fromOsSpecific(modelPath))
        self.texture = loader.loadTexture(Filename.fromOsSpecific(texPath))
        self.model.setTexture(self.texture, 1)
        self.model.setPos(posVec)
        self.model.setScale(scaleVec)
        self.model.reparentTo(parentNode)
        self.model.setName(nodeName)
        self.model.setTwoSided(True)
