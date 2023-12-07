import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# OBJ 파일을 읽어서 정점, 면, 텍스처 좌표, 법선 벡터 정보를 추출하는 함수
def load_obj(file_path):
    vertices = []
    faces = []
    texture_coords = []
    normals = []
    with open(file_path, 'r') as file:
        for line in file: # 파일로부터 한 줄씩 얻어온다.
            if line.startswith('v '): # obj를 보면 v_ (_ = 띄어쓰기) 이후에 값들이 들어가 있다. 따라서 인덱스로 2부터 얻는다.
                vertices.append(list(map(float, line[2:].split()))) # split()은 문자열을 띄어쓰기로 구분하여 리스트로 만든다.
                #우리가 원하는 float값으로 바꿔주기 위해서 map을 사용하고, 다시 list로 변환해준다.
            elif line.startswith('vt '):
                texture_coords.append(list(map(float, line[3:].split()))) # vt_ 이므로 3부터
            elif line.startswith('vn '):
                normals.append(list(map(float, line[3:].split())))  # vn_이므로 3부터
            elif line.startswith('f '): # F는 v/vt/vn 의 인덱스들로 이루어져 있다.
                face_info = line[2:].split() # v/vt/vn 씩 얻기 (현재 읽으려는 model.obj는 v/vt/vn가 3개씩 들어있으므로 3개씩 들어감.)
                face = []
                texture_coord = []
                normal = []
                for vertex_info in face_info:
                    vertex_data = vertex_info.split('/') # v/vt/vn 씩 얻었으므로 /을 기준으로 나눔
                    face.append(int(vertex_data[0])) # v부터 
                    if len(vertex_data) >= 2 and vertex_data[1]:
                        texture_coord.append(int(vertex_data[1]))
                    if len(vertex_data) >= 3 and vertex_data[2]:
                        normal.append(int(vertex_data[2]))
                faces.append([face, texture_coord, normal])
    return vertices, faces, texture_coords, normals

# 텍스처를 로드하는 함수
def load_texture(texture_path):
    texture_surface = pygame.image.load(texture_path)
    texture_data = pygame.image.tostring(texture_surface, 'RGBA', 1) # 이미지를 바이트 버퍼로

    texture_id = glGenTextures(1) #  텍스처 이름을 생성.(사용할 텍스처는 하나이므로 1)
    glBindTexture(GL_TEXTURE_2D, texture_id) # 사용하려는 텍스처를 GL_TEXTURE_2D에 바인딩. = (이후에 GL_TEXTURE_2D에 세팅되는 것들이 texture_id에 적용됨.)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(), texture_surface.get_height(), 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    # 2차원 텍스처 이미지를 지정하는 함수. 각 매개변수에 알맞도록.

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # 텍스처 축소 함수는 텍스처 처리 중인 픽셀이 텍스처 요소보다 큰 영역에 매핑될 때마다 사용된다.
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # 텍스처화되는 픽셀이 하나의 텍스처 요소보다 작거나 같은 영역에 매핑될 때 사용된다.

    return texture_id

# OBJ 파일의 정점, 면, 텍스처 좌표, 법선 벡터 정보를 사용하여 모델을 그리는 함수
def draw_textured_obj(vertices, faces, texture_coords, normals, texture_id):
    glEnable(GL_TEXTURE_2D) # 텍스처를 적용할 수 있도록 GL_TEXTURE_2D 활성화
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL) # 텍스처 환경 매개 변수 설정
    glBindTexture(GL_TEXTURE_2D, texture_id) # GL_TEXTURE_2D에 texture_id 바인딩

    glBegin(GL_TRIANGLES)
    for face in faces:
        for i, vertex_index in enumerate(face[0]): # enumerate는 튜플인 (인덱스, 리스트의 원소) 형태로 반환한다.
            vertex = vertices[vertex_index - 1]
            texture_coord = texture_coords[face[1][i] - 1]
            normal = normals[face[2][i] - 1]
            # 현재 텍스처가 활성화 되어있으므로 glTexCoord2fv로 현재 텍스처 좌표를 설정한다.
            glTexCoord2fv(texture_coord)
            glNormal3fv(normal)
            glVertex3fv(vertex)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
# OBJ 파일의 정점과 면 정보를 사용하여 모델을 그리는 함수
def draw_obj(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex_index in face[0]: # 한 face엔 3개의 vertex_index가 있으므로, GL_TRIANGLES에 맞게 3번씩 glVertex3fv함.
            vertex = vertices[vertex_index - 1]
            glVertex3fv(vertex)
    glEnd()
    
# Pygame 초기화 및 화면 설정
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Obj load & Display")
# 카메라 및 뷰포트 설정
gluPerspective(45, (display[0] / display[1]), 0.1, 200.0)
glTranslatef(0.0, 0.0, -50)

# OBJ 파일 및 텍스처 파일 경로
first_obj_file_path = 'model.obj'
texture_file_path = 'face.png'

second_obj_file_path = 'teapot.obj'
# OBJ 파일 로드
first_vertices, first_faces, first_texture_coords, first_normals = load_obj(first_obj_file_path)

second_vertices, second_faces, _, _ = load_obj(second_obj_file_path)
# 텍스처 로드
texture_id = load_texture(texture_file_path)


# 초기 회전 각도 설정
rotation_angle1 = 0
rotation_angle2 = 0

# 메인 루프
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    glEnable(GL_DEPTH_TEST)  # 깊이 테스트 활성화
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # 여러 개의 모델에 원하는 transform을 위한 push&pop
    glPushMatrix()
    glRotatef(rotation_angle1, -1, 1, 0)  # 첫 번째 모델 회전
    glTranslatef(10.0, 10.0, 0.0)  # 첫 번째 모델의 위치 조정
    glRotatef(rotation_angle2, 3, 1, 1)  # 첫 번째 모델 회전
    draw_textured_obj(first_vertices, first_faces, first_texture_coords, first_normals, texture_id)
    glPopMatrix()

    
    glPushMatrix()
    glRotatef(rotation_angle2, 3, 1, 1)  # 두 번째 모델 회전
    glScalef(0.3,0.3,0.3)
    draw_obj(second_vertices, second_faces)
    glPopMatrix()
    
    # 회전 각도 갱신
    rotation_angle1 += 1
    rotation_angle2 += 5
    
    pygame.display.flip()
    pygame.time.wait(10)

