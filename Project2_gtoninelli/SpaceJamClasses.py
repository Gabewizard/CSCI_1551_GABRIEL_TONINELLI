# GABRIEL F. TONINELLI - PROJECT2 - CSCI-1551

from panda3d.core import Filename

# UNIVERSE CLASS - BACKGROUND SKYBOX
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
