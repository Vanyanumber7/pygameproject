import pygame
from main_menu import main_menu
from tetris import tetris
from dinosaur import dinosaur
from end import tetris_end

FPS = 60

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
running = True
# подключаем музыку
tetris_sound = pygame.mixer.Sound('data/music/tetris.mp3')
dinosaur_sound = pygame.mixer.Sound('data/music/dinosaur.mp3')
end_sound = pygame.mixer.Sound('data/music/end.mp3')

while running:
    pygame.display.set_caption("Главное меню")
    # запускаем меню
    game = main_menu(screen)
    # запускаем игру по запросу
    if game == 'Tetris':
        while True:
            pygame.display.set_caption("Тетрис")
            tetris_sound.play(loops=-1)
            # запускаем заставку
            result = tetris(screen)
            tetris_sound.stop()
            end_sound.play()
            event = tetris_end(*result)
            pygame.display.set_caption("Конец игры")
            if event == 'Menu':
                break
    else:
        while True:
            pygame.display.set_caption("Динозавр")
            dinosaur_sound.play(loops=-1)
            result = dinosaur(screen)
            dinosaur_sound.stop()
            end_sound.play()
            event = tetris_end(*result)
            pygame.display.set_caption("Конец игры")
            if event == 'Menu':
                break
pygame.quit()
