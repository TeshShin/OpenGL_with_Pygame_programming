from Mesh3D import *
from Transform import *
from Camera import *

class Object:
    def __init__(self, obj_name):
        self.name = obj_name
        self.components = []
        self.scene_angle = 0

    def add_component(self, component):
        if isinstance(component, Transform):
            self.components.insert(0, self.components)
        self.components.append(component)

    def get_component(self, class_type):
        for c in self.components:
            if type(c) is class_type:
                return c
        return None


    def update(self, camera: Camera, events = None):
        glPushMatrix()
        for c in self.components:
            if isinstance(c, Transform):
                glLoadMatrixf(c.get_MVM() * camera.get_VM())
            elif isinstance(c, Mesh3D):
                glColor(1, 1, 1)
                c.draw(camera.forward)
        glPopMatrix()
