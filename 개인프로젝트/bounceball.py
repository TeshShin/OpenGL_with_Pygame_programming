import pygame
import sys
import math
from pygame.locals import *
# 게임 초기화
pygame.init()
# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('바운스볼 게임')

# 색 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (100,100,0)
# 중력 가속도 
gravity = 0.6
# 시간 설정
clock = pygame.time.Clock()
FPS = 60  # 시간당 프레임

# 플레이어(공)의 초기 위치와 초기 속도 및 튀어오르는 속도 세팅
class player:
    def __init__(self, x, y):
        self.died = False
        self.pos = [x,y]
        self.radius = 10
        self.velocity = [0, 0]
        self.bouncing_velocity = -8
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = (x,y)
    def updatecollider(self):
        self.rect.center = (self.pos[0], self.pos[1])
    

class platform:
    def __init__(self, x, y, width, height):
        self.pos = [x,y]
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)   # 중심점 기준 좌표로 위치 세팅
        self.width = width
        self.height = height
        
        
    def checkcollide(self, ball):
        if self.rect.collidepoint(ball.rect.midright): # 플랫폼 왼쪽에 부딪힐때
            ball.velocity[0] = -0.5
        elif self.rect.collidepoint(ball.rect.midleft): # 플랫폼 오른쪽에 부딪힐때
            ball.velocity[0] = 0.5
        elif self.rect.collidepoint(ball.rect.midtop) or self.rect.collidepoint(ball.rect.topleft) or self.rect.collidepoint(ball.rect.topright): # 플랫폼 아래쪽에 부딪힐때
            ball.pos[1] = self.rect.bottom + ball.radius
            if (ball.velocity[1] < 0):
                ball.velocity[1] = -ball.velocity[1]
        elif self.rect.collidepoint(ball.rect.midbottom) or self.rect.collidepoint(ball.rect.bottomleft) or self.rect.collidepoint(ball.rect.bottomright): # 플랫폼 위쪽에 부딪힐때
            ball.velocity[1] = ball.bouncing_velocity
           
class star:
    def __init__(self, x, y):
        self.pos = [x,y]
        self.img = pygame.image.load('star.png')
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.touch = False
        
    def checkcollide(self, ball):
        if self.rect.colliderect(ball.rect):
            self.touch = True
            self.rect = Rect(0,0,0,0) # 충돌체 초기화
            return True
        else:
            return False
class spike:
    def __init__(self, x, y):
        self.pos = [x,y]
        self.img = pygame.image.load('spike.png')
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
    def checkcollide(self, ball):
        if self.rect.colliderect(ball.rect):
            return True
        else:
            return False

