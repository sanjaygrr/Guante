import pygame
import random
from settings import *
import os


class Note:
    def __init__(self, x, y, speed, color, key):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.key = key
        self.rect = pygame.Rect(x, y, 50, 50)

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Game:
    def __init__(self, screen, num_keys, music_file, timing_file):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.notes = []
        self.running = True
        self.note_colors = [RED, GREEN, YELLOW, BLUE][:num_keys]
        self.note_positions = [100, 250, 400, 550][:num_keys]
        self.note_keys = [KEY_BINDINGS['left'], KEY_BINDINGS['up'],
                          KEY_BINDINGS['down'], KEY_BINDINGS['right']][:num_keys]
        self.score = 0
        self.timing = []
        self.music_file = music_file
        self.timing_file = timing_file
        self.load_timing()
        self.music_start_ticks = None

    def load_timing(self):
        with open(self.timing_file, 'r') as file:
            for line in file:
                time = int(line.strip())
                if time > 0:
                    self.timing.append(time)
                    # Print para depuración
                    print(f"Note timing added: {time} ms")

    def spawn_note_at_time(self, current_time):
        while self.timing and current_time >= self.timing[0]:
            # Asegurar rotación de colores y posiciones
            index = len(self.notes) % len(self.note_colors)
            color = self.note_colors[index]
            position = self.note_positions[index]
            key = self.note_keys[index]
            new_note = Note(position, 0, 5, color, key)
            self.notes.append(new_note)
            # Print para depuración
            print(
                f"Note spawned at: {current_time} ms, position: {position}, color: {color}")
            self.timing.pop(0)

    def run(self):
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play()
        self.music_start_ticks = pygame.time.get_ticks()

        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.mixer.music.stop()
            elif event.type == pygame.KEYDOWN:
                self.check_key(event.key)

    def check_key(self, key):
        for note in self.notes:
            if note.key == key and note.rect.colliderect(pygame.Rect(note.x, SCREEN_HEIGHT - 50, 50, 50)):
                self.notes.remove(note)
                self.score += 1
                print("Score:", self.score)
                break

    def update(self):
        current_time = pygame.time.get_ticks() - self.music_start_ticks
        self.spawn_note_at_time(current_time)

        for note in self.notes:
            note.move()
            if note.y > SCREEN_HEIGHT:
                self.notes.remove(note)

    def draw(self):
        self.screen.fill(WHITE)
        for i, color in enumerate(self.note_colors):
            pygame.draw.line(self.screen, color, (
                self.note_positions[i] + 25, 0), (self.note_positions[i] + 25, SCREEN_HEIGHT), 5)
            key_text = pygame.font.Font(None, 36).render(
                pygame.key.name(self.note_keys[i]), True, BLACK)
            self.screen.blit(
                key_text, (self.note_positions[i] + 5, SCREEN_HEIGHT - 45))
        for note in self.notes:
            note.draw(self.screen)
        pygame.display.flip()
