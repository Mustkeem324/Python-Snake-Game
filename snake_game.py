import pygame
import random

#BEGIN PYGAME
pygame.init() 

#DEFINE ALL COLOR
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIME = (0, 255, 0)
TEAL = (0, 128, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
NAVY = (0, 0, 128)
AQUA = (0, 128, 128)

#DIMENSION OF SCREEN
DIS_WIDTH = 1200
DIS_HEIGHT = 800

#SNAKE BLOCK SIZE  % SPEED
SNAKE_BLOCK = 25
SNAKE_SPEED = 10

#FONTS TYPE
FONT_STYLE = pygame.font.Font(None, 50)
SCORE_FONT = pygame.font.Font(None, 40)

#BEGIN DISPLAY
DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game by NX PRO')

background_image = pygame.image.load("background_image.jpg")
background_image = pygame.transform.scale(background_image, (DIS_WIDTH , DIS_HEIGHT))

#CLOCK FOR CONTROLLING GAME SPEED
CLOCK = pygame.time.Clock()

#DISPLAY SCORE
def show_score(score):
    score_text = SCORE_FONT.render("Score: " + str(score), True, WHITE)
    bg_surface = pygame.Surface((score_text.get_width() + 20, score_text.get_height() + 20))
    bg_surface.fill(RED)
    bg_surface.blit(score_text, (10, 10))
    DIS.blit(bg_surface, [10, 10])

#SHOW USERNAME
def show_username(username_name):
    username_text = SCORE_FONT.render("Username: " + str(username_name), True, WHITE)
    bg_surface = pygame.Surface((username_text.get_width() + 20, username_text.get_height() + 20))
    bg_surface.fill(RED)
    bg_surface.blit(username_text, (10, 10))
    DIS.blit(bg_surface, [10 + username_text.get_width() + 20, 10])

#DISPLAY MESSAGE
def display_message(message, color):
    message_text = FONT_STYLE.render(message, True, color)
    DIS.blit(message_text, [DIS_WIDTH/6, DIS_HEIGHT/3])

#ENTER USERNAME
def enter_username():
    username = ""
    font = pygame.font.Font(None, 30)
    input_box = pygame.Rect(10, 10, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return username
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

        DIS.blit(background_image, (0, 0))
        pygame.draw.rect(DIS, color, input_box, 2)
        username_surface = font.render("Username: " + username, True, BLACK)
        DIS.blit(username_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

#MAIN FUNCTION
def main():
    username = enter_username()
    print("Username entered:", username)

#MAIN GAME LOOP
def snake_game_loop():
    game_over = False
    game_close = False

    #GET USERNAME
    username = enter_username()

    #BEGIN POSTION OF SNAKE
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    #BEGIN MOVEMENT
    x1_change = 0
    y1_change = 0

    #BEGIN SNAKE LENGTH
    snake_list = []
    snake_length = 1

    #BEDGIN FOOD  POSTION
    food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
    food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK

    while not game_over:
        while game_close == True:
            DIS.fill(BLACK)
            display_message("You Lost! Press C-Play Again or Q-Quit", RED)
            show_score(snake_length - 1)
            show_username(username)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        snake_game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        #CHECK ID SNAKE FALL IN WALL
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True

        #MOVE TO SNAKE
        x1 += x1_change
        y1 += y1_change

        DIS.fill(AQUA)
        pygame.draw.circle(DIS, GREEN, (food_x + SNAKE_BLOCK // 2, food_y + SNAKE_BLOCK // 2), SNAKE_BLOCK // 2)
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        #IF SNAKE EAT FOOD
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
            food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
            snake_length += 1

        if len(snake_list) > snake_length:
            del snake_list[0]

        #IF SNAKE COLIDE WITH ITSELF
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        #DRAW SNAKE
        for segment in snake_list:
            pygame.draw.circle(DIS, WHITE, (segment[0] + SNAKE_BLOCK // 2, segment[1] + SNAKE_BLOCK // 2), SNAKE_BLOCK // 2)

        show_score(snake_length - 1)
        show_username(username)
        pygame.display.update()

        CLOCK.tick(SNAKE_SPEED)

    pygame.quit()

snake_game_loop()