# 플레이어 생성
ballinitx, ballinity = 110, 450
ball = player(ballinitx, ballinity)
# 플랫폼 생성
# 정사각형의 플랫폼(20,20) 사이 자연스러운 최대 길이차 = 100, 
# 50 높은 곳은 (이전 플랫폼의 x좌표 + 이전 플랫폼의 너비 - 20 + 80)
ground_list = [
    platform(70,460,20,100), # 왼쪽 벽
    platform(100,500,80,20), # 첫 바닥
    platform(200,500,60,20),
    platform(300,500,60,20),
    platform(420,500,60,20),
    platform(550,500,60,20),
    platform(710,500,60,20),
    platform(740,460,20,100),
    
    platform(100,80,20,100),
    platform(130,80,40,20),
    platform(160,80,20,100),    # H
    
    platform(220,80,20,100),
    platform(260,80,60,20),
    platform(260,40,60,20),
    platform(260,120,60,20),    # E
    
    platform(340,80,20,100),
    platform(380,120,60,20),    # L
    
    platform(460,80,20,100),
    platform(500,120,60,20),    # L
    
    platform(580,80,20,100),
    platform(620,120,80,20),
    platform(650,80,20,100),
    platform(620,40,80,20),     # O
    
    platform(700, 60,20,60),
    platform(700, 120, 20, 20)  # !
    
    
]
star_list = [
    star(300,420),
    star(420,420),
    star(550,420),
    star(720,420)
]
spike_list = []
goals = 0
# 다른 스테이지부터 로드하고 싶다면
stage = 2 # 스테이지 숫자를 바꾸고 (초기 1)
loadstage = True # 로드 스테이지를 True로 하면 된다. (초기 False)
# 게임 루프
while True:
    clock.tick(FPS)  # 프레임 제한
    # 공이 죽으면
    if (ball.died):
        if(abs(pygame.time.get_ticks() - diedtime) > 800): # 0.8초가 지나면 리스폰(get_ticks는 밀리초를 반환 1초는 1000밀리초)
            ball.pos = [ballinitx, ballinity]
            ball.updatecollider()
            ball.died = False
            goals = 0
            print('초기화')        
            for star in star_list:
                if star.touch: # 죽기 전에 먹은 별들 다시 초기화
                    star.touch = False
                    star.rect = Rect(0,0,20,20)
                    star.rect.center = star.pos[0], star.pos[1]
            
            
    # 스테이지 1 종료
    if (goals == len(star_list) and stage == 1 and not loadstage):
        endtime = pygame.time.get_ticks()
        loadstage = True
        print('종료중')
    # 스테이지 2로 초기화
    if (stage == 1 and loadstage):
        if(abs(pygame.time.get_ticks() - endtime) > 800):
            stage += 1
    if (stage == 2 and loadstage): # 스테이지 2 맵세팅
        ground_list.clear()
        star_list.clear()
        goals = 0
        ballinitx, ballinity = 50, 20
        ball.pos = [ballinitx, ballinity]
        ball.velocity = [0, 0]
        ground_list = [
            platform(10,300,20,600),
            
            platform(50,110,60,40),
            platform(140,110,40,40),
            platform(260,110,80,40),
            platform(420,120,80,60),
            
            platform(530,90,20,200),
            platform(300,200,480,20), #_l
            
            platform(220,140,440,20),
            
            platform(50,300,60,20),
            platform(190,300,60,20),
            platform(330,300,60,20),
            
            platform(470,400,60,20),
                       
        
            platform(200,590,400,20)
        ]
        
        spike_list = [
            spike(90,120),
            spike(110,120),
            
            spike(170,120),
            spike(190,120),
            spike(210,120),
            
            spike(310,120),
            spike(330,120),
            spike(350,120),
            spike(370,120),
            
            
           
            
        ]
        
        
        loadstage = False
            
    
    
            
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball.velocity[0] = -4
    if keys[pygame.K_RIGHT]:
        ball.velocity[0] = 4
    elif not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        ball.velocity[0] = 0
        # if event.type == pygame.KEYDOWN: # 플레이어 키 입력
        #     if event.key == pygame.K_LEFT:
        #         ball.velocity[0] = -5
        #     elif event.key == pygame.K_RIGHT:
        #         ball.velocity[0] = 5
        # elif event.type == pygame.KEYUP and ball.velocity[0] < 0:
        #     if event.key == pygame.K_LEFT:
        #         ball.velocity[0] = 0
        # elif event.type == pygame.KEYUP and ball.velocity[0] > 0:
        #     if event.key == pygame.K_RIGHT:
        #         ball.velocity[0] = 0

    # 공에 중력 가하기(중력에 의해 가해진 속도 최대치 한정하기)
    # 속도가 너무 커지면 위치가 큰 값으로 순간이동하기 때문에 콜리전 측정 등이 이상해짐.
    # 8로 정한 이유는 플랫폼들의 두께가 보통 20이기 때문에 2프레임이 지나도 16의 위치가 변하는 것이므로
    # 충돌 판정이 스킵되지 않을 것이라고 생각했다. 
    if (ball.velocity[1] < 8):
        ball.velocity[1] += gravity
        

        
    # 플랫폼과 플레이어(공)와의 콜리전 판정
    for ground in ground_list:
        ground.checkcollide(ball)
    # 별과 플레이어와의 콜리전 판정
    for star in star_list:
        if star.checkcollide(ball):
            goals += 1
            print('닿음')
    # 가시와 플레이어와의 콜리전 판정
    for spike in spike_list:
        if spike.checkcollide(ball) and not ball.died:
            diedtime = pygame.time.get_ticks()  # 리스폰까지의 딜레이를 위한 시간 측정
            ball.died = True
            print('가시 닿음')
            
    # <주의> 공 움직이는 것은 콜리전 판정 이후에 있어야함!!
    if not ball.died:
        # 공 움직이기
        ball.pos[0] += ball.velocity[0]
        ball.pos[1] += ball.velocity[1]
        # 물체의 움직임에 따른 콜라이더 업데이트
        ball.updatecollider()
    
    
    
    
    # 화면 가장자리와 공의 콜리젼
    # 플레이어가 화면 바깥으로 나가면 죽음
    if (ball.pos[1] + ball.radius >= 600) and not ball.died:
        diedtime = pygame.time.get_ticks()  # 리스폰까지의 딜레이를 위한 시간 측정
        ball.died = True

    # 화면 클리어
    screen.fill(WHITE)
    # 플랫폼 그리기
    for ground in ground_list:
        pygame.draw.rect(screen, GREEN, ground.rect)
        
    # 별 그리기
    for star in star_list:
        if not star.touch:
            screen.blit(star.img, star.rect)
    # 가시 그리기
    for spike in spike_list:
        screen.blit(spike.img, spike.rect)
    
    # 공그리기
    if not ball.died:
        pygame.draw.circle(screen, RED, (int(ball.pos[0]), int(ball.pos[1])), ball.radius)
    
    # 화면 업데이트하기
    pygame.display.flip()
