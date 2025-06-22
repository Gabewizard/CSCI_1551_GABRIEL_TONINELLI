# GABRIEL F. TONINELLI - PROJECT1 - CSCI-1551

from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, Filename, AmbientLight, Point3, Vec3
from direct.task import Task
from math import sin, cos, pi

class SpaceJam(ShowBase):
    def __init__(self):
        print("Initializing SpaceJam...")
        super().__init__()

        # DISABLE MOUSE CAMERA CONTROL
        self.disableMouse()

        # SETUP CONTROLS AND SCENE
        self.setup_controls()
        self.setup_scene()

        # MOUSE WHEEL ZOOM
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)

        # ADD CAMERA MOVEMENT TASK
        self.taskMgr.add(self.update_camera, "UpdateCameraTask")

        print("Initialization complete.")

    # LOAD AND SCALE A MODEL WITH TEXTURE
    def load_scaled_obj(self, model_path, texture_path=None, scale=1, pos=(0, 0, 0), normalize=False, target_size=10):
        try:
            print(f"Loading model: {model_path}")
            model = self.loader.loadModel(Filename.fromOsSpecific(model_path))
            
            # APPLY NORMALIZATION IF REQUESTED
            if normalize:
                bounds = model.getBounds()
                if not bounds.isEmpty():
                    current_size = bounds.getRadius() * 2
                    if current_size > 0:
                        scale_factor = (target_size * 5) / current_size  # 5x multiplier for planets
                        model.setScale(scale_factor)
                        print(f"Normalized scale for {model_path}: {scale_factor:.2f}")
            else:
                # REGULAR SCALING (5x for most objects)
                model.setScale(scale * 5)
            
            model.setPos(pos[0] * 5, pos[1] * 5, pos[2] * 5)  # Scale positions too
            model.reparentTo(self.render)

            if texture_path:
                tex = self.loader.loadTexture(Filename.fromOsSpecific(texture_path))
                model.setTexture(tex, 1)

            model.setTwoSided(True)
            return model
        except Exception as e:
            print(f"Error loading model: {model_path}\n{str(e)}")
            return None

    # SETUP ALL MODELS AND LIGHTING
    def setup_scene(self):
        print("Setting up scene...")

        # BACKGROUND COLOR
        self.setBackgroundColor(0.1, 0.1, 0.1)

        # AMBIENT LIGHT
        ambient = AmbientLight("ambient")
        ambient.setColor((0.3, 0.3, 0.3, 1))
        self.render.setLight(self.render.attachNewNode(ambient))

        # DIRECTIONAL LIGHT
        dlight = DirectionalLight("sun")
        dlight.setColor((0.8, 0.8, 0.7, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(45, -60, 0)
        self.render.setLight(dlnp)

        # CAMERA POSITION (SCALED UP 5X)
        self.camera.setPos(0, -2000, 750)  # Originally (0, -400, 150) * 5
        self.camera.lookAt(0, 0, 0)

        # UNIVERSE BACKGROUND (SCALED UP 5X)
        universe = self.loader.loadModel(Filename.fromOsSpecific("Assets/Universe/Universe.obj"))
        universe.setScale(7500)  # Originally 1500 * 5
        universe.setTexture(self.loader.loadTexture(Filename.fromOsSpecific("Assets/Universe/starfield-in-blue.jpg")), 1)
        universe.setBin("background", 0)
        universe.setDepthWrite(False)
        universe.setTwoSided(True)
        universe.reparentTo(self.camera)
        print("Universe loaded and set as background.")

        # PLANET LIST
        planet_data = [
            ("AlienPlanet", "Assets/Planets/AlienPlanet/AlienPlanet.obj", "Assets/Planets/AlienPlanet/planet_Bog1200.png"),
            ("Earth",       "Assets/Planets/Earth/Earth 2K.obj",          "Assets/Planets/Earth/Diffuse_2K.png"),
            ("Mars",        "Assets/Planets/Mars/Mars 2K.obj",            "Assets/Planets/Mars/Diffuse_2K.png"),
            ("Mercury",     "Assets/Planets/Mercury/Mercury 1K.obj",      "Assets/Planets/Mercury/Diffuse_1K.png"),
            ("Moon",        "Assets/Planets/Moon/Moon 2K.obj",            "Assets/Planets/Moon/Diffuse_2K.png"),
            ("Venus",       "Assets/Planets/Venus/Venus_1K.obj",          "Assets/Planets/Venus/Diffuse_1K.png"),
        ]

        # ARRANGE PLANETS IN CIRCLE (SCALED UP 5X)
        radius = 1750  # Originally 350 * 5
        angle_increment = 2 * pi / len(planet_data)
        target_planet_size = 50  # Originally 10 * 5

        for i, (name, model, tex) in enumerate(planet_data):
            angle = i * angle_increment
            x = radius * cos(angle)
            y = radius * sin(angle)
            z = 0
            planet = self.load_scaled_obj(model, tex, normalize=True, target_size=target_planet_size, pos=(x/5, y/5, z))
            if not planet:
                print(f"Planet {name} failed to load")
            else:
                print(f"Planet {name} positioned at ({x:.1f}, {y:.1f}, {z:.1f})")

        # LOAD SPACE STATION (ORIGINAL SCALE - NOT NORMALIZED)
        station = self.load_scaled_obj(
            "Assets/SpaceStation1B/spaceStation.x",
            "Assets/SpaceStation1B/SpaceStation1_Dif2.png",
            scale=6,  # Original scale
            pos=(0, 300, 0),  # Position will be multiplied by 5
            normalize=False  # Don't normalize - keep original scale
        )
        if not station:
            print("Space station failed to load")

        # LOAD PLAYER SPACESHIP (ORIGINAL SCALE - NOT NORMALIZED)
        self.spaceship = self.load_scaled_obj(
            "Assets/Dumbledore/Dumbledore.x",
            "Assets/Dumbledore/spacejet_C.png",
            scale=5,  # Original scale
            pos=(0, 0, 0),  # Position will be multiplied by 5
            normalize=False  # Don't normalize - keep original scale
        )
        if not self.spaceship:
            print("Critical error: Player spaceship failed to load")
        else:
            print("Player spaceship loaded.")

        print("Scene setup complete.")

    # KEYBOARD CONTROLS
    def setup_controls(self):
        print("Setting up controls...")
        self.key_map = {"w": False, "s": False, "a": False, "d": False}

        for key in self.key_map:
            self.accept(key, self.set_key, [key, True])
            self.accept(f"{key}-up", self.set_key, [key, False])

        self.cam_speed = 25  # Originally 5 * 5
        self.zoom_step = 125  # Originally 25 * 5

    # SET KEY STATE
    def set_key(self, key, value):
        self.key_map[key] = value

    # ZOOM CAMERA IN
    def zoom_in(self):
        self.camera.setY(self.camera, self.zoom_step)

    # ZOOM CAMERA OUT
    def zoom_out(self):
        self.camera.setY(self.camera, -self.zoom_step)

    # UPDATE CAMERA POSITION BASED ON KEY INPUT
    def update_camera(self, task):
        dt = globalClock.getDt()
        if self.key_map["w"]:
            self.camera.setZ(self.camera, self.cam_speed * dt * 60)
        if self.key_map["s"]:
            self.camera.setZ(self.camera, -self.cam_speed * dt * 60)
        if self.key_map["a"]:
            self.camera.setX(self.camera, -self.cam_speed * dt * 60)
        if self.key_map["d"]:
            self.camera.setX(self.camera, self.cam_speed * dt * 60)
        return Task.cont

# RUN GAME
print("Launching SpaceJam...")
game = SpaceJam()
game.run()