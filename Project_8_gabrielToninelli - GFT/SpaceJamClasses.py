# GABRIEL F. TONINELLI - PROJECT8 - CLASSES FILE
from panda3d.core import Filename, Vec3, Point3, CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerQueue, CardMaker, TransparencyAttrib, LineSegs, Material
from CollideObjectBase import SphereCollideObject
from DefensePaths import cloud as CloudPath
import random, math
from direct.interval.IntervalGlobal import Sequence, LerpPosInterval

# -----------------------
# UNIVERSE BACKGROUND CLASS
# -----------------------
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

# -----------------------
# SPACE STATION CLASS
# -----------------------
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

# -----------------------
# DRONE CLASS
# -----------------------
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

        self.max_health = 1500
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
        self.health_bg.setBin("fixed", 100)
        self._make_bar_unlit(self.health_bg)

        cm_fg = CardMaker("drone_health_fg")
        cm_fg.setFrame(-1.5, 1.5, -0.6, 0.6)
        self.health_fg = self.model.attachNewNode(cm_fg.generate())
        self.health_fg.setColor(0, 1, 0, 1)
        self.health_fg.setBillboardPointEye()
        self.health_fg.setPos(0, 0, self.model.getScale().getZ() * 0.3 + 0.01)
        self.health_fg.setBin("fixed", 101)
        self._make_bar_unlit(self.health_fg)

    def _make_bar_unlit(self, node):
        node.setLightOff()
        node.setShaderOff()
        node.setColorScaleOff()
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setTwoSided(True)
        node.setDepthTest(False)
        node.setDepthWrite(False)

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

# -----------------------
# PLANET CLASS
# -----------------------
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

# -----------------------
# MISSILE CLASS
# -----------------------
class Missile(SphereCollideObject):
    fireModels = {}
    collisionNodes = {}
    intervals = {}
    collisionSolids = {}
    missileCount = 0

    @classmethod
    def clear_all(cls):
        """Completely remove all missiles from scene & reset tracking."""
        for missile in list(cls.fireModels.keys()):
            cls.fireModels[missile].removeNode()
        cls.fireModels.clear()
        cls.collisionNodes.clear()
        cls.collisionSolids.clear()
        cls.intervals.clear()

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
# -----------------------
# LASER CLASS
# -----------------------
class Laser:
    def __init__(self, shooter_model, traverser, range_distance=2000, beam_speed=2000):
        self.shooter_model = shooter_model
        self.range = range_distance
        self.beam_speed = beam_speed
        self.beam_node = None
        self.traverser = traverser
        self.queue = CollisionHandlerQueue()

        self.ray_node = CollisionNode("laser_ray")
        self.ray = CollisionRay()
        self.ray_node.addSolid(self.ray)
        self.ray_node.setFromCollideMask(0xFFFFFFFF)
        self.ray_node.setIntoCollideMask(0)
        self.ray_np = render.attachNewNode(self.ray_node)
        self.traverser.addCollider(self.ray_np, self.queue)

        self.start_point = None
        self.end_point = None

    def fire(self):
        forward_vec = render.getRelativeVector(self.shooter_model, Vec3(0, 1, 0)).normalized()
        start_point = self.shooter_model.getPos(render) + forward_vec * 150

        self.ray.setOrigin(start_point)
        self.ray.setDirection(forward_vec)

        self.traverser.traverse(render)
        self.queue.sortEntries()

        hit_point = None
        if self.queue.getNumEntries() > 0:
            entry = self.queue.getEntry(0)
            hit_point = entry.getSurfacePoint(render)
            target_name = entry.getIntoNodePath().getName()
            victim_base = ''.join([c for c in target_name if not c.isdigit()])

            if victim_base in ["Drone", "Orbiter", "Wanderer"]:
                target_node = render.find(f"**/{target_name}")
                if not target_node.isEmpty():
                    target_node.getPythonTag("drone_instance").take_damage(300)  # Increased from 100
            elif victim_base == "Station":
                target_node = render.find(f"**/{target_name}")
                if not target_node.isEmpty():
                    target_node.getPythonTag("station_instance").apply_damage_from_player(300)  # Increased from 100

        end_point = hit_point if hit_point else (start_point + forward_vec * self.range)
        self.start_point = start_point
        self.end_point = end_point
        self._draw_beam(self.start_point, self.end_point)

        taskMgr.add(self.move_beam_task, "move-beam-task")
        taskMgr.doMethodLater(2, self.remove_beam, f"remove-beam-task-{id(self)}")

    def _draw_beam(self, start, end):
        if self.beam_node:
            self.beam_node.removeNode()
        ls = LineSegs()
        ls.setThickness(2.5)
        ls.setColor(1, 0, 0, 1)
        ls.moveTo(start)
        ls.drawTo(end)
        self.beam_node = render.attachNewNode(ls.create())
        self.beam_node.setBin("fixed", 200)
        self.beam_node.setDepthTest(False)
        self.beam_node.setDepthWrite(False)

    def move_beam_task(self, task):
        if not self.start_point or not self.end_point:
            return task.done
        direction = (self.end_point - self.start_point).normalized()
        distance = (self.end_point - self.start_point).length()
        move_dist = self.beam_speed * globalClock.getDt()

        if move_dist >= distance:
            self.remove_beam()
            return task.done

        self.start_point = self.start_point + direction * move_dist
        self._draw_beam(self.start_point, self.end_point)
        return task.cont

    def remove_beam(self, task=None):
        taskMgr.remove("move-beam-task")
        if self.beam_node:
            self.beam_node.removeNode()
            self.beam_node = None
        return task.done if task else None

