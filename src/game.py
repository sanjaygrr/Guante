import pygame
import random
from settings import *


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
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.notes = []
        self.spawn_timer = 0
        self.running = True
        self.note_colors = [RED, GREEN, YELLOW, BLUE]
        self.note_positions = [100, 250, 400, 550]
        self.note_keys = [KEY_BINDINGS['left'], KEY_BINDINGS['up'],
                          KEY_BINDINGS['down'], KEY_BINDINGS['right']]
        self.score = 0

    def spawn_note(self):
        index = random.randint(0, 3)
        color = self.note_colors[index]
        position = self.note_positions[index]
        key = self.note_keys[index]
        new_note = Note(position, 0, 5, color, key)
        self.notes.append(new_note)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
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
        if self.spawn_timer == 0:
            self.spawn_note()
            self.spawn_timer = random.randint(30, 50)
        else:
            self.spawn_timer -= 1

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
