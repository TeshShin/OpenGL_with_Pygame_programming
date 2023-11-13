import math

from Object import *
from pygame.locals import *
from OpenGL.GLU import *
from Cube import *
from Camera import *

window_dimensions = (0, 800, 0, 600)
pygame.init()
screen_width = math.fabs(window_dimensions[1] - window_dimensions[0])
screen_height = math.fabs(window_dimensions[3] - window_dimensions[2])
pygame.display.set_caption('BackFaceCulling')
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
done = False
white = pygame.Color(255, 255, 255)

objects_3d = []

cube = Object("Cube")
cube.add_component(Transform())
cube.add_component(Cube(GL_LINE_LOOP, back_face_cull=True)) # False시, 폴리곤 다보임. back face cull이 안되므로


camera = Camera(60, (screen_width / screen_height), 0.1, 1000.0)
objects_3d.append(cube)
clock = pygame.time.Clock()
fps = 30



def set_3d():
    glMatrixMode(GL_PROJECTION)
    glLoadMatrixf(camera.get_PPM())
    #glLoadIdentity()
    #gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)
    #pv = glGetDoublev(GL_PROJECTION_MATRIX)
    #print("PV: ")
    #print(pv)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glLight(GL_LIGHT0, GL_POSITION, (5, 5, 5, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (1, 0, 1, 1))
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, (0, 1, 0, 1))
    # glLightfv(GL_LIGHT0, GL_SPECULAR, (0, 1, 0, 1))
    glEnable(GL_LIGHT0)


pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True

    glPushMatrix()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera.update()
    set_3d()

    for o in objects_3d:
        o.update(camera, events)


    glPopMatrix()
    pygame.display.flip()
    dt = clock.tick(fps)
pygame.quit()
