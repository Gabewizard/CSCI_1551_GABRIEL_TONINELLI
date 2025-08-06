# GABRIEL F. TONINELLI - PROJECT8 - MAIN FILE
from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, AmbientLight, Point3, Vec3, CollisionTraverser
from panda3d.core import CollisionHandlerPusher, loadPrcFileData
from direct.gui.OnscreenText import OnscreenText
from SpaceJamClasses import Universe, SpaceStation, Drone, Planet, Orbiter, Wanderer, Missile
from Player import Spaceship
from DefensePaths import get_all_defense_positions
from math import sin, cos, pi
import random

# FORCE-ENABLE PARTICLE SYSTEMS BEFORE STARTUP
loadPrcFileData("", "particles-enabled true")

class SpaceJam(ShowBase):
    def __init__(self):
        print("LAUNCHING SPACEJAM...")
        super().__init__()

        base.enableParticles()
        self.disableMouse()
        self.setBackgroundColor(0.1, 0.1, 0.1)

        # COLLISION SYSTEM
        self.traverser = CollisionTraverser()
        base.cTrav = self.traverser
        self.pusher = CollisionHandlerPusher()

        # LIGHTS
        self.setup_lights()

        # HUD restart text
        self.restart_text = OnscreenText(
            text="Press R to Restart",
            pos=(0.85, -0.95),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=0,
            mayChange=False
        )

        # HUD controls text
        self.controls_text_laser = OnscreenText(
            text="E = Laser",
            pos=(-1.25, -0.90),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=0,
            mayChange=False
        )
        self.controls_text_missiles = OnscreenText(
            text="SPACE = Missiles",
            pos=(-1.25, -0.95),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=0,
            mayChange=False
        )

        # Bind restart key
        base.accept("r", self.restart_game)

        # INITIALIZE SCENE
        self.start_game()

    def start_game(self):
        """Initializes all game objects and HUD fresh."""
        # Remove all old cooldown tasks from previous ships
        for task in list(taskMgr.getAllTasks()):
            if "laser-cooldown-task" in task.getName():
                taskMgr.remove(task.getName())

        # Remove old cooldown bar NodePath if it exists
        if hasattr(self, "ship") and hasattr(self.ship, "cooldown_bar") and self.ship.cooldown_bar:
            self.ship.cooldown_bar.removeNode()

        # Reset orbiter counter and clear old cloud group data
        Orbiter.count = 0
        Orbiter.cloud_group_centers.clear()
        Orbiter.cloud_group_offsets.clear()
        Orbiter.cloud_group_next_index.clear()
        Orbiter.cloud_group_last_update.clear()
        Wanderer.count = 0

        # Remove old score HUD if restarting
        if hasattr(self, "ship"):
            if hasattr(self.ship, "score_text"):
                self.ship.score_text.removeNode()
            self.ship.score = 0

        # SCENE OBJECTS
        self.universe = Universe(self.loader, self.camera)
        self.ship = Spaceship(self.loader, self.render, self.traverser, self.pusher)
        self.station = SpaceStation(self.loader, self.render, self.traverser, self.pusher, self.ship)

        # FIXED PLAYER SPAWN POSITION
        station_pos = self.station.model.getPos()
        spawn_distance = 500
        spawn_pos = Point3(station_pos.x, station_pos.y - spawn_distance, station_pos.z)
        self.ship.model.setPos(spawn_pos)
        self.ship.model.setHpr(0, 0, 0)
        self.ship.model.lookAt(self.station.model)

        # HUD
        self.ship.EnableHUD()

        # TASKS
        self.taskMgr.add(self.ship.CheckIntervals, "checkMissiles", 34)
        self.taskMgr.add(self.update_laser, "updateLaser")

        # CAMERA
        self.set_camera()

        # SPAWN OBJECTS
        self.spawn_planets()
        self.spawn_drones()
        self.spawn_orbiters()
        self.spawn_wanderers()

    def restart_game(self):
        print("RESTARTING GAME...")

        # Remove old tasks first
        self.taskMgr.remove("checkMissiles")
        self.taskMgr.remove("updateLaser")

        # REMOVE ALL ACTIVE MISSILES
        for missile_id in list(Missile.fireModels.keys()):
            if missile_id in Missile.intervals:
                Missile.intervals[missile_id].finish()
            if Missile.fireModels[missile_id]:
                Missile.fireModels[missile_id].removeNode()
        Missile.fireModels.clear()
        Missile.collisionNodes.clear()
        Missile.collisionSolids.clear()
        Missile.intervals.clear()

        # REMOVE ACTIVE LASER BEAM
        if hasattr(self, "ship") and self.ship.laser and self.ship.laser.beam_node:
            self.ship.laser.beam_node.removeNode()
            self.ship.laser.beam_node = None
        taskMgr.remove("move-beam-task")

        # REMOVE OLD NODES
        for child in render.getChildren():
            child.removeNode()

        self.start_game()

    def setup_lights(self):
        print("SETTING UP LIGHTS...")
        ambient = AmbientLight("ambient")
        ambient.setColor((0.3, 0.3, 0.3, 1))
        self.render.setLight(self.render.attachNewNode(ambient))
        sun = DirectionalLight("sun")
        sun.setColor((0.8, 0.8, 0.7, 1))
        sun_np = self.render.attachNewNode(sun)
        sun_np.setHpr(45, -60, 0)
        self.render.setLight(sun_np)

    def set_camera(self):
        self.camera.reparentTo(self.ship.model)
        self.camera.setPos(0, -35, 8)
        self.camera.lookAt(self.ship.model)
        self.camLens.setFov(85)

    def spawn_planets(self):
        print("SPAWNING PLANETS...")
        planet_data = [
            ("AlienPlanet", "Assets/Planets/AlienPlanet/AlienPlanet.obj", "Assets/Planets/AlienPlanet/planet_Bog1200.png"),
            ("Earth",       "Assets/Planets/Earth/Earth 2K.obj",           "Assets/Planets/Earth/Diffuse_2K.png"),
            ("Mars",        "Assets/Planets/Mars/Mars 2K.obj",             "Assets/Planets/Mars/Diffuse_2K.png"),
            ("Mercury",     "Assets/Planets/Mercury/Mercury 1K.obj",       "Assets/Planets/Mercury/Diffuse_1K.png"),
            ("Moon",        "Assets/Planets/Moon/Moon 2K.obj",             "Assets/Planets/Moon/Diffuse_2K.png"),
            ("Venus",       "Assets/Planets/Venus/Venus_1K.obj",           "Assets/Planets/Venus/Diffuse_1K.png"),
        ]
        radius = 6000
        angle_increment = 2 * pi / len(planet_data)
        for i, (name, model, tex) in enumerate(planet_data):
            angle = i * angle_increment
            x = radius * cos(angle)
            y = radius * sin(angle)
            z = 0
            Planet(self.loader, model, self.render, name, tex,
                   Point3(x, y, z), Vec3(100, 100, 100), self.traverser, self.pusher)

    def spawn_drones(self):
        print("DEPLOYING DRONES...")
        texture_path = "Assets/DroneDefender/Drones.jpg"
        positions = get_all_defense_positions(self.ship.model.getPos(), self.station.model.getPos())
        for pos in positions:
            Drone(self.loader, self.render, Point3(*pos), texture_path,
                  self.traverser, self.pusher, player_ref=self.ship)

    def spawn_orbiters(self):
        print("SPAWNING ORBITERS...")
        texture_path = "Assets/DroneDefender/Drones.jpg"
        model_path = "Assets/DroneDefender/DroneDefender.x"
        Orbiter(self.loader, self.taskMgr, model_path, self.render,
                "Orbiter", 40, texture_path, self.station.model, 4000, "MLB",
                self.station.model, self.traverser, self.pusher, player_ref=self.ship)
        swarm_size_0 = random.randint(5, 10)
        for _ in range(swarm_size_0):
            Orbiter(self.loader, self.taskMgr, model_path, self.render,
                    "Orbiter", 40, texture_path, self.station.model, 4000, "Cloud",
                    self.station.model, self.traverser, self.pusher, player_ref=self.ship, cloud_group=0)
        swarm_size_1 = random.randint(5, 10)
        for _ in range(swarm_size_1):
            Orbiter(self.loader, self.taskMgr, model_path, self.render,
                    "Orbiter", 40, texture_path, self.station.model, 4000, "Cloud",
                    self.station.model, self.traverser, self.pusher, player_ref=self.ship, cloud_group=1)

    def spawn_wanderers(self):
        print("SPAWNING WANDERERS...")
        for _ in range(2):
            Wanderer(self.loader, self.render, self.traverser, self.pusher, player_ref=self.ship)

    def update_laser(self, task):
        if self.ship.laser_firing:
            pass
        return task.cont

# RUN APP
app = SpaceJam()
app.run()
