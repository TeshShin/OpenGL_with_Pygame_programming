import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

vertices = [[1,-1,1], [1,-1,-1],[1,1,-1], [1,1,1],
            [-1,-1,1], [-1,-1,-1], [-1,1,-1], [-1,1,1]]
triangles = [[4,0,3], [4,3,7], [0,1,2],[0,2,3],[1,5,6],[1,6,2],
             [5,4,7],[5,7,6],[7,3,2],[7,2,6],[0,5,1],[0,4,5]]
colors = [[1,0,0],[1,0,0],[1,0,1],[1,0,1],[0,1,0],[0,1,0],
          [0,0,1],[0,0,1],[0,1,1],[0,1,1],[1,1,1],[1,1,1]]

normals = []

def calculate_normal(v1,v2,v3):
    vector1 = np.array(v2) - np.array(v1)
    vector2 = np.array(v3) - np.array(v1)
    cross_product = np.cross(vector1, vector2)
    normalized_cross_product = cross_product / np.linalg.norm(cross_product)
    return normalized_cross_product

for tri in triangles:
    v1 = vertices[tri[0]]
    v2 = vertices[tri[1]]
    v3 = vertices[tri[2]]
    normal = calculate_normal(v1, v2,v3)
    normals.append(normal)

def Cube():
    # glEnable(GL_CULL_FACE)
    # glFrontFace(GL_CCW)
    glBegin(GL_TRIANGLES)
    i = 0
    for tri in triangles:
        glColor3fv(colors[i])
        glVertex3fv(vertices[tri[0]])
        glVertex3fv(vertices[tri[1]])
        glVertex3fv(vertices[tri[2]])
        i+=1
    glEnd()

# Function to draw a circle
def draw_circle(radius, num_vertices):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0, 0)
    for i in range(num_vertices + 1):
        angle = 2 * math.pi * i / num_vertices
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()

def rotation_Yaw(angle):
    # Yaw 축을 기준으로 각도를 라디안으로 변환
    angle = math.radians(angle)

    # Yaw 회전 행렬 생성
    yaw_rotation_matrix = np.array([[math.cos(angle), 0, math.sin(angle)],
                                   [0, 1, 0],
                                   [-math.sin(angle), 0, math.cos(angle)]])

    for i in range(len(vertices)):
        vertices[i] = (np.dot(yaw_rotation_matrix, np.array(vertices[i]))).tolist()

    normals.clear()
    for tri in triangles:
        v1 = vertices[tri[0]]
        v2 = vertices[tri[1]]
        v3 = vertices[tri[2]]
        normal = calculate_normal(v1, v2, v3)
        normals.append(normal)


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glMatrixMode(GL_PROJECTION)  # 투영 모드로 전환
    glLoadIdentity()  # 현재 행렬을 단위 행렬로 초기화
    gluPerspective(30, (800 / 600), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)  # 모델뷰 모드로 전환
    glLoadIdentity()  # 현재 행렬을 단위 행렬로 초기화

    glTranslatef(0, -2.5, -20)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    light_pos = [-1.8, 1.1, 0]
    light_color = np.array([0, 1, 1])
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_LEFT:
                    light_pos[0] -= 0.5
                if event.key ==pygame.K_RIGHT:
                    light_pos[0] += 0.5
                if event.key ==pygame.K_UP:
                    light_pos[2] -= 0.5
                if event.key ==pygame.K_DOWN:
                    light_pos[2] += 0.5
                if event.key == pygame.K_q:
                    light_pos[1] -= 0.5
                if event.key == pygame.K_e:
                    light_pos[1] += 0.5
        #glRotatef(1, 0, 1, 0)
        # ======================

        '''
        triangles[0][0] # vertex 4, colors[0], normals[0]
        triangles[0][1]  # vertex 0, colors[0], normals[0]
        triangles[0][2]  # vertex 3, colors[0], normals[0]
        '''

        for i in range(len(triangles)):
            new_color = 0
            for j in range(1):
                l = np.array(light_pos) - np.array(vertices[triangles[i][j]])
                l_norm = l/np.linalg.norm(l)
                shading = np.clip(np.dot(normals[i], l_norm), 0.0,1.0)
                new_color += light_color*shading

            colors[i] = new_color.tolist()

        # ======================
        rotation_Yaw(0.1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()

        # Draw Light
        glPushMatrix()
        glTranslatef(light_pos[0], light_pos[1], light_pos[2])  # light pos
        glColor3f(light_color.tolist()[0],light_color.tolist()[1],light_color.tolist()[2])  # light color
        draw_circle(0.1, 100)
        glPopMatrix()




        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()

main()