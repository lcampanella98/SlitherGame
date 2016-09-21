import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

RIGHT = 3
UP = 0
LEFT = 1
DOWN = 2

background_color = white
window_width = 800
window_height = 600

game_display = pygame.display.set_mode((window_width, window_height))
title = 'Slither'
pygame.display.set_caption(title)
clock = pygame.time.Clock()
in_game_fps = 30
pause_fps = 5

small_font = pygame.font.SysFont("comicsansms", 25)
med_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 80)

snake_head_img = pygame.image.load('sprites/snake_head.png')
red_apple_img = pygame.image.load('sprites/red_apple.png')
icon = pygame.image.load('sprites/red_apple_icon.ico')
pygame.display.set_icon(icon)


def pause():

    paused = True
    message_to_screen(large_font, "Paused", black, y_displace=-100)
    message_to_screen(small_font, "Press C to continue or Q to quit", black, y_displace=25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                    break
                elif event.key == pygame.K_q:
                    quit_game()


def score(the_score):
    text = small_font.render("Score: "+str(the_score), True, black)
    game_display.blit(text, [0, 0])


def game_intro():
    intro = True
    while intro:
        game_display.fill(background_color)
        message_to_screen(large_font, "Welcome to Slither", green, y_displace=-100)
        message_to_screen(small_font, "The objective is to eat red apples", black, y_displace=-30)
        message_to_screen(small_font, "The more apples you eat, the longer you get", black, y_displace=0)
        message_to_screen(small_font, "If you run into yourself, or the edges, you die", black, y_displace=30)
        message_to_screen(small_font, "Press E to pause in-game", black, y_displace=60)
        message_to_screen(med_font, "Press any key to start", black, y_displace=200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                intro = False

        pygame.display.update()
        clock.tick(pause_fps)


def snake_overlapping(snake_list):
    head = snake_list[-1]
    for segment in snake_list[:-1]:
        if segment == head:
            return True
    return False


def snake(block_size, snake_list, direction):
    head = pygame.transform.rotate(snake_head_img, 90 * direction)
    for segment in snake_list[:-1]:
        pygame.draw.rect(game_display, green, [segment[0], segment[1], block_size, block_size])
    game_display.blit(head, (snake_list[-1][0], snake_list[-1][1]))


def message_to_screen(font, msg, color, y_displace=0):
    screen_text = font.render(msg, True, color)
    size = font.size(msg)
    game_display.blit(screen_text, [window_width / 2 - size[0] / 2,
                                    window_height / 2 - size[1] / 2 + y_displace])


def get_random_apple_coord(max_x, max_y, size):
    return random.randrange(0, max_x-size), random.randrange(0, max_y-size)


def is_eating_apple(apple_coord, snake_head_coord, apple_size, block_size):
    return ((apple_coord[0] <=
             snake_head_coord[0] <=
             apple_coord[0] + apple_size and
            apple_coord[1] <=
             snake_head_coord[1] <=
             apple_coord[1] + apple_size) or
            (apple_coord[0] <=
             snake_head_coord[0] + block_size <=
             apple_coord[0] + apple_size and
            apple_coord[1] <=
             snake_head_coord[1] + block_size <=
             apple_coord[1] + apple_size))


def is_snake_in_screen(snake_coord):
    return 0 <= snake_coord[0] < window_width and 0 <= snake_coord[1] < window_height


def quit_game():
    pygame.quit()
    quit()


def game_loop():
    block_size = 20
    lead_x = window_width/2
    lead_y = window_height/2
    lead_x_change = 10
    lead_y_change = 0
    x_change = block_size
    y_change = block_size
    snake_length = 2
    snake_list = []
    apple_thickness = 30
    snake_direction = RIGHT
    the_score = 0

    game_exit = False
    game_over = False

    apple_coord = get_random_apple_coord(window_width, window_height, block_size)

    while not game_exit:

        if game_over:
            message_to_screen(large_font, "Game Over", red, y_displace=-30)
            message_to_screen(med_font, "Press C to play again or Q to quit", black, y_displace=70)
            pygame.display.update()

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit_game()
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if lead_x_change == 0:
                        snake_direction = LEFT
                        lead_x_change = - x_change
                        lead_y_change = 0
                    break
                elif event.key == pygame.K_RIGHT:
                    if lead_x_change == 0:
                        snake_direction = RIGHT
                        lead_x_change = x_change
                        lead_y_change = 0
                    break
                elif event.key == pygame.K_UP:
                    if lead_y_change == 0:
                        snake_direction = UP
                        lead_y_change = - y_change
                        lead_x_change = 0
                    break
                elif event.key == pygame.K_DOWN:
                    if lead_y_change == 0:
                        snake_direction = DOWN
                        lead_y_change = y_change
                        lead_x_change = 0
                    break
                elif event.key == pygame.K_e:
                    pause()
        if not is_snake_in_screen((lead_x, lead_y)):
            game_over = True

        if is_eating_apple(apple_coord, (lead_x, lead_y), apple_thickness, block_size):
            apple_coord = get_random_apple_coord(window_width, window_height, apple_thickness)
            snake_length += 1
            the_score += 1

        game_display.fill(background_color)
        score(the_score)
        lead_x += lead_x_change
        lead_y += lead_y_change

        game_display.blit(red_apple_img, (apple_coord[0], apple_coord[1]))

        snake_list.append((lead_x, lead_y))
        if len(snake_list) > snake_length:
            del snake_list[0]

        if snake_overlapping(snake_list):
            game_over = True

        snake(block_size, snake_list, snake_direction)
        pygame.display.update()
        clock.tick(in_game_fps)

game_intro()
game_loop()
