import pygame
import random


pygame.init()
screen = pygame.display.set_mode((800, 600))

# constants

PLAYER_CHANGE = 2
PLAYER_CHANGE_JUMP = -5
LEFT_BOUNDARY = 100
RIGHT_BOUNDARY = 565
BOTTOM_BOUNDARY = 530
BLACK = (0, 0 ,0)
WHITE = (255, 255, 255)


def setup():

    global player_x, player_y, player_size, playerX_change, playerY_change, restart_cooldown
    global letter_x, letter_y, letter_size, message, current_letter_index
    global final_screen_initialize, game_state
    global background_image, background_image_final_scene, player_image
    global font

    # backgrounds 

    background_image = pygame.image.load('wallFINAL.png')
    background_image_final_scene = pygame.image.load('wallDYNO.png')

    # player
    player_image = pygame.image.load('guy128transparent.png')
    player_x = 370
    player_y = 480
    player_size = 128
    playerX_change = 0
    playerY_change = 0


    # letter 
    letter_x = random.randint(150, 650)
    letter_y = random.randint(50, 450)
    letter_size = 50


    font = pygame.font.Font('PeaberryBase.ttf', 50)
    message = "HAPPYBIRTHDAY"
    current_letter_index = 0
    final_screen_initialize = False
    game_state = "normal"
    restart_cooldown = 0

def player(x, y):
    screen.blit(player_image, (x, y))


def draw_letter(letter, x, y):
    letter_surface = font.render(letter, True, BLACK)
    screen.blit(letter_surface, (x, y))

# play button screen
def play_screen():
    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        # center the button
        button_width = 200
        button_height = 50
        button_x = (800 - button_width) // 2  # Center horizontally (screen is 800 wide)
        button_y = (600 - button_height) // 2  # Center vertically (screen is 600 tall)
        
        play_button = pygame.Rect(button_x, button_y, button_width, button_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse_pos):
                    return  # exit the function and start game

        # draw button
        button_font = pygame.font.Font('PeaberryBase.ttf', 100)
        button_text = button_font.render("PLAY", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=play_button.center)
        screen.blit(button_text, button_text_rect)

        # draw directions
        directions_font = pygame.font.Font('PeaberryBase.ttf', 24)
        directions_text = directions_font.render("Collect All Letters. Use ARROW Keys to Move.", True, (255, 255, 255))
        directions_text_rect = directions_text.get_rect(center=(400, button_y + button_height + 50))
        screen.blit(directions_text, directions_text_rect)


        pygame.display.update()



play_screen()
running = True
is_setup = False

while running: 

    if not is_setup:
        setup()
        is_setup = True

    screen.blit(background_image, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "normal":
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT:
                    playerX_change = -PLAYER_CHANGE
                if event.key == pygame.K_RIGHT:
                    playerX_change = PLAYER_CHANGE
                if event.key == pygame.K_UP:
                    playerY_change = -PLAYER_CHANGE
                if event.key == pygame.K_DOWN:
                    playerY_change = PLAYER_CHANGE
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0
        # space bar use only for final scene
        if game_state == "restricted":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playerY_change = PLAYER_CHANGE_JUMP



    # screen boundaries
    if player_x <= LEFT_BOUNDARY:
        player_x = LEFT_BOUNDARY
    elif player_x >= RIGHT_BOUNDARY:
        player_x = RIGHT_BOUNDARY
    elif player_y >= BOTTOM_BOUNDARY:
        player_y = BOTTOM_BOUNDARY
    elif player_y <= 0:
        player_y = 0

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    letter_rect = pygame.Rect(letter_x, letter_y, letter_size, letter_size)

    if current_letter_index < len(message):

        if current_letter_index == len(message)-1:

            screen.blit(background_image_final_scene, (0,0))
            screen.blit(font.render("dyno !", True, BLACK), (500, 300))

            if not final_screen_initialize:
                letter_x = 400
                letter_y = 0

                player_x = 370
                player_y = 350
                playerX_change = 0
                playerY_change = 0
                player_rect.x = player_x
                player_rect.y = player_y
                game_state = "restricted"
                final_screen_initialize = True

            letter_rect.x = letter_x
            letter_rect.y = letter_y

        current_letter = message[current_letter_index]
        draw_letter(current_letter, letter_x, letter_y)
    else: 
        playerX_change = 0
        playerY_change = 0
        complete_text = font.render("HAPPY BIRTHDAY ERLE!", True, BLACK)
        complete_text_rect = complete_text.get_rect(center=(400, 300))

        screen.blit(complete_text, complete_text_rect)
        
        # play again button
        button_width = 300
        button_height = 60
        button_x = (800 - button_width) // 2
        button_y = 400
        play_again_button = pygame.Rect(button_x, button_y, button_width, button_height)
        
        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:  
            if play_again_button.collidepoint(mouse_pos):
                is_setup = False
                restart_cooldown = 30  # Wait 30 frames before checking collisions
                
        # draw button
        
        play_again_font = pygame.font.Font('PeaberryBase.ttf', 40)
        play_again_text = play_again_font.render("Play Again", True, BLACK)
        play_again_rect = play_again_text.get_rect(center=play_again_button.center)
        screen.blit(play_again_text, play_again_rect)

        # check for button click
        if pygame.mouse.get_pressed()[0]:  
            if play_again_button.collidepoint(mouse_pos):
                is_setup = False


    if restart_cooldown > 0:
        restart_cooldown -= 1

    if player_rect.colliderect(letter_rect) and restart_cooldown == 0:
        letter_x = random.randint(150, 650)
        letter_y = random.randint(50, 450)
        letter_rect.x = letter_x
        letter_rect.y = letter_y
        current_letter_index+=1

    player_x += playerX_change
    player_y += playerY_change
    player(player_x, player_y)
    pygame.display.update()

