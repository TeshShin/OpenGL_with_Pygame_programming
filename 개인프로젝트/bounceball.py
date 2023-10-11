import pygame
import sys

# 게임 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bounce Ball Game')

# 색 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 플레이어(공)의 초기 위치와 초기 속도 및 튀어오르는 속도 세팅
class player:
    def __init__(self, x, y):
        self.pos = [x,y]
        self.radius = 10
        self.velocity = [0, 0]
        self.bouncing_velocity = -13
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.radius * 2, self.radius * 2)
    def updatecollider(self):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.radius * 2, self.radius * 2)
class platform:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.pos = [x, y]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
    def updatecollider(self):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        
        
        
        
        
ball = player(400,300)
ground1 = platform(600,500,20,20)
# 중력 가속도 
gravity = 0.9

# 시간 설정
clock = pygame.time.Clock()
FPS = 60  # 시간당 프레임

# 게임 루프
while True:
    clock.tick(FPS)  # 프레임 제한
    # 물체의 움직임에 따른 콜라이더 업데이트
    ball.updatecollider()
    ground1.updatecollider()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball.velocity[0] = -5
            elif event.key == pygame.K_RIGHT:
                ball.velocity[0] = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                ball.velocity[0] = 0

    # 공에 중력 가하기
    ball.velocity[1] += gravity
    

    
    
    # 플랫폼과 플레이어(공)와의 콜리전 판정
    if ground1.rect.colliderect(ball.rect):
        if ball.rect.right >= ground1.rect.left and ball.rect.left <= ground1.rect.left:
            ball.pos[0] = ground1.rect.left - ball.radius
        elif ball.rect.left <= ground1.rect.right and ball.rect.right >= ground1.rect.right:
            ball.pos[0] = ground1.rect.right + ball.radius
        elif ball.rect.bottom >= ground1.rect.top and ball.rect.top <= ground1.rect.top:
            ball.velocity[1] = ball.bouncing_velocity
        elif ball.rect.top <= ground1.rect.bottom and ball.rect.bottom >= ground1.rect.bottom:
            ball.pos[1] = ground1.rect.bottom + ball.radius
            

    # 공 움직이기
    ball.pos[0] += ball.velocity[0]
    ball.pos[1] += ball.velocity[1]
    
    
    
    
    # 화면 가장자리와 공의 콜리젼
    if ball.pos[0] - ball.radius <= 0 or ball.pos[0] + ball.radius >= 800:
        ball.velocity[0] = -ball.velocity[0]
    if ball.pos[1] + ball.radius >= 600:
        ball.pos[1] = 600 - ball.radius
        ball.velocity[1] = ball.bouncing_velocity

    # 화면 클리어
    screen.fill(WHITE)

    # 공그리기
    
    pygame.draw.rect(screen, GREEN, (int(ground1.pos[0]), int(ground1.pos[1]), ground1.width, ground1.height))
    pygame.draw.circle(screen, RED, (int(ball.pos[0]), int(ball.pos[1])), ball.radius)
    # 화면 업데이트하기
    pygame.display.flip()
