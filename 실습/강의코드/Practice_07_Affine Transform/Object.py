from Mesh3D import *
from Transform import *
from Button import *
from Grid import *
from DisplayNormals import *


class Object:
    def __init__(self, obj_name):
        self.name = obj_name
        self.components = []
        self.scene_angle = 45

    def add_component(self, component):
        if isinstance(component, Transform):
            self.components.insert(0, self.components)
        self.components.append(component)

    def get_component(self, class_type):
        for c in self.components:
            if type(c) is class_type:
                return c
        return None


    def update(self, events = None):
        glPushMatrix()
        for c in self.components:
            if isinstance(c, Transform):
                pos = c.get_position()
                scale = c.get_scale()
                rot_angle = c.get_rotation_angle()
                rot_axis = c.get_rotation_axis()
            # 카메라를 중심으로 오브젝트가 빙빙돈다.
            # Testing Transformation Order 
                glRotated(rot_angle, rot_axis.x, rot_axis.y, rot_axis.z)
                glTranslatef(pos.x, pos.y, pos.z)
                glScalef(scale.x, scale.y, scale.z)
            # 아래 주석은 오브젝트가 제자리서 회전한다.
                # glTranslatef(pos.x, pos.y, pos.z)
                # glRotated(rot_angle, rot_axis.x, rot_axis.y, rot_axis.z)
                # glScalef(scale.x, scale.y, scale.z)
                
                mv = glGetDoublev(GL_MODELVIEW_MATRIX)
                print("MV: ")
                print(mv)

            elif isinstance(c, Mesh3D):
                glColor(1, 1, 1)
                c.draw()
            elif isinstance(c, Grid):
                c.draw()
            elif isinstance(c, DisplayNormals):
                c.draw()
            elif isinstance(c, Button):
                c.draw(events)
        glPopMatrix()
