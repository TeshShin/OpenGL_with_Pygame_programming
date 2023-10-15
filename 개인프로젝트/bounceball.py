import pygame
import sys

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

# 플레이어(공)의 초기 위치와 초기 속도 및 튀어오르는 속도 세팅
class player:
    def __init__(self, x, y):
        self.pos = [x,y]
        self.radius = 10
        self.velocity = [0, 0]
        self.bouncing_velocity = -13
        self.rect = pygame.Rect(self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius * 2, self.radius * 2)
    def updatecollider(self):
        self.rect = pygame.Rect(self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius * 2, self.radius * 2)
        
class platform:
    def __init__(self, x, y, width, height):
        self.pos = [x, y]
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
    def updatecollider(self):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
    # def checkcollide(self, ball):
    #     if ball.pos[0] + ball.radius >= self.rect.left and  ball.pos[0] - ball.radius <= self.rect.left: #플랫폼 왼쪽에 부딪힐 때
    #         ball.pos[0] = self.rect.left - ball.radius
    #     elif ball.pos[1] - ball.radius >= self.rect.top and ball.pos[1] + ball.radius <= self.rect.top: # 플랫폼 위쪽에 부딪힐 때
    #         ball.velocity[1] = ball.bouncing_velocity
    #     elif ball.pos[1] + ball.radius and ball.pos[1] - ball.radius >= self.rect.bottom: # 플랫폼 아래쪽에 부딪힐 때
    #         ball.pos[1] = self.rect.bottom + ball.radius
    #         ball.velocity[1] = -ball.velocity[1]
    #     elif ball.pos[0] - ball.radius <= self.rect.right and ball.pos[0] + ball.radius >= self.rect.right: # 플랫폼 오른쪽에 부딪힐 때
    #         ball.pos[0] = self.rect.right + ball.radius
    def checkcollide(self, ball):
        if self.rect.colliderect(ball.rect):
            if ball.rect.right >= self.rect.left and ball.rect.left <= self.rect.left: #플랫폼 왼쪽에 부딪힐 때
                ball.pos[0] = self.rect.left - ball.radius
            elif ball.rect.left <= self.rect.right and ball.rect.right >= self.rect.right: # 플랫폼 오른쪽에 부딪힐 때
                ball.pos[0] = self.rect.right + ball.radius    
            elif ball.rect.bottom >= self.rect.top and ball.rect.top <= self.rect.top: # 플랫폼 위쪽에 부딪힐 때
                ball.velocity[1] = ball.bouncing_velocity
            elif ball.rect.top <= self.rect.bottom and ball.rect.bottom >= self.rect.bottom: # 플랫폼 아래쪽에 부딪힐 때
                ball.pos[1] = self.rect.bottom + ball.radius
                ball.velocity[1] = -ball.velocity[1]
            
        
        
        
# 플레이어 생성  
ball = player(400,300)
# 플랫폼 생성
ground1 = platform(600,500,20,50)
ground2 = platform(550,500,50,20)
# 중력 가속도 
gravity = 0.9

# 시간 설정
clock = pygame.time.Clock()
FPS = 60  # 시간당 프레임

# 게임 루프
while True:
    clock.tick(FPS)  # 프레임 제한
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball.velocity[0] = -5
            elif event.key == pygame.K_RIGHT:
                ball.velocity[0] = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                ball.velocity[0] = 0
            elif event.key == pygame.K_RIGHT:
                ball.velocity[0] = 0

    # 공에 중력 가하기
    ball.velocity[1] += gravity
    # 플랫폼과 플레이어(공)와의 콜리전 판정
    ground1.checkcollide(ball)
    ground2.checkcollide(ball)
        
            
     # 공 움직이기
    ball.pos[0] += ball.velocity[0]
    ball.pos[1] += ball.velocity[1]
  # 물체의 움직임에 따른 콜라이더 업데이트
    ball.updatecollider()
    
    
    
    
    # 화면 가장자리와 공의 콜리젼
    if ball.pos[0] - ball.radius <= 0 or ball.pos[0] + ball.radius >= 800:
        ball.velocity[0] = -ball.velocity[0]
    if ball.pos[1] + ball.radius >= 600:
        ball.pos[1] = 600 - ball.radius
        ball.velocity[1] = ball.bouncing_velocity

    # 화면 클리어
    screen.fill(WHITE)

    # 플랫폼 그리기
    pygame.draw.rect(screen, GREEN, (int(ground1.pos[0]), int(ground1.pos[1]), ground1.width, ground1.height))
    pygame.draw.rect(screen, GREEN, (int(ground2.pos[0]), int(ground2.pos[1]), ground2.width, ground2.height))
    # 공그리기
    pygame.draw.circle(screen, RED, (int(ball.pos[0]), int(ball.pos[1])), ball.radius)
    # 화면 업데이트하기
    pygame.display.flip()
