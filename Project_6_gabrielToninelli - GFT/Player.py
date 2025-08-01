# GABRIEL F. TONINELLI
import os, random, re
from panda3d.core import Vec3, TransparencyAttrib, CollisionHandlerEvent, Material, WindowProperties
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import LerpScaleInterval, LerpColorScaleInterval, Sequence, Parallel, Func
from CollideObjectBase import SphereCollideObject
from SpaceJamClasses import Missile, Drone, SpaceStation

class Spaceship(SphereCollideObject, DirectObject.DirectObject):
    def __init__(self, loader, parent, traverser, pusher):
        DirectObject.DirectObject.__init__(self)
        self.loader = loader
        self.parent = parent
        self.traverser = traverser
        self.pusher = pusher

        # Ship model
        self.model = loader.loadModel("Assets/Dumbledore/Dumbledore.x")
        tex = loader.loadTexture("Assets/Dumbledore/spacejet_C.png")
        self.model.setTexture(tex, 1)
        self.model.setScale(10)
        self.model.setTwoSided(True)
        self.model.reparentTo(parent)

        super().__init__(self.model, "Player", radius=6,
                         parent=parent, traverser=traverser, pusher=pusher, is_dynamic=True)

        # Gameplay
        self.reloadTime = 0.1
        self.missileDistance = 5200
        self.missileBay = 1
        self.firing = False

        # Score
        self.score = 0
        self.score_text = OnscreenText(text=f"Score: {self.score}",
                                       pos=(-1.3, 0.9), scale=0.07,
                                       fg=(1, 1, 1, 1), align=0)

        self.set_key_bindings()
        self.setup_collision_handler()
        self.EnableHUD()

        # Enable mouse movement
        self.enable_mouse_control()

    def update_score(self, points):
        self.score += points
        self.score_text.setText(f"Score: {self.score}")

    def setup_collision_handler(self):
        self.handler = CollisionHandlerEvent()
        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)

    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        intoNode = entry.getIntoNodePath().getName()
        hit_pos = entry.getSurfacePoint(render)

        print(f"Collision detected: {fromNode} hit {intoNode} at {hit_pos}")

        missile_parts = fromNode.split('-')
        missile_id = missile_parts[0] + "-" + missile_parts[1] if len(missile_parts) > 1 else missile_parts[0]

        victim_name = intoNode.split('-')[0]
        victim_base = re.sub(r'[0-9]', '', victim_name)

        if victim_base in ["Drone", "Planet", "Station", "Earth", "Mars", "AlienPlanet", "Venus", "Moon", "Mercury"]:
            self.spawn_self_emitting_explosion(hit_pos)

            if victim_base == "Drone":
                drone_node = render.find(f"**/{victim_name}")
                if not drone_node.isEmpty():
                    drone_instance = drone_node.getPythonTag("drone_instance")
                    if isinstance(drone_instance, Drone):
                        drone_instance.take_damage(50)

            elif victim_base == "Station":
                station_node = render.find(f"**/{victim_name}")
                if not station_node.isEmpty():
                    station_instance = station_node.getPythonTag("station_instance")
                    if isinstance(station_instance, SpaceStation):
                        station_instance.apply_damage_from_player(50)

            self.cleanup_missile(missile_id)

    def spawn_self_emitting_explosion(self, position):
        pos_above = position + Vec3(0, 0, 10)

        flash = loader.loadModel("models/misc/sphere")
        flash.setPos(pos_above)
        flash.setScale(5)
        flash.setTransparency(TransparencyAttrib.MAlpha)
        mat_flash = Material()
        mat_flash.setEmission((1, 1, 1, 1))
        flash.setMaterial(mat_flash, 1)
        flash.reparentTo(render)
        Sequence(LerpScaleInterval(flash, 0.15, 30), Func(flash.removeNode)).start()

        for i in range(random.randint(3, 4)):
            sphere = loader.loadModel("models/misc/sphere")
            sphere.setPos(pos_above + Vec3(random.uniform(-3, 3),
                                           random.uniform(-3, 3),
                                           random.uniform(-1, 1)))
            sphere.setScale(random.uniform(3, 5))
            sphere.setTransparency(TransparencyAttrib.MAlpha)
            mat = Material()
            mat.setEmission((1, 1, 0.6, 1))
            sphere.setMaterial(mat, 1)
            sphere.reparentTo(render)

            grow = LerpScaleInterval(sphere, 0.4, sphere.getScale() * random.uniform(4, 6))
            fade_to_orange = LerpColorScaleInterval(sphere, 0.2, (1, 0.5, 0.2, 1))
            fade_out = LerpColorScaleInterval(sphere, 0.6, (1, 0.3, 0, 0))
            Sequence(Parallel(grow, fade_to_orange), fade_out, Func(sphere.removeNode)).start()

    def cleanup_missile(self, missile_id):
        if missile_id in Missile.intervals:
            Missile.intervals[missile_id].finish()
        if missile_id in Missile.fireModels:
            Missile.fireModels[missile_id].removeNode()
        if missile_id in Missile.collisionNodes:
            Missile.collisionNodes[missile_id].removeNode()
        if missile_id in Missile.collisionSolids:
            del Missile.collisionSolids[missile_id]

        Missile.intervals.pop(missile_id, None)
        Missile.fireModels.pop(missile_id, None)
        Missile.collisionNodes.pop(missile_id, None)

    def set_key_bindings(self):
        base.accept("w", self.move_forward, [True])
        base.accept("w-up", self.move_forward, [False])
        base.accept("s", self.move_backward, [True])
        base.accept("s-up", self.move_backward, [False])
        base.accept("a", self.move_left, [True])  # Strafe left now on A
        base.accept("a-up", self.move_left, [False])
        base.accept("d", self.move_right, [True]) # Strafe right now on D
        base.accept("d-up", self.move_right, [False])
        base.accept("arrow_up", self.pitch_up, [True])
        base.accept("arrow_up-up", self.pitch_up, [False])
        base.accept("arrow_down", self.pitch_down, [True])
        base.accept("arrow_down-up", self.pitch_down, [False])
        base.accept("q", self.roll_left, [True])
        base.accept("q-up", self.roll_left, [False])
        base.accept("e", self.roll_right, [True])
        base.accept("e-up", self.roll_right, [False])
        base.accept("space", self.start_firing)
        base.accept("space-up", self.stop_firing)
        base.accept("escape", self.disable_mouse_control)

    # -------- Mouse Control --------
    def enable_mouse_control(self):
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        base.disableMouse()
        taskMgr.add(self.mouse_control_task, "mouse-control-task")

    def disable_mouse_control(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        taskMgr.remove("mouse-control-task")

    def mouse_control_task(self, task):
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()

            yaw_sensitivity = 750
            pitch_sensitivity = 750

            self.model.setH(self.model.getH() - x * yaw_sensitivity * globalClock.getDt())
            self.model.setP(self.model.getP() + y * pitch_sensitivity * globalClock.getDt())

            base.win.movePointer(
                0,
                int(base.win.getProperties().getXSize() / 2),
                int(base.win.getProperties().getYSize() / 2)
            )
        return task.cont
    # ------------------------------

    def start_firing(self):
        self.firing = True
        taskMgr.add(self.fire_loop, "auto-fire-loop")

    def stop_firing(self):
        self.firing = False
        taskMgr.remove("auto-fire-loop")

    def fire_loop(self, task):
        if self.firing:
            self.Fire()
            return task.again
        return task.done

    def Fire(self):
        if self.missileBay:
            print("Missile Fired")
            aim = render.getRelativeVector(self.model, Vec3.forward())
            aim.normalize()
            fireSolution = aim * self.missileDistance
            inFront = aim * 150
            travVec = fireSolution + self.model.getPos()
            posVec = self.model.getPos() + inFront

            self.missileBay -= 1
            tag = "Missile-" + str(Missile.missileCount + 1)

            missile = Missile(self.loader, "Assets/Phaser/phaser.egg", tag, render,
                              base.camera, posVec, 1.0, self.traverser, self.pusher)

            self.traverser.addCollider(missile.collisionNode, self.handler)
            Missile.intervals[tag] = missile.model.posInterval(4.0, travVec, posVec, fluid=1)
            Missile.intervals[tag].start()

            taskMgr.doMethodLater(self.reloadTime, self.Reload, 'reload')
        else:
            if not taskMgr.hasTaskNamed('reload'):
                taskMgr.doMethodLater(self.reloadTime, self.Reload, 'reload')

    def Reload(self, task):
        self.missileBay = 1
        print("Reload Complete")
        return task.done

    def CheckIntervals(self, task):
        for missile in list(Missile.intervals.keys()):
            if not Missile.intervals[missile].isPlaying():
                Missile.collisionNodes[missile].removeNode()
                Missile.fireModels[missile].removeNode()
                del Missile.intervals[missile]
                del Missile.fireModels[missile]
                del Missile.collisionNodes[missile]
                del Missile.collisionSolids[missile]
                break
        return task.cont

    def EnableHUD(self):
        self.crosshair = OnscreenImage(
            image="Hud/Reticle3b.png",
            pos=(0.00, 0, 0.275),
            scale=(0.275, 0.85, 0.035)  # Width, Y-scale, Height
        )
        self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
        self.crosshair.setAlphaScale(0.3)  # 50% transparent

    def move_forward(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_forward, "move-forward")
        else:
            taskMgr.remove("move-forward")

    def apply_forward(self, task):
        direction = self.model.getQuat().getForward()
        self.model.setFluidPos(self.model.getPos() + direction * 20)
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

    def move_left(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_move_left, "move-left")
        else:
            taskMgr.remove("move-left")

    def apply_move_left(self, task):
        direction = self.model.getQuat().getRight()
        self.model.setFluidPos(self.model.getPos() - direction * 15)
        return Task.cont

    def move_right(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_move_right, "move-right")
        else:
            taskMgr.remove("move-right")

    def apply_move_right(self, task):
        direction = self.model.getQuat().getRight()
        self.model.setFluidPos(self.model.getPos() + direction * 15)
        return Task.cont

    def pitch_up(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_pitch_up, "pitch-up")
        else:
            taskMgr.remove("pitch-up")

    def apply_pitch_up(self, task):
        self.model.setP(self.model.getP() + 1.5)
        return Task.cont

    def pitch_down(self, keyDown):
        if keyDown:
            taskMgr.add(self.apply_pitch_down, "pitch-down")
        else:
            taskMgr.remove("pitch-down")

    def apply_pitch_down(self, task):
        self.model.setP(self.model.getP() - 1.5)
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
