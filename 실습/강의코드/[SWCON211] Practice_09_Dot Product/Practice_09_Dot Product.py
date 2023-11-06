import pygame
import sys
import math
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sight Checking")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)

targetColor = WHITE
playerPosition = [300,300]
targetPosition = [130, 100]

theta = 0
playerViewVector = [0, -100]
norm_playerViewVector = [1,1]
dir1 = [-100, -100*math.sqrt(3)]
dir2 = [100, -100*math.sqrt(3)]
playerToTarget = [1,1] #v
norm_playerToTarget = [1,1]


def calculate_playerToTarget(playerToTarget,norm_playerToTarget):
    ptt = [targetPosition[0]-playerPosition[0],targetPosition[1]-playerPosition[1]]
    norm_ptt = np.array(playerToTarget/np.linalg.norm(playerToTarget)).tolist()
    
    return ptt, norm_ptt

# ========== new =============
def angle_between_vectors(norm_v, norm_f):

    dot_product = norm_v[0] * norm_f[0] + norm_v[1] * norm_f[1] # 두 벡터의 내적
    # dot_product = np.dot(norm_v, norm_f)
    angle = np.arccos(dot_product) # 코사인 역함수로 각도 계산
    angle = angle * 180 / math.pi   # 라디안으로 각도 계산   
    return angle
# ========== new =============

def draw_circles():
    pygame.draw.circle(screen, RED, playerPosition, 15)  # player
    pygame.draw.circle(screen, targetColor, targetPosition, 5)  # target

def draw_text():
    font = pygame.font.Font(None, 36)
    text_player = font.render(f"Player Pos: {playerPosition}", True, WHITE)
    text_target = font.render(f"Target Pos: {targetPosition}", True, WHITE)
    screen.blit(text_player, (screen.get_width() - text_player.get_width() - 10,10))
    screen.blit(text_target, (screen.get_width() - text_target.get_width() - 10,50))

    text_v = font.render(f"v: {norm_playerToTarget[0]:.3f},{norm_playerToTarget[1]:.3f}", True, BLUE)
    screen.blit(text_v, (screen.get_width() - text_v.get_width() - 10,90))
    # ========== new =============
    text_alpha = font.render(f"alpha: {alpha:.3f}", True, BLUE)
    screen.blit(text_alpha, (screen.get_width() - text_alpha.get_width() - 10,130))
    # ========== new =============
    
def rotation(x,y,theta):
    x_ = x*math.cos(theta) - y*math.sin(theta)
    y_ = x*math.sin(theta) + y*math.cos(theta)
    return x_,y_

def draw_line():
    pygame.draw.line(screen, WHITE, playerPosition, (np.array(playerPosition)+np.array(playerViewVector)).tolist(),3 )

    pygame.draw.line(screen, WHITE, playerPosition, (np.array(playerPosition) + np.array(dir1)).tolist(),2)
    pygame.draw.line(screen, WHITE, playerPosition, (np.array(playerPosition) + np.array(dir2)).tolist(),2)

# ========== new =============
alpha = 0
# ========== new =============
done = False
left_p = False
right_p = False
up_p = False
down_p = False
space_p = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True       
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                space_p = True
            if event.key == pygame.K_LEFT:
                left_p = True
            if event.key == pygame.K_RIGHT:
                right_p = True
            if event.key == pygame.K_UP:
                up_p = True
            if event.key == pygame.K_DOWN:
                down_p = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_p = False
            if event.key == pygame.K_LEFT:
                left_p = False
            if event.key == pygame.K_RIGHT:
                right_p = False
            if event.key == pygame.K_UP:
                up_p = False
            if event.key == pygame.K_DOWN:
                down_p = False
    
    if space_p:
        theta =0.05
#################
        # Write codes for rotating player
        # Rotate PlayerViewVector using rotation(posX,posY,angle)	
        # Rotate dir1 & dir2 (visualizing the sight of a player)  
        playerViewVector = rotation(playerViewVector[0], playerViewVector[1], theta)
        dir1 = rotation(dir1[0],dir1[1], theta)
        dir2 = rotation(dir2[0], dir2[1], theta)
#################
    if left_p:
        playerPosition[0] -= 1
    if right_p:
        playerPosition[0] += 1
    if up_p:
        playerPosition[1] -= 1
    if down_p:
        playerPosition[1] += 1
        
    # update
    playerToTarget,norm_playerToTarget = calculate_playerToTarget(playerToTarget,norm_playerToTarget)
    
    # ========== new =============

    norm_playerViewVector = np.array(playerViewVector/np.linalg.norm(playerViewVector))
    alpha = angle_between_vectors(norm_playerToTarget, norm_playerViewVector)
    #시야각 내 인지 판별하는 부분
    beta = 30
    if(alpha<beta):
        targetColor = BLUE
    else:
        targetColor = WHITE
    # ========== new =============
    
    screen.fill(BLACK)
    draw_circles()
    draw_text()
    draw_line()
    pygame.display.update()
    clock.tick(30)


pygame.quit()