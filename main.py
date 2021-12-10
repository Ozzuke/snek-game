import pygame
import game_functions as gf
import classes


def run_game():
    """start running the snake game"""

    # init the pygame module
    pygame.init()
    # init the settings class
    settings = classes.Settings()
    # set the game window
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    # set the window name
    pygame.display.set_caption("Snake")

    # init the built in pygame clock
    clock = pygame.time.Clock()
    # init the snake class
    snake = classes.Snake(settings)
    # init the game map class
    game_map = classes.Map(settings)
    # init the apple class
    apple = classes.Apple(game_map)
    # init the status class
    status = classes.Status()
    # draw the whole snake onto the screen
    gf.start_map(game_map, snake)

    while True:
        # the main loop of the game

        gf.check_events(settings, status)
        if status.normal_map_update:
            gf.update_snake(status, game_map, snake, apple, settings)
        if not status.bad_hit:
            gf.update_snake_on_map(game_map, snake)
            gf.update_apple_on_map(game_map, apple)
        else:
            status.normal_map_update = False
            gf.destory_snake(game_map, snake)
            settings.snake_color = [180, 0, 0]
            pygame.time.wait(200)
        gf.draw_screen(screen, settings, game_map)

        if status.quit:
            pygame.quit()

        clock.tick(15)


if __name__ == "__main__":
    run_game()
