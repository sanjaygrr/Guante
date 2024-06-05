import pygame
import os


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        self.main_menu_options = ["Guitar Hero"] + ["Vacío"] * 8
        self.key_options = ["1 tecla", "2 teclas", "3 teclas", "4 teclas"]
        self.songs = self.get_song_files()
        self.selected_main_menu_option = 0
        self.selected_key_option = 0
        self.selected_song_option = 0
        self.stage = 0  # 0: seleccionar juego, 1: seleccionar teclas, 2: seleccionar canción

    def get_song_files(self):
        song_files = []
        song_directory = 'assets'
        for root, dirs, files in os.walk(song_directory):
            for file in files:
                if file.endswith('.ogg'):
                    song_files.append(os.path.join(root, file))
        return song_files

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            if self.stage == 0:
                self.draw_main_menu()
            elif self.stage == 1:
                self.draw_options(self.key_options, self.selected_key_option)
            else:
                self.draw_options([os.path.basename(song)
                                  for song in self.songs], self.selected_song_option)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.stage == 0:
                            self.selected_main_menu_option = (
                                self.selected_main_menu_option - 1) % len(self.main_menu_options)
                        elif self.stage == 1:
                            self.selected_key_option = (
                                self.selected_key_option - 1) % len(self.key_options)
                        else:
                            self.selected_song_option = (
                                self.selected_song_option - 1) % len(self.songs)
                    elif event.key == pygame.K_DOWN:
                        if self.stage == 0:
                            self.selected_main_menu_option = (
                                self.selected_main_menu_option + 1) % len(self.main_menu_options)
                        elif self.stage == 1:
                            self.selected_key_option = (
                                self.selected_key_option + 1) % len(self.key_options)
                        else:
                            self.selected_song_option = (
                                self.selected_song_option + 1) % len(self.songs)
                    elif event.key == pygame.K_RETURN:
                        if self.stage == 0:
                            if self.main_menu_options[self.selected_main_menu_option] == "Vacío":
                                print("No se ha creado función")
                            else:
                                self.stage = 1
                        elif self.stage == 1:
                            self.stage = 2
                        else:
                            running = False
                            return self.selected_key_option + 1, self.songs[self.selected_song_option]

    def draw_main_menu(self):
        title = self.title_font.render(
            "Seleccionar actividad para guante", True, (255, 255, 255))
        self.screen.blit(title, (100, 50))

        for i in range(9):
            color = (255, 0, 0) if i == self.selected_main_menu_option else (
                255, 255, 255)
            rect = pygame.Rect(100 + (i % 3) * 200, 150 +
                               (i // 3) * 150, 150, 100)
            pygame.draw.rect(self.screen, color, rect, 2)
            text = self.font.render(self.main_menu_options[i], True, color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_options(self, options, selected_index):
        for i, option in enumerate(options):
            color = (255, 0, 0) if i == selected_index else (255, 255, 255)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (100, 100 + i * 40))
