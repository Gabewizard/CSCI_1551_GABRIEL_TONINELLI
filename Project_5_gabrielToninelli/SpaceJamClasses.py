# GABRIEL F. TONINELLI - PROJECT5 - CLASSES FILE

from panda3d.core import Filename, Vec3, Point3
from CollideObjectBase import SphereCollideObject

# UNIVERSE BACKGROUND CLASS
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
class SpaceStation(SphereCollideObject):
    def __init__(self, loader, parent, traverser, pusher):
        self.model = loader.loadModel("Assets/SpaceStation1B/spaceStation.x")
        tex = loader.loadTexture("Assets/SpaceStation1B/SpaceStation1_Dif2.png")
        self.model.setTexture(tex, 1)
        self.model.setScale(6)
        self.model.setPos(0, 300, 0)
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)

        super().__init__(self.model, "Station", radius=7, parent=parent, traverser=traverser, pusher=pusher)

# DRONE CLASS
class Drone(SphereCollideObject):
    count = 0

    def __init__(self, loader, parent, pos, texture_path, traverser, pusher):
        Drone.count += 1
        self.model = loader.loadModel("Assets/DroneDefender/DroneDefender.x")
        tex = loader.loadTexture(Filename.fromOsSpecific(texture_path))
        self.model.setTexture(tex, 1)
        self.model.setScale(12)
        self.model.setPos(pos)
        self.model.setName(f"Drone{Drone.count}")
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)

        super().__init__(self.model, f"Drone{Drone.count}", radius=5, parent=parent, traverser=traverser, pusher=pusher)

# PLANET CLASS
class Planet(SphereCollideObject):
    def __init__(self, loader, modelPath, parentNode, nodeName, texPath, posVec, scaleVec, traverser, pusher):
        self.model = loader.loadModel(Filename.fromOsSpecific(modelPath))
        self.texture = loader.loadTexture(Filename.fromOsSpecific(texPath))
        self.model.setTexture(self.texture, 1)
        self.model.setPos(posVec)
        self.model.setScale(scaleVec)
        self.model.setTwoSided(True)
        self.model.setName(nodeName)
        self.model.reparentTo(parentNode)

        avg_scale = (scaleVec.getX() + scaleVec.getY() + scaleVec.getZ()) / 3
        radius = avg_scale * 0.055
        super().__init__(self.model, nodeName, radius=radius, parent=parentNode, traverser=traverser, pusher=pusher)

# MISSILE CLASS
class Missile(SphereCollideObject):
    fireModels = {}
    collisionNodes = {}
    intervals = {}
    collisionSolids = {}
    missileCount = 0

    def __init__(self, loader, modelPath, name, parent, camera, posVec, radius, traverser, pusher):
        Missile.missileCount += 1
        self.model = loader.loadModel(Filename.fromOsSpecific(modelPath))
        tex_path = "Assets/Phaser/phaser_auv.jpg"
        tex = loader.loadTexture(Filename.fromOsSpecific(tex_path))
        self.model.setTexture(tex, 1)
        self.model.setScale(3.7)
        self.model.setPos(posVec)
        self.model.setName(name)
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)

        super().__init__(self.model, name, radius=radius, parent=parent, traverser=traverser, pusher=pusher, is_dynamic=True)

        Missile.fireModels[name] = self.model
        Missile.collisionNodes[name] = self.model.find("**/+CollisionNode")
        Missile.collisionSolids[name] = radius
