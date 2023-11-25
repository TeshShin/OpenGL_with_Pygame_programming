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


def rotation_Yaw(angle):
    # y 축을 기준으로 각도를 라디안으로 변환
    angle = math.radians(angle)

    # Yaw 회전 행렬 생성
    rotation_matrix = np.array([[math.cos(angle), 0, math.sin(angle)],
                                   [0, 1, 0],
                                   [-math.sin(angle), 0, math.cos(angle)]])

    for i in range(len(vertices)):
        vertices[i] = (np.dot(rotation_matrix, np.array(vertices[i]))).tolist()

    normals.clear()
    for tri in triangles:
        v1 = vertices[tri[0]]
        v2 = vertices[tri[1]]
        v3 = vertices[tri[2]]
        normal = calculate_normal(v1, v2, v3)
        normals.append(normal)


def rotation_Pitch(angle):
    # x 축을 기준으로 각도를 라디안으로 변환
    angle = math.radians(angle)

    # Pitch 회전 행렬 생성
    rotation_matrix = np.array([[1, 0, 0],
                                   [0, math.cos(angle), -math.sin(angle)],
                                   [0, math.sin(angle), math.cos(angle)]])

    for i in range(len(vertices)):
        vertices[i] = (np.dot(rotation_matrix, np.array(vertices[i]))).tolist()

    normals.clear()
    for tri in triangles:
        v1 = vertices[tri[0]]
        v2 = vertices[tri[1]]
        v3 = vertices[tri[2]]
        normal = calculate_normal(v1, v2, v3)
        normals.append(normal)
    

def rotation_Roll(angle):
    # z 축을 기준으로 각도를 라디안으로 변환
    angle = math.radians(angle)

    # roll 회전 행렬 생성
    rotation_matrix = np.array([[math.cos(angle),  -math.sin(angle), 0],
                                   [ math.sin(angle),  math.cos(angle),0],
                                   [0,0,1]])

    for i in range(len(vertices)):
        vertices[i] = (np.dot(rotation_matrix, np.array(vertices[i]))).tolist()

    normals.clear()
    for tri in triangles:
        v1 = vertices[tri[0]]
        v2 = vertices[tri[1]]
        v3 = vertices[tri[2]]
        normal = calculate_normal(v1, v2, v3)
        normals.append(normal)
   

def main():
    once = False

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glMatrixMode(GL_PROJECTION)  # 투영 모드로 전환
    glLoadIdentity()  # 현재 행렬을 단위 행렬로 초기화
    gluPerspective(30, (800 / 600), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)  # 모델뷰 모드로 전환
    glLoadIdentity()  # 현재 행렬을 단위 행렬로 초기화

    glTranslatef(3, -2, -20)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    #glRotatef(45, 0, 45, 0)
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        

        check = "Case1"
        
        if(check=="Case1"):
            if(once == False):

                rotation_Roll(90)
                rotation_Pitch(-90)

                #rotation_Roll(270)
                #rotation_Pitch(30)
                #rotation_Yaw(-20)
                once = True
                
            rotation_Yaw(0.1)

        elif(check=="Case2"):
            rotation_Roll(0.1)
            
            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()

        pygame.display.flip()
        pygame.time.wait(10)
        
        
    pygame.quit()

main()