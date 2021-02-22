import pygame

FPS = 60

pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