# -----------------------
# ORBITER CLASS
# -----------------------
class Orbiter(SphereCollideObject):
    count = 0
    cloud_group_centers = {}
    cloud_group_offsets = {}
    cloud_group_next_index = {}
    cloud_group_last_update = {}

    def __init__(self, loader, taskMgr, modelPath, parentNode, name, scale, texturePath,
                 centralObject, orbitRadius, orbitType, staringAt,
                 traverser, pusher, player_ref=None, cloud_group=None):
        Orbiter.count += 1
        self.loader = loader
        self.taskMgr = taskMgr
        self.centralObject = centralObject
        self.orbitRadius = orbitRadius
        self.orbitType = orbitType.lower()
        self.staringAt = staringAt
        self.player_ref = player_ref
        self.cloud_group = cloud_group

        self.velocity = 0.5 if self.orbitType == "cloud" else 0.03
        self.angle = random.uniform(0, 2 * math.pi)

        self.model = loader.loadModel(Filename.fromOsSpecific(modelPath))
        if texturePath:
            tex = loader.loadTexture(Filename.fromOsSpecific(texturePath))
            self.model.setTexture(tex, 1)

        if self.orbitType in ["mlb", "cloud"]:
            self.model.setScale(scale * 1.5)
        else:
            self.model.setScale(scale)

        self.model.setTwoSided(True)
        self.model.setName(f"Orbiter{Orbiter.count}")
        self.model.reparentTo(parentNode)
        self.model.setPythonTag("drone_instance", self)

        super().__init__(self.model, f"Orbiter{Orbiter.count}", radius=5,
                         parent=parentNode, traverser=traverser, pusher=pusher)

        self.max_health = 1600
        self.health = self.max_health
        self._create_health_bar()
        self.health_bg.hide()
        self.health_fg.hide()

        self.last_central_pos = self.centralObject.getPos()

        if self.orbitType == "cloud":
            self.cloudTimer = 5.0
            self.cloudClock = 0.0
            if self.cloud_group not in Orbiter.cloud_group_centers:
                Orbiter.cloud_group_centers[self.cloud_group] = self._random_cloud_center()
            if self.cloud_group not in Orbiter.cloud_group_offsets:
                Orbiter.cloud_group_offsets[self.cloud_group] = self._generate_offsets()
                Orbiter.cloud_group_next_index[self.cloud_group] = 0
                Orbiter.cloud_group_last_update[self.cloud_group] = -1
            self.offset_index = Orbiter.cloud_group_next_index[self.cloud_group]
            Orbiter.cloud_group_next_index[self.cloud_group] += 1

        self.task_name = f"orbit-task-{Orbiter.count}"
        taskMgr.add(self.Orbit, self.task_name)

    def _generate_offsets(self):
        spread = 110
        return [Point3(random.uniform(-spread, spread),
                       random.uniform(-spread, spread),
                       random.uniform(-spread, spread)) for _ in range(10)]

    def _create_health_bar(self):
        cm_bg = CardMaker("orbiter_health_bg")
        cm_bg.setFrame(-1.5, 1.5, -0.6, 0.6)
        self.health_bg = self.model.attachNewNode(cm_bg.generate())
        self.health_bg.setColor(1, 0, 0, 1)
        self.health_bg.setBillboardPointEye()
        self.health_bg.setPos(0, 0, 1.5)
        self.health_bg.setBin("fixed", 100)
        self._make_bar_unlit(self.health_bg)

        cm_fg = CardMaker("orbiter_health_fg")
        cm_fg.setFrame(-1.5, 1.5, -0.6, 0.6)
        self.health_fg = self.model.attachNewNode(cm_fg.generate())
        self.health_fg.setColor(0, 1, 0, 1)
        self.health_fg.setBillboardPointEye()
        self.health_fg.setPos(0, 0, 1.51)
        self.health_fg.setBin("fixed", 101)
        self._make_bar_unlit(self.health_fg)

    def _make_bar_unlit(self, node):
        node.setLightOff()
        node.setShaderOff()
        node.setColorScaleOff()
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setTwoSided(True)
        node.setDepthTest(False)
        node.setDepthWrite(False)

    def _random_cloud_center(self):
        angle_h = random.uniform(0, 2 * math.pi)
        angle_v = random.uniform(-math.pi/4, math.pi/4)
        dist = random.uniform(self.orbitRadius * 0.7, self.orbitRadius)
        return self.last_central_pos + Point3(
            math.cos(angle_h) * math.cos(angle_v) * dist,
            math.sin(angle_h) * math.cos(angle_v) * dist,
            math.sin(angle_v) * dist
        )

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
        taskMgr.remove(self.task_name)
        self.model.removeNode()

    def Orbit(self, task):
        if not self.centralObject.isEmpty():
            self.last_central_pos = self.centralObject.getPos()

        if self.orbitType == "mlb":
            t = task.time * (self.velocity * 20.0)
            k = 2.2
            r = self.orbitRadius
            x = r * math.cos(t) * math.cos(k * t)
            y = r * math.sin(t) * math.cos(k * t)
            z = r * math.sin(k * t)
            self.model.setPos(self.last_central_pos + Point3(x, y, z))

        elif self.orbitType == "cloud":
            self.cloudClock += globalClock.getDt()
            if self.cloudClock >= self.cloudTimer:
                if Orbiter.cloud_group_last_update[self.cloud_group] != int(task.frame):
                    Orbiter.cloud_group_centers[self.cloud_group] = self._random_cloud_center()
                    Orbiter.cloud_group_offsets[self.cloud_group] = self._generate_offsets()
                    Orbiter.cloud_group_last_update[self.cloud_group] = int(task.frame)
                self.cloudClock = 0.0
            base_center = Orbiter.cloud_group_centers[self.cloud_group]
            offsets = Orbiter.cloud_group_offsets[self.cloud_group]
            if 0 <= self.offset_index < len(offsets):
                self.model.setPos(base_center + offsets[self.offset_index])

        if self.staringAt:
            self.model.lookAt(self.staringAt)

        return task.cont

