# GABRIEL F. TONINELLI - PROJECT2 - CSCI-1551

from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, AmbientLight, Point3, Vec3, Filename, Mat3
from direct.task import Task
from math import sin, cos, pi
from SpaceJamClasses import Universe, SpaceStation, Spaceship, Drone, Planet
from DefensePaths import get_all_defense_positions

class SpaceJam(ShowBase):
    def __init__(self):
        print("LAUNCHING SPACEJAM...")
        super().__init__()

        # DISABLE MOUSE CONTROL
        self.disableMouse()

        # SETUP SCENE LIGHTING AND OBJECTS
        self.setBackgroundColor(0.1, 0.1, 0.1)
        self.setup_lights()

        # LOAD SCENE OBJECTS
        self.universe = Universe(self.loader, self.camera)
        self.station = SpaceStation(self.loader, self.render)
        self.ship = Spaceship(self.loader, self.render)

        # SET CAMERA START POSITION
        self.camera.setPos(0, -2000, 750)
        self.camera.lookAt(0, 0, 0)

        # CONTROLS AND CAMERA UPDATES
        self.setup_controls()
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)
        self.taskMgr.add(self.update_camera, "UpdateCamera")

        # SPAWN PLANETS AND DRONES
        self.spawn_planets()
        print("DEPLOYING DRONES...")
        self.spawn_drones()

    # SETUP SCENE LIGHTING
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

    # SPAWN PLANETS IN A CIRCLE
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
            Planet(self.loader, model, self.render, name, tex, Point3(x, y, z), Vec3(100, 100, 100))

    # SPAWN ALL DRONES BASED ON FORMATION LOGIC
    def spawn_drones(self):
        texture_path = "Assets/DroneDefender/Drones.jpg"
        positions = get_all_defense_positions(self.ship.model.getPos(), self.station.model.getPos())
        for i, pos in enumerate(positions):
            Drone(self.loader, self.render, Point3(*pos), texture_path)

    # SETUP KEYBOARD CONTROLS
    def setup_controls(self):
        self.key_map = {"w": False, "s": False, "a": False, "d": False, "q": False, "e": False}
        for key in self.key_map:
            self.accept(key, self.set_key, [key, True])
            self.accept(f"{key}-up", self.set_key, [key, False])
        self.cam_speed = 25
        self.zoom_step = 125

    # SET KEY STATE
    def set_key(self, key, value):
        self.key_map[key] = value

    # ZOOM CAMERA IN
    def zoom_in(self):
        self.camera.setY(self.camera, self.zoom_step)

    # ZOOM CAMERA OUT
    def zoom_out(self):
        self.camera.setY(self.camera, -self.zoom_step)

    # UPDATE CAMERA MOVEMENT AND ROTATION
    def update_camera(self, task):
        dt = globalClock.getDt()
        speed = self.cam_speed * dt * 60

        # WASD MOVEMENT
        if self.key_map["w"]:
            self.camera.setZ(self.camera, speed)
        if self.key_map["s"]:
            self.camera.setZ(self.camera, -speed)
        if self.key_map["a"]:
            self.camera.setX(self.camera, -speed)
        if self.key_map["d"]:
            self.camera.setX(self.camera, speed)

        # ORBIT CAMERA WITH Q/E AROUND ORIGIN
        pivot = Point3(0, 0, 0)
        cam_pos = self.camera.getPos()
        cam_vec = cam_pos - pivot

        if self.key_map["q"] or self.key_map["e"]:
            angle = 1.0 if self.key_map["q"] else -1.0
            rotation_matrix = Mat3.rotateMat(angle, Vec3(0, 0, 1))
            rotated_vec = rotation_matrix.xform(cam_vec)
            self.camera.setPos(pivot + rotated_vec)
            self.camera.lookAt(pivot)

        return Task.cont

# RUN GAME
app = SpaceJam()
app.run()
