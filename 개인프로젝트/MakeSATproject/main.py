import pygame
from pygame.locals import *
from pygame import Vector2

HUGE = 100000

class polygon():
    def __init__(self,points):
        self.points = points
        self.rotation_angle = 0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.angular_velocity = 0
        
def SATtest(axis : Vector2, pointset : Vector2, minAlong : float, maxAlong : float):
    minAlong = HUGE, maxAlong = -HUGE
    for i in range(0, len(pointset)):
        # 이 축에 따른 최소/최대를 얻기 위해 내적을 함.
        dotval = pointset[i].dot(axis)
        if(dotval < minAlong): minAlong = dotval
        if(dotval > maxAlong): maxAlong = dotval
    return axis, pointset, minAlong, maxAlong

# 두 도형은 CONVEX HULLS 이어야함.
def intersects(shape1 : polygon, shape2 : polygon):
    for i in range(0, len(shape1.normals)):
        shape1.normals[i], shape1.points, shape1Min, shape1Max = SATtest(shape1.normals[i], shape1.points, shape1Min, shape1Max)
        shape1.normals[i], shape2.points, shape2Min, shape2Max = SATtest(shape1.normals[i], shape2.points, shape2Min, shape2Max)
        if (not overlaps(shape1Min, shape1Max, shape2Min, shape2Max)):
            return 0 # 교차점 없음
        # 그렇지 않으면 다음 테스트로 넘어감
    for i in range(0, len(shape2.normals)):
        shape2.normals[i], shape1.points, shape1Min, shape1Max = SATtest(shape2.normals[i], shape1.points, shape1Min, shape1Max)
        shape2.normals[i], shape2.points, shape2Min, shape2Max = SATtest(shape2.normals[i], shape2.points, shape2Min, shape2Max)
        if (not overlaps(shape1Min, shape1Max, shape2Min, shape2Max)):
            return 0 # 교차점 없음
        # 모든 축에 대해서 오버랩이 발생했다면, 두 물체는 충돌한 것이다.
    return 1
        
def overlaps(min1 : float, max1 : float, min2 : float, max2 : float):
    return isBetweenOrdered(min2,min1,max1) or isBetweenOrdered(min1, min2, max2)

def isBetweenOrdered(val : float, lowerBound : float, upperBound : float):
    return lowerBound <= val and val <= upperBound

pygame.init()

screen = pygame.display.set_mode((500,500))

# TO-DO : 폴리곤 두 개 만들고 하나에 대해서 키보드의 입력에 따라 이동함.
# 그리고 두 물체가 충돌했을때 충돌했다고 알람이 뜨도록 함.

# SAT를 완전히 이해하기 위해서

# 각 노말축을 보이게하고 충돌한 길이에 대해선 색이 다르게 해서 충돌 했을 때 모든 축에 충돌한
# 부분이 있는지 보여주는 기능이 있으면 좋겠음.