import pygame
from game import Game
from menu import Menu
from settings import *
import os


def generate_timing_file(audio_path):
    timing_file = os.path.splitext(audio_path)[0] + '_timing.txt'
    if not os.path.exists(timing_file):
        import librosa
        y, sr = librosa.load(audio_path)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(
            beat_frames, sr=sr) * 1000  # Convertir a milisegundos
        with open(timing_file, 'w') as f:
            for time in beat_times:
                f.write(f"{int(time)}\n")
        print(f"Timing file created: {timing_file}")
    else:
        print(f"Timing file already exists: {timing_file}")
    return timing_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Selector")

    menu = Menu(screen)
    num_keys, selected_song = menu.run()

    if num_keys:
        timing_file = generate_timing_file(selected_song)
        game = Game(screen, num_keys, selected_song, timing_file)
        game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
