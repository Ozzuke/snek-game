import pygame
import numpy as np
import random


def check_events(settings, status):
    """check for pygame events and respond accordingly"""

    # go through the list of events and act or queue the event
    for event in pygame.event.get():

        # quit if the quit signal is sent or "q" has been pressed
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            status.quit = True

        # if event is a key press and queue isn't full
        elif len(status.event_queue) < settings.queue_len and event.type == pygame.KEYDOWN:
            status.event_queue.append(event)

    # if event queue isn't empty, act on the first event
    if status.event_queue:
        event = status.event_queue.pop(0)

        # if event is a key press, respond
        if event.type == pygame.KEYDOWN:
            respond_keydown(event, status)


def respond_keydown(event, status):
    """respond to key presses accordingly"""

    # change direction key presses
    if event.key in [pygame.K_UP, pygame.K_w, pygame.K_k] and status.move_dir not in "NS":
        # if not already moving along the same axis, change direction to north
        status.move_dir = "N"

    if event.key in [pygame.K_DOWN, pygame.K_s, pygame.K_j] and status.move_dir not in "NS":
        # if not already moving along the same axis, change direction to south
        status.move_dir = "S"

    if event.key in [pygame.K_RIGHT, pygame.K_d, pygame.K_l] and status.move_dir not in "EW":
        # if not already moving along the same axis, change direction to east
        status.move_dir = "E"

    if event.key in [pygame.K_LEFT, pygame.K_a, pygame.K_h] and status.move_dir not in "EW":
        # if not already moving along the same axis, change direction to west
        status.move_dir = "W"


def draw_screen(screen, settings, game_map, status):
    """draw and flip the display"""

    # fill screen with background color
    screen.fill(settings.background_color)

    # draw the border and map area
    pygame.draw.rect(screen, settings.edge_color, pygame.Rect(settings.edge_coordinates))
    pygame.draw.rect(screen, settings.map_empty_color, pygame.Rect(settings.map_coordinates))

    # draw items (snake, apple, wall etc) on the map
    for pixel in np.array([x for y in game_map.game_map for x in y if x[2]]):
        # each pixel that has a nonzero state
        color = [0, 0, 0]
        state = pixel[2]

        # set color according to state
        if state == 1:
            color = settings.snake_color
        elif state == 2:
            color = settings.apple_color

        # draw the individual pixel
        pygame.draw.rect(screen, color, pygame.Rect([
            settings.map_coordinates[0] + round(pixel[0] * settings.pixel_size),
            settings.map_coordinates[1] + round(pixel[1] * settings.pixel_size),
            np.ceil(settings.pixel_size),
            np.ceil(settings.pixel_size)
        ]))

    # display the score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {status.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # show the new frame
    pygame.display.flip()


def xy_to_n(coords, settings, reverse=False):
    """translate x and y position into the index in game map; reverse works the opposite
    input: any array with first and seconds items being int, for x and y respectively [x, y, ...]
    output: index n, an integer
    if reverse=True:
    input: index n, an integer
    output: an array in the form of [x, y]"""

    if not reverse:
        return coords[0] * settings.pixels + coords[1]

    return [int(coords / settings.pixels), coords - int(coords / settings.pixels)]


def update_snake_on_map(game_map, snake):
    """update map to correspond to snake positions"""
    if snake.was not in snake.whole:
        game_map.game_map[snake.was[0], snake.was[1], [2]] = 0
    game_map.game_map[snake.head[0], snake.head[1], [2]] = 1


def update_apple_on_map(game_map, apple):
    """update map to correspond to apple positions"""
    game_map.game_map[apple.pos[0], apple.pos[1], [2]] = 2


def update_snake(status, game_map, snake, apple, settings):
    """update the position of the snake and it's related statuses"""

    # move the snake
    if status.move_dir == "N":
        snake.head[1] -= 1
    elif status.move_dir == "E":
        snake.head[0] += 1
    elif status.move_dir == "S":
        snake.head[1] += 1
    elif status.move_dir == "W":
        snake.head[0] -= 1

    # check if snake hit an apple
    if snake.head[0] == apple.pos[0] and snake.head[1] == apple.pos[1]:
        status.apple_hit = True
        # TODO: move growing of snake and moving of apple to status dealing function
        snake.whole.append(snake.whole[-1])
        apple.pos = random.choice([y for x in game_map.game_map for y in x if not y[2]])
        status.score += 1  # P44cf

    # check if snake hit bad
    if snake.head in snake.whole[1:] or any([not 0 <= x < settings.pixels for x in snake.head]):
        status.self_hit, status.bad_hit = True, True
    else:
        # insert new head into snake body
        snake.whole.insert(0, snake.head[:])
        # update the position of where the snake was, aka the tail
        snake.was = snake.whole.pop()


def start_map(game_map, snake):
    """draw the whole snake onto the map at the start of the game"""
    for coords in snake.whole:
        game_map.game_map[coords[0], coords[1], 2] = 1


def destory_snake(game_map, snake):
    """snake has died, remove snake"""
    if snake.whole:
        dedsnek = snake.whole.pop(0)
        game_map.game_map[dedsnek[0], dedsnek[1], 2] = 0
    else:
        pygame.quit()
