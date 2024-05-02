import pygame
import game_functions as gf
import classes

def title_screen(settings, screen):
    """Display the title screen with options to play, settings, or quit."""
    title_font = pygame.font.SysFont(None, 48)
    options_font = pygame.font.SysFont(None, 36)
    options = ["Play", "Settings", "Quit"]
    selected_option = 0

    while True:
        screen.fill(settings.background_color)
        title_text = title_font.render("Snake Game", True, (255, 255, 255))
        screen.blit(title_text, (settings.screen_width / 2 - title_text.get_width() / 2, 100))

        for i, option in enumerate(options):
            if i == selected_option:
                option_text = options_font.render(option, True, (255, 0, 0))
            else:
                option_text = options_font.render(option, True, (255, 255, 255))
            screen.blit(option_text, (settings.screen_width / 2 - option_text.get_width() / 2, 200 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'Quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_option > 0:
                    selected_option -= 1
                elif event.key == pygame.K_DOWN and selected_option < len(options) - 1:
                    selected_option += 1
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]

def settings_screen(settings, screen):
    """Display the settings screen for adjusting game settings."""
    settings_font = pygame.font.SysFont(None, 36)
    options = ["Back"]
    selected_option = 0

    while True:
        screen.fill(settings.background_color)
        settings_text = settings_font.render("Settings (Placeholder)", True, (255, 255, 255))
        screen.blit(settings_text, (settings.screen_width / 2 - settings_text.get_width() / 2, 100))

        for i, option in enumerate(options):
            if i == selected_option:
                option_text = settings_font.render(option, True, (255, 0, 0))
            else:
                option_text = settings_font.render(option, True, (255, 255, 255))
            screen.blit(option_text, (settings.screen_width / 2 - option_text.get_width() / 2, 200 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'Quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return options[selected_option]

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

    # Display the title screen
    action = title_screen(settings, screen)
    if action == "Quit":
        return
    elif action == "Settings":
        settings_screen(settings, screen)
        action = title_screen(settings, screen)
        if action == "Quit":
            return

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
