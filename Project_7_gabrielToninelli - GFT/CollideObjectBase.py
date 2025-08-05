# GABRIEL F. TONINELLI - PROJECT6 - COLLISION BASE CLASSES
from panda3d.core import CollisionNode, CollisionSphere, CollisionHandlerPusher, CollisionTraverser

# BASE COLLIDABLE OBJECT
class SphereCollideObject:
    def __init__(self, model, name, radius, parent, traverser, pusher, is_dynamic=False):
        c_node = CollisionNode(name)
        c_node.addSolid(CollisionSphere(0, 0, 0, radius))
        c_np = model.attachNewNode(c_node)

        self.collisionNode = c_np  # Store collider reference for later use

        if is_dynamic:
            c_node.setFromCollideMask(1)
            c_node.setIntoCollideMask(1)
            pusher.addCollider(c_np, model)
        else:
            c_node.setFromCollideMask(0)
            c_node.setIntoCollideMask(1)

        traverser.addCollider(c_np, pusher)
