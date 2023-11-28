import pygame
import sys
import math

# Pygame 초기화
pygame.init()

# 화면 크기 및 색상 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SAT Collision Detection")
# 시간 설정
clock = pygame.time.Clock()
FPS = 60 # 시간 당 프레임
# 색상 정의
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0,0,0)

# 원점을 화면의 중앙으로 삼기 위한 세팅
originx = width / 2
originy = height / 2

# 다각형 정점 좌표
polygon1 = [[100, 100], [200, 100], [130, 200]]
polygon2 = [[-300, -150], [-350, -100], [-400, -150], [-400, -200], [-350, -250], [-300, -200]]

def project_polygon(axis, polygon):
    """다각형을 축에 사영한 결과를 반환합니다."""
    min_proj = float('inf')
    max_proj = float('-inf')

    for point in polygon:
        dot_product = axis[0] * point[0] + axis[1] * point[1]
        min_proj = min(min_proj, dot_product)
        max_proj = max(max_proj, dot_product)

    return min_proj, max_proj

def get_axes(polygon):
    """다각형의 변에 대한 노말축을 반환합니다."""
    axes = []
    for i in range(len(polygon)):
        point1 = polygon[i]
        point2 = polygon[(i + 1) % len(polygon)]
        edge = [point1[0] - point2[0], point1[1] - point2[1]]
        normal = [edge[1], -edge[0]]
        length = math.sqrt(normal[0]**2 + normal[1]**2)
        axis = [normal[0] / length, normal[1] / length]
        axes.append(axis)
    
    return axes

def check_collision(polygon1, polygon2):
    """두 다각형이 충돌하는지 여부를 확인합니다."""
    axes = get_axes(polygon1) + get_axes(polygon2)

    for axis in axes:
        min_proj1, max_proj1 = project_polygon(axis, polygon1)
        min_proj2, max_proj2 = project_polygon(axis, polygon2)

        if max_proj1 < min_proj2 or max_proj2 < min_proj1:
            # 축 사이에 갭이 있으면 충돌하지 않음
            return False

    return True

def draw_SAT(polygon1, polygon2):
    """두 다각형의 각 선의 직교 벡터를 화면 중앙을 원점으로 시각화"""
    axes = get_axes(polygon1) + get_axes(polygon2)
    for axis in axes:
        x1 = (axis[0]* 1000 + originx) 
        y1 = (axis[1]* 1000 + originy) 
        x2 = (axis[0]* -1000 + originx) 
        y2 = (axis[1]* -1000 + originy)
        pygame.draw.aaline(screen, black, [x1, y1], [x2, y2])
        """두 다각형이 축에 내적된 결과인 선을 시각화"""
        min_proj1 , max_proj1 = project_polygon(axis, polygon1)
        proj1_x1 = (axis[0]* min_proj1 + originx)
        proj1_y1 = (axis[1]* min_proj1 + originy)
        proj1_x2 = (axis[0]* max_proj1 + originx)
        proj1_y2 = (axis[1]* max_proj1 + originy)
        
        min_proj2 , max_proj2 = project_polygon(axis, polygon2)
        proj2_x1 = (axis[0]* min_proj2 + originx)
        proj2_y1 = (axis[1]* min_proj2 + originy)
        proj2_x2 = (axis[0]* max_proj2 + originx)
        proj2_y2 = (axis[1]* max_proj2 + originy)
        # 선끼리의 충돌 판정
        if max_proj1 < min_proj2 or max_proj2 < min_proj1:
            # 내적된 선이 서로 충돌하지 않으면 초록색
            pygame.draw.line(screen, green, [proj1_x1, proj1_y1], [proj1_x2, proj1_y2],5)
            pygame.draw.line(screen, green, [proj2_x1, proj2_y1], [proj2_x2, proj2_y2],5)
        else:
            # 충돌하면 빨간색
            pygame.draw.line(screen, red, [proj1_x1, proj1_y1], [proj1_x2, proj1_y2],5)
            pygame.draw.line(screen, red, [proj2_x1, proj2_y1], [proj2_x2, proj2_y2],5)

def draw_neworigin_polygon(polygon, color = green):
    newpolygon = []
    for point in polygon:
        newpolygon.append([point[0] + originx, point[1] + originy])
    pygame.draw.polygon(screen, color, newpolygon)
    

# 게임 루프
while True:
    clock.tick(FPS)  # 프레임 제한
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        for i in range(len(polygon1)):
            polygon1[i][0] -= 1
    if keys[pygame.K_RIGHT]:
        for i in range(len(polygon1)):
            polygon1[i][0] += 1
    if keys[pygame.K_UP]:
        for i in range(len(polygon1)):
            polygon1[i][1] -= 1 
    if keys[pygame.K_DOWN]:
        for i in range(len(polygon1)):
            polygon1[i][1] += 1 
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        for i in range(len(polygon2)):
            polygon2[i][0] -= 1
    if keys[pygame.K_d]:
        for i in range(len(polygon2)):
            polygon2[i][0] += 1
    if keys[pygame.K_w]:
        for i in range(len(polygon2)):
            polygon2[i][1] -= 1 
    if keys[pygame.K_s]:
        for i in range(len(polygon2)):
            polygon2[i][1] += 1 
    # 충돌 감지
    collision = check_collision(polygon1, polygon2)

    # 화면 그리기
    screen.fill(white)
    # pygame.draw.polygon(screen, green, polygon1)
    # pygame.draw.polygon(screen, green, polygon2)
    draw_neworigin_polygon(polygon1)
    draw_neworigin_polygon(polygon2)
    draw_SAT(polygon1, polygon2)
    # 충돌 시 색상 변경
    if collision:
        draw_neworigin_polygon(polygon1, red)
        draw_neworigin_polygon(polygon2, red)

    pygame.display.flip()

# 코드 실행
pygame.quit()
