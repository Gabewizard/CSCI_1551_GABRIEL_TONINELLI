# GABRIEL F. TONINELLI - PROJECT6 - CLASSES FILE
from panda3d.core import Filename, Vec3, Point3, CollisionNode, CollisionSphere, CardMaker, TransparencyAttrib
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
    def __init__(self, loader, parent, traverser, pusher, player_ref=None):
        self.model = loader.loadModel("Assets/SpaceStation1B/spaceStation.x")
        tex = loader.loadTexture("Assets/SpaceStation1B/SpaceStation1_Dif2.png")
        self.model.setTexture(tex, 1)
        self.model.setScale(8)
        self.model.setPos(0, 300, 0)
        self.model.setTwoSided(True)
        self.model.setName("Station")
        self.model.reparentTo(parent)
        self.model.setPythonTag("station_instance", self)

        super().__init__(self.model, "Station", radius=7, parent=parent, traverser=traverser, pusher=pusher)

        self.max_health = 2500
        self.health = self.max_health
        self.player_ref = player_ref

        self._create_health_bar()
        self.health_bg.hide()
        self.health_fg.hide()

    def _create_health_bar(self):
        cm_bg = CardMaker("station_health_bg")
        cm_bg.setFrame(-4, 4, -0.6, 0.6)  
        self.health_bg = self.model.attachNewNode(cm_bg.generate())
        self.health_bg.setColor(1, 0, 0, 1)
        self.health_bg.setBillboardPointEye()
        self.health_bg.setPos(0, 0, 18)
        self._make_bar_unlit(self.health_bg)

        cm_fg = CardMaker("station_health_fg")
        cm_fg.setFrame(-4, 4, -0.6, 0.6)  
        self.health_fg = self.model.attachNewNode(cm_fg.generate())
        self.health_fg.setColor(0, 1, 0, 1)
        self.health_fg.setBillboardPointEye()
        self.health_fg.setPos(0, 0, 18.01)
        self._make_bar_unlit(self.health_fg)

    def _make_bar_unlit(self, node):
        node.setLightOff()
        node.setShaderOff()
        node.setColorScaleOff()
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setTwoSided(True)
        node.setDepthTest(False)
        node.setDepthWrite(False)
        node.setBin("fixed", 0)

    def apply_damage_from_player(self, amount):
        self.health_bg.show()
        self.health_fg.show()
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self._update_health_bar()

        if self.player_ref:
            self.player_ref.update_score(10)

        if self.health <= 0:
            if self.player_ref:
                self.player_ref.update_score(200)
            self.destroy()

    def _update_health_bar(self):
        health_ratio = self.health / self.max_health
        red_amount = min(1.0, (1 - health_ratio) * 1.2)     
        green_amount = max(0.0, health_ratio * 1.2)         
        self.health_fg.setScale(health_ratio, 1, 1)
        self.health_fg.setColor(red_amount, green_amount, 0, 1)

    def destroy(self):
        self.model.removeNode()

# DRONE CLASS
class Drone(SphereCollideObject):
    count = 0

    def __init__(self, loader, parent, pos, texture_path, traverser, pusher, player_ref=None):
        Drone.count += 1
        self.model = loader.loadModel("Assets/DroneDefender/DroneDefender.x")
        tex = loader.loadTexture(Filename.fromOsSpecific(texture_path))
        self.model.setTexture(tex, 1)
        self.model.setScale(12)
        self.model.setPos(pos)
        self.model.setName(f"Drone{Drone.count}")
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)
        self.model.setPythonTag("drone_instance", self)

        super().__init__(self.model, f"Drone{Drone.count}", radius=5, parent=parent, traverser=traverser, pusher=pusher)

        self.max_health = 725
        self.health = self.max_health
        self.player_ref = player_ref
        self._create_health_bar()
        self.health_bg.hide()
        self.health_fg.hide()

    def _create_health_bar(self):
        cm_bg = CardMaker("drone_health_bg")
        cm_bg.setFrame(-1.5, 1.5, -0.6, 0.6)  
        self.health_bg = self.model.attachNewNode(cm_bg.generate())
        self.health_bg.setColor(1, 0, 0, 1)
        self.health_bg.setBillboardPointEye()
        self.health_bg.setPos(0, 0, self.model.getScale().getZ() * 0.3)
        self._make_bar_unlit(self.health_bg)

        cm_fg = CardMaker("drone_health_fg")
        cm_fg.setFrame(-1.5, 1.5, -0.6, 0.6)  
        self.health_fg = self.model.attachNewNode(cm_fg.generate())
        self.health_fg.setColor(0, 1, 0, 1)
        self.health_fg.setBillboardPointEye()
        self.health_fg.setPos(0, 0, self.model.getScale().getZ() * 0.3 + 0.01)
        self._make_bar_unlit(self.health_fg)

    def _make_bar_unlit(self, node):
        node.setLightOff()
        node.setShaderOff()
        node.setColorScaleOff()
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setTwoSided(True)
        node.setDepthTest(False)
        node.setDepthWrite(False)
        node.setBin("fixed", 0)

    def take_damage(self, amount):
        self.health_bg.show()
        self.health_fg.show()
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self._update_health_bar()

        if self.player_ref:
            self.player_ref.update_score(10)

        if self.health <= 0:
            if self.player_ref:
                self.player_ref.update_score(100)
            self.destroy()

    def _update_health_bar(self):
        health_ratio = self.health / self.max_health
        red_amount = min(1.0, (1 - health_ratio) * 1.2)
        green_amount = max(0.0, health_ratio * 1.2)
        self.health_fg.setScale(health_ratio, 1, 1)
        self.health_fg.setColor(red_amount, green_amount, 0, 1)

    def destroy(self):
        self.model.removeNode()

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
        radius = avg_scale * 0.035
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
