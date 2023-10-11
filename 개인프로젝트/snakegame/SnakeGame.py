import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 640, 480
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255) # 파란색 추가

# Snake and food properties
snake_pos = [320, 240]
snake_body = [[320, 240], [310, 240], [300, 240]]
food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
food_spawn = True
# 뱀의 길이를 짧게 해주고 속도를 느리게 해주는 다이어트 식품 (파란색으로 할 것임.)
diet_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
while food_pos == diet_pos:
     diet_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
diet_spawn = True
# Direction
direction = 'RIGHT'
change_to = direction

# Initial frame rate
framerate = 15

# Score
score = 0
addscore = 3 # 점수 추가량
# Display Score function
def Your_score(score):
    value = pygame.font.SysFont('comicsans', 30).render("Your Score: " + str(score), True, WHITE)
    window.blit(value, [0, 0])

# Main Function
def gameLoop():
    global direction, change_to
    global snake_pos, snake_body
    global food_pos, food_spawn
    global score, framerate, addscore # 점수 추가량
    global diet_pos, diet_spawn

    # Game Over
    game_over = False
    game_close = False

    while not game_over:
        while game_close == True:
            window.fill(BLACK)
            Your_score(score)
            pygame.display.update()

            # Asking user to play again or quit
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r: # r키를 누르면 재시작
                        snake_pos = [320, 240] # 재시작 시 뱀의 초기 위치
                        snake_body = [[320, 240], [310, 240], [300, 240]] # 재시작 시 뱀의 초기 길이
                        direction = 'RIGHT'
                        change_to = direction # 재시작 시 뱀의 초기 방향
                        score = 0 # 재시작 시 점수 초기화
                        addscore = 3 # 재시작 시 점수 추가량 초기화
                        framerate = 15 # 재시작 시 뱀 이동속도 초기화
                        food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10] # 재시작 시 음식 초기 위치 초기화
                        # 재시작 시 다이어트 음식 초기 위치 초기화
                        diet_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
                        while food_pos == diet_pos:
                            diet_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Validation of direction: avoid the overlap of snake's body
        if change_to == 'UP' and not direction == 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism: insert a new position (snake_pose) on 
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += addscore # 점수 추가 방식 변경
            framerate += 2
            addscore += 1 # 뱀의 길이가 늘수록 점수 추가량 증가
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
        food_spawn = True
        
        # 다이어트 음식을 먹으면 이동속도와 길이 줄이기.
        if snake_pos[0] == diet_pos[0] and snake_pos[1] == diet_pos[1]:
            diet_spawn = False
            if len(snake_body) > 1: # 몸통이 하나면 이속과 길이가 줄어들면 안됨.
                framerate -= 2
                addscore -= 1 # 뱀의 길이가 짧아질수록 점수 추가량 감소
                snake_body.pop()
                
                
        # 다이어트 음식 먹으면 다시 스폰하기.
        if not diet_spawn:
            diet_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
            while food_pos == diet_pos:
                diet_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
        diet_spawn = True
        
        window.fill(BLACK)
        for pos in snake_body:
            pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(window, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        
        pygame.draw.rect(window, BLUE, pygame.Rect(diet_pos[0], diet_pos[1], 10, 10)) # 다이어트 음식 보이기
        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH-10:
            game_close = True
        if snake_pos[1] < 0 or snake_pos[1] > HEIGHT-10:
            game_close = True

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_close = True

        pygame.display.update()
        # Limit frame rate to 15 Hz
        pygame.time.Clock().tick(framerate)

    pygame.quit()
    quit()

# Run the game
gameLoop()