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

# 다각형 정점 좌표
polygon1 = [[100, 100], [200, 100], [150, 200]]
polygon2 = [[300, 150], [400, 150], [350, 250], [300, 200]]

def transform_coordinates(x, y, screen_width, screen_height):
    center_x = screen_width // 2
    center_y = screen_height // 2
    transformed_x = x - center_x
    transformed_y = y - center_y
    return transformed_x, transformed_y

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

def draw_axis(polygon):
    axes = get_axes(polygon)
    for axis in axes:
        x = width / 2
        y = height / 2
        x1 = (axis[0]* 1000 + x) 
        y1 = (axis[1]* 1000 + y) 
        x2 = (axis[0]* -1000 + x) 
        y2 = (axis[1]* -1000 + y)
        
        min_proj , max_proj = project_polygon(axis, polygon)
        print(min_proj)
        proj_x1 = (axis[0]* min_proj + x)
        proj_y1 = (axis[1]* min_proj + y)
        proj_x2 = (axis[0]* max_proj + x)
        proj_y2 = (axis[1]* max_proj + y)
        pygame.draw.aaline(screen, black, [x1, y1], [x2, y2])
        pygame.draw.aaline(screen, green, [proj_x1, proj_y1], [proj_x2, proj_y2])

def draw_neworigin_polygon(polygon, color = green):
    newpolygon = []
    for point in polygon:
        newpolygon.append([point[0] + width / 2, point[1] + height / 2])
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
    # 충돌 감지
    collision = check_collision(polygon1, polygon2)

    # 화면 그리기
    screen.fill(white)
    # pygame.draw.polygon(screen, green, polygon1)
    # pygame.draw.polygon(screen, green, polygon2)
    draw_neworigin_polygon(polygon1)
    draw_neworigin_polygon(polygon2)
    draw_axis(polygon1)
    # 충돌 시 색상 변경
    if collision:
        draw_neworigin_polygon(polygon1, red)
        draw_neworigin_polygon(polygon2, red)

    pygame.display.flip()

# 코드 실행
pygame.quit()

# TO-DO : 폴리곤 두 개 만들고 하나에 대해서 키보드의 입력에 따라 이동함.
# 그리고 두 물체가 충돌했을때 충돌했다고 알람이 뜨도록 함.

# SAT를 완전히 이해하기 위해서

# 각 노말축을 보이게하고 충돌한 길이에 대해선 색이 다르게 해서 충돌 했을 때 모든 축에 충돌한
# 부분이 있는지 보여주는 기능이 있으면 좋겠음.


# 11-27 도형들의 원점기준을 바꿔서 하는게 아닌 새로 생성한 축에 대한 투영을 해보기