import pygame
import random
import numpy as np


class Settings:
    """a class for the settings of the game"""

    def __init__(self):
        self.screen_height = 840  # display height in pixels
        self.screen_width = self.screen_height * 1.5  # reference 1260 if height 840
        self.map_margin_factor = 0.05  # map height divided by display height, divided by two; all sides margin for map
        self.map_margin = round(self.screen_height * self.map_margin_factor)  # map margin in pixels
        self.map_height = self.screen_height - 2 * self.map_margin
        self.edge_width = 2  # thickness of the map edge
        self.pixels = 50  # pixels in a row, total is pixels^2; represents squares on the map not display pixels
        self.pixel_size = (self.screen_height - 2 * self.map_margin) / self.pixels  # map pixel in real pixels
        self.start_len = 3  # starting length of the snake
        self.background_color = [0, 0, 0]
        self.map_empty_color = [0, 0, 0]
        self.snake_color = [255, 255, 255]
        self.edge_color = [255, 255, 255]
        self.wall_color = [180, 180, 180]
        self.apple_color = [255, 0, 0]
        self.queue_len = 3  # maximum allowed length of event queue

        self.map_coordinates = np.array([self.map_margin,  # [x, y, width, height]
                                         self.map_margin,
                                         self.map_height,
                                         self.map_height])
        self.edge_coordinates = np.array([self.map_coordinates[0] - self.edge_width,  # [x, y, width, height]
                                          self.map_coordinates[1] - self.edge_width,
                                          self.map_coordinates[2] + 2 * self.edge_width,
                                          self.map_coordinates[3] + 2 * self.edge_width])


class Status:
    """a class for variable statuses and also easy communication between functions"""

    def __init__(self):
        self.move_dir = "N"  # current moving direction of the snake: N, E, W or S
        self.event_queue = []  # when multiple events happen in one move, store here (e.g. key presses)
        self.apple_hit = False
        self.self_hit = False
        self.wall_hit = False
        self.obst_hit = False
        self.bad_hit = False
        self.quit = False
        self.restart = False
        self.normal_map_update = True


class Snake:
    """a class for the snake itself"""

    def __init__(self, settings):
        # [x, y] starting position of the snake starting with it's head
        self.head = [settings.pixels - random.randint(max([int(settings.pixels / 10), settings.start_len + 1]),
                                                      int(settings.pixels / 2)) for _ in range(2)]
        # [[x1, y1], [x2, y2], ...] an array containing all locations where the snake (incl body) is
        self.whole = [[self.head[0], self.head[1] + i] for i in range(settings.start_len)]
        # [x, y] the position where the snake was the moment before
        self.was = [self.head[0], self.head[1] + settings.start_len]


class Map:
    """a class for the game map"""

    def __init__(self, settings):
        # [[x1, y1, state], [x1, y2, state], ..., [x2, y1, state], [x2, y2, state], ...] the whole map itself
        # states: {0: empty, 1: snake, 2: apple, 3: wall}
        self.game_map = np.array([[[x, y, 0] for y in range(settings.pixels)] for x in range(settings.pixels)])


class Apple:
    """a class for the apple"""

    def __init__(self, game_map):
        # [x, y] position of the apple, from every tile with state 0
        self.pos = random.choice([y for x in game_map.game_map for y in x if not y[2]])[:2]
