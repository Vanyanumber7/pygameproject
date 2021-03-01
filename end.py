import os
import random
import sys

import pygame
import sqlite3

def load_image(name, colorkey=None):
    fullname = os.path.join('data/image', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

screen_rect = (0, 0, 800, 600)
all_sprites = pygame.sprite.Group()

class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.25

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

def text_format(message, font, size, color):
    new_font = pygame.font.Font(font, size)
    new_text = new_font.render(message, 0, color)
    return new_text

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


font = "data/fonts/EvilEmpire-4BBVK.ttf"


def tetris_end(screen, table, score):
    # подключение базы данных
    con = sqlite3.connect('data/records.db')
    cur = con.cursor()
    records = cur.execute(f"""SELECT * FROM {table}""").fetchall()

    records.sort(reverse=True)
    running = True
    clock = pygame.time.Clock()
    list_of_elements = ['Retry', 'Menu', 'Exit']
    selected = 0
    f2 = True
    while running:
        f1 = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # выбор кнопки
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(list_of_elements)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(list_of_elements)
                if event.key == pygame.K_RETURN:
                    if list_of_elements[selected] == 'Exit':
                        pygame.quit()
                        quit()
                    else:
                        return list_of_elements[selected]

        screen.fill((0, 0, 0))

        # вывод рекордов и фейрверка
        screen.blit(text_format('Records:', font, 40, pygame.color.Color('white')),
                    (screen.get_width() // 16, screen.get_height() // 3))
        for i in range(1, 6):
            if i - 1 < len(records):
                if records[i - 1][0] == score and f1:
                    screen.blit(text_format(f'{i}. {records[i - 1][0]}', font, 50, pygame.color.Color('red')),
                                (screen.get_width() // 16, i * screen.get_height() // 12 + screen.get_height() // 3))
                    f1 = False
                    if i == 1 and f2:
                        for _ in range(9):
                            create_particles((random.randint(100, screen.get_width() - 100),
                                             random.randint(200, screen.get_height() - 200)))
                        f2 = False
                else:
                    screen.blit(text_format(f'{i}. {records[i - 1][0]}', font, 50, pygame.color.Color('white')),
                                (screen.get_width() // 16, i * screen.get_height() // 12 + screen.get_height() // 3))
            else:
                screen.blit(text_format(f'{i}. ---', font, 50, pygame.color.Color('white')),
                            (screen.get_width() // 16, i * screen.get_height() // 12 + screen.get_height() // 3))
        # отрисовка объектов
        title = text_format("Game over", font, 100, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - (title.get_rect()[2] / 2), 60))
        for i in range(len(list_of_elements)):
            if i == selected:
                text = text_format(list_of_elements[i], font, 75, (255, 255, 255))
                screen.blit(text, (screen.get_width() // 2 - (text.get_rect()[2] // 2),
                                   screen.get_height() // 8 * 3 + i * 70))
            else:
                text = text_format(list_of_elements[i], font, 75, (50, 50, 50))
                screen.blit(text, (screen.get_width() // 2 - (text.get_rect()[2] // 2),
                                   screen.get_height() // 8 * 3 + i * 70))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
        clock.tick(30)
