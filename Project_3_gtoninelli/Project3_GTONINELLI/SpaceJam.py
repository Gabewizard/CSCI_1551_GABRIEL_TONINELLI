# GABRIEL F. TONINELLI - PROJECT3 - CSCI-1551

from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, AmbientLight, Point3, Vec3
from math import sin, cos, pi
from SpaceJamClasses import Universe, SpaceStation, Spaceship, Drone, Planet
from DefensePaths import get_all_defense_positions

class SpaceJam(ShowBase):
    def __init__(self):
        print("LAUNCHING SPACEJAM...")
        super().__init__()

        self.disableMouse()
        self.setBackgroundColor(0.1, 0.1, 0.1)
        self.setup_lights()

        self.universe = Universe(self.loader, self.camera)
        self.station = SpaceStation(self.loader, self.render)
        self.ship = Spaceship(self.loader, self.render)

        self.set_camera()

        self.spawn_planets()
        print("DEPLOYING DRONES...")
        self.spawn_drones()

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
        self.camera.setPos(0, -40, 10)
        self.camera.lookAt(self.ship.model)

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

    def spawn_drones(self):
        texture_path = "Assets/DroneDefender/Drones.jpg"
        positions = get_all_defense_positions(self.ship.model.getPos(), self.station.model.getPos())
        for pos in positions:
            Drone(self.loader, self.render, Point3(*pos), texture_path)

app = SpaceJam()
app.run()