# -----------------------
# WANDERER CLASS
# -----------------------
class Wanderer(SphereCollideObject):
    count = 0
    def __init__(self, loader, parent, traverser, pusher, player_ref=None):
        Wanderer.count += 1
        self.model = loader.loadModel("Assets/DroneDefender/DroneDefender.x")
        tex = loader.loadTexture(Filename.fromOsSpecific("Assets/DroneDefender/Drones.jpg"))
        self.model.setTexture(tex, 1)
        self.model.setScale(12)
        self.model.setName(f"Wanderer{Wanderer.count}")
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)
        self.model.setPythonTag("drone_instance", self)

        super().__init__(self.model, f"Wanderer{Wanderer.count}", radius=5,
                         parent=parent, traverser=traverser, pusher=pusher)

        self.max_health = 725
        self.health = self.max_health
        self.player_ref = player_ref
        self._create_health_bar()
        self.health_bg.hide()
        self.health_fg.hide()

        start = Point3(random.uniform(-500, 500), random.uniform(-500, 500), random.uniform(-200, 200))
        p2 = Point3(start.x + random.uniform(200, 400), start.y + random.uniform(200, 400), start.z)
        p3 = Point3(start.x - random.uniform(200, 400), start.y - random.uniform(200, 400), start.z + random.uniform(-150, 150))

        self.model.setPos(start)
        self.travelRoute = Sequence(
            LerpPosInterval(self.model, 4, p2),
            LerpPosInterval(self.model, 4, p3),
            LerpPosInterval(self.model, 4, start)
        )
        self.travelRoute.loop()

        if player_ref:
            self.face_task_name = f"wanderer-face-task-{Wanderer.count}"
            taskMgr.add(self.face_player_task, self.face_task_name)

    def _create_health_bar(self):
        cm_bg = CardMaker("wanderer_health_bg")
        cm_bg.setFrame(-1.5, 1.5, -0.6, 0.6)
        self.health_bg = self.model.attachNewNode(cm_bg.generate())
        self.health_bg.setColor(1, 0, 0, 1)
        self.health_bg.setBillboardPointEye()
        self.health_bg.setPos(0, 0, self.model.getScale().getZ() * 0.3)
        self.health_bg.setBin("fixed", 100)
        self._make_bar_unlit(self.health_bg)

        cm_fg = CardMaker("wanderer_health_fg")
        cm_fg.setFrame(-1.5, 1.5, -0.6, 0.6)
        self.health_fg = self.model.attachNewNode(cm_fg.generate())
        self.health_fg.setColor(0, 1, 0, 1)
        self.health_fg.setBillboardPointEye()
        self.health_fg.setPos(0, 0, self.model.getScale().getZ() * 0.3 + 0.01)
        self.health_fg.setBin("fixed", 101)
        self._make_bar_unlit(self.health_fg)

    def _make_bar_unlit(self, node):
        node.setLightOff()
        node.setShaderOff()
        node.setColorScaleOff()
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setTwoSided(True)
        node.setDepthTest(False)
        node.setDepthWrite(False)

    def face_player_task(self, task):
        if self.player_ref and not self.model.isEmpty():
            self.model.lookAt(self.player_ref.model)
        return task.cont

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
        if hasattr(self, "travelRoute"):
            self.travelRoute.finish()
        if hasattr(self, "face_task_name"):
            taskMgr.remove(self.face_task_name)
        self.model.removeNode()
