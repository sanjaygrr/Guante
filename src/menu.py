import pygame
from settings import *


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.options = ["Start Game", "Settings", "Quit"]
        self.selected_option = 0
        self.settings_selected = 0
        self.in_settings = False
        self.settings_options = ["Control: Arrows", "Control: WASD"]

    def display_menu(self):
        self.screen.fill(BLACK)
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = YELLOW
            else:
                color = WHITE
            text = self.font.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() //
                             2, SCREEN_HEIGHT // 2 - 100 + i * 100))
        pygame.display.flip()

    def display_settings(self):
        self.screen.fill(BLACK)
        for i, option in enumerate(self.settings_options):
            if i == self.settings_selected:
                color = YELLOW
            else:
                color = WHITE
            text = self.font.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() //
                             2, SCREEN_HEIGHT // 2 - 100 + i * 100))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.in_settings:
                        if event.key == pygame.K_UP:
                            self.selected_option = (
                                self.selected_option - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (
                                self.selected_option + 1) % len(self.options)
                        elif event.key == pygame.K_RETURN:
                            if self.selected_option == 0:  # Start Game
                                return "start_game"
                            elif self.selected_option == 1:  # Settings
                                self.in_settings = True
                            elif self.selected_option == 2:  # Quit
                                return "quit"
                    else:
                        if event.key == pygame.K_UP:
                            self.settings_selected = (
                                self.settings_selected - 1) % len(self.settings_options)
                        elif event.key == pygame.K_DOWN:
                            self.settings_selected = (
                                self.settings_selected + 1) % len(self.settings_options)
                        elif event.key == pygame.K_RETURN:
                            if self.settings_selected == 0:  # Control: Arrows
                                KEY_BINDINGS.update({'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                                                    'up': pygame.K_UP, 'down': pygame.K_DOWN, 'action': pygame.K_SPACE})
                            elif self.settings_selected == 1:  # Control: WASD
                                KEY_BINDINGS.update(
                                    {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s, 'action': pygame.K_SPACE})
                            self.in_settings = False
            if self.in_settings:
                self.display_settings()
            else:
                self.display_menu()
