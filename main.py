import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(("Snake"))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

BOARD = pygame.image.load(os.path.join('Assets', 'snake_board.png'))
GAME_OVER_TEXT = pygame.image.load(os.path.join('Assets', 'game_over.png'))
TEXT_FONT = pygame.font.SysFont('Early GameBoy', 30)

BP_WIDTH, BP_HEIGHT = 10, 10
BODY_PART = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'body.png')), (15, 15))

FOOD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'body.png')), (10, 10))
F_WIDTH, F_HEIGHT = 10, 10
food_pos = [(random.randrange(10, 380)//10)*10, (random.randrange(10, 380)//10)*10]
venom = False

FOOD_HIT = pygame.USEREVENT + 1
BODY_HIT = pygame.USEREVENT + 2
WALL_HIT = pygame.USEREVENT + 3

score_list = [0]

def draw_window(snake, food, food_list, venom, score, record):
    WIN.blit(BOARD, (0, 0))
    for body in snake:
        pygame.draw.rect(WIN, WHITE, body)

    if len(food_list) == 1:
        if venom == True:
            pygame.draw.rect(WIN, GREEN, food)
        else:
            pygame.draw.rect(WIN, RED, food)

    score_text = TEXT_FONT.render("Score: " + str(score), 1, WHITE)
    WIN.blit(score_text, (20, 490 - score_text.get_height() - 10))
    record_text = TEXT_FONT.render("Record: " + str(record), 1, WHITE)
    WIN.blit(record_text, (20, 500))

    pygame.display.update()

def handle_movement(change_to, direction, snake):
    if change_to == "L" and direction != "R":
        direction = "L"
    if change_to == "R" and direction != "L":
        direction = "R"
    if change_to == "U" and direction != "D":
        direction = "U"
    if change_to == "D" and direction != "U":
        direction = "D"

    if direction == "L":
        snake[len(snake) - 1].x = snake[0].x - BP_WIDTH
        snake[len(snake) - 1].y = snake[0].y
    if direction == "R":
        snake[len(snake) - 1].x = snake[0].x + BP_WIDTH
        snake[len(snake) - 1].y = snake[0].y
    if direction == "U":
        snake[len(snake) - 1].x = snake[0].x
        snake[len(snake) - 1].y = snake[0].y - BP_HEIGHT
    if direction == "D":
        snake[len(snake) - 1].x = snake[0].x
        snake[len(snake) - 1].y = snake[0].y + BP_HEIGHT
    snake.insert(0, snake.pop())

    return direction

def handle_growth(snake, food_list):
    for food in food_list:
        if snake[0].colliderect(food):
            pygame.event.post(pygame.event.Event(FOOD_HIT))
            new_body = pygame.Rect(-10, -10, BP_WIDTH, BP_HEIGHT)
            snake.append(new_body)

def handle_collision(snake, direction):
    for i in range(1, len(snake)):
        if snake[0].colliderect(snake[i]):
            pygame.event.post(pygame.event.Event(BODY_HIT))
    if direction == "L" and snake[0].x < 10:
        pygame.event.post(pygame.event.Event(WALL_HIT))
    if direction == "R" and snake[0].x > 380:
        pygame.event.post(pygame.event.Event(WALL_HIT))
    if direction == "U" and snake[0].y < 10:
        pygame.event.post(pygame.event.Event(WALL_HIT))
    if direction == "D" and snake[0].y > 380:
        pygame.event.post(pygame.event.Event(WALL_HIT))

def handle_difficulty(score):
    if score < 10:
        fps = 10
    elif score >= 10 and score < 20:
        fps = 12
    elif score >= 20 and score < 30:
        fps = 15
    elif score >= 30 and score < 40:
        fps = 17
    else:
        fps = 20
    return fps

def get_record(score_list):
    record = max(score_list)
    return record

def game_over_display():
    WIN.blit(GAME_OVER_TEXT, (10, 10))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    global random_num
    direction = ""
    change_to = ""

    score = 0

    body = pygame.Rect(190, 190, BP_WIDTH, BP_HEIGHT)
    snake = [body]

    food = pygame.Rect(food_pos[0], food_pos[1], F_WIDTH, F_HEIGHT)
    food_list = [food]

    cycle_counter = 0

    if len(food_list) == 0:
        food_list.append(food)

    clock = pygame.time.Clock()
    run = True
    game_over = False
    while run:
        FPS = handle_difficulty(score)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_to = "L"
                if event.key == pygame.K_RIGHT:
                    change_to = "R"
                if event.key == pygame.K_UP:
                    change_to = "U"
                if event.key == pygame.K_DOWN:
                    change_to = "D"
            if event.type == FOOD_HIT:
                if venom == True:
                    game_over = True
                else:
                    score += 1
                    food_list.remove(food)
                    food = pygame.Rect((random.randrange(10, 380)//10)*10, (random.randrange(10, 380)//10)*10, F_WIDTH, F_HEIGHT)
                    food_list.append(food)
            if event.type == BODY_HIT or event.type == WALL_HIT:
                game_over = True

        if cycle_counter % 40 == 0:
            random_num = random.randrange(0, 4)
            if random_num == 1:
                venom = True
            else:
                venom = False

        direction = handle_movement(change_to, direction, snake)
        handle_growth(snake, food_list)
        handle_collision(snake, direction)
        record = get_record(score_list)
        cycle_counter += 1

        if game_over == True:
            score_list.append(score)
            game_over_display()
            break

        draw_window(snake, food, food_list, venom, score, record)

    main()

if __name__ == "__main__":
    main()
