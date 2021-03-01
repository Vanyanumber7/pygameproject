import os
import sqlite3
import sys
from random import choice
import random
import pygame


def text_format(message, font, size, color):
    # формирование текста
    new_font = pygame.font.Font(font, size)
    new_text = new_font.render(message, 0, color)
    return new_text


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
    else:
        image = image.convert_alpha()
    return image


class Dinosaur(pygame.sprite.Sprite):
    # класс героя
    def __init__(self, sheet, columns, rows, x, y, surfaceHeight, all_sprites):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.jump_image = self.frames[0]
        self.kill_image = self.frames[-1]
        self.frames = self.frames[2:4]
        self.x = 60
        self.y = 0
        self.yvelocity = 0
        self.surfaceHeight = surfaceHeight
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.surfaceHeight - self.y - self.rect.height)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def jump(self):
        if (self.y == 0):
            self.yvelocity = 400
            self.image = self.jump_image

    def update(self, obstacles):
        if pygame.sprite.spritecollideany(self, obstacles):
            # проверка на столкнавение
            return True
        self.yvelocity += -500 // 15 * 2  # Gravity
        self.y += self.yvelocity // 15 * 1.5
        if self.y <= 0:
            # обновление картинки
            self.y = 0
            self.yvelocity = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.rect.y = self.surfaceHeight - self.y - self.rect.height


class Obstacle(pygame.sprite.Sprite):
    # класс препятствий
    def __init__(self, sheet, columns, rows, x, size, GroundHeight, all_sprites):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.image = choice(self.frames)
        self.size = size
        self.GroundHeight = GroundHeight
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = self.GroundHeight - self.size

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.rect.x -= 20

    def checkOver(self):
        # проверка на нахождение объекта
        if self.rect.x <= 0:
            return True
        else:
            return False


class Floor(pygame.sprite.Sprite):
    # класс пола
    def __init__(self, sheet, x, GroundHeight, all_sprites):
        super().__init__(all_sprites)
        self.all_sprites = all_sprites
        self.image = sheet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = GroundHeight - sheet.get_height()

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.rect.x <= -self.image.get_width():
            # если картинка ушла с поля, то убить
            self.kill()
            return False
        elif -self.image.get_width() + 820 <= self.rect.x < -self.image.get_width() + 840:
            # если картинка не закрывает всё поля, то создание нового
            self.rect.x -= 20
            return True
        else:
            # смещение пола влево
            self.rect.x -= 20
            return False


def dinosaur(screen):
    score = 0
    width, height = 640, 480
    GROUND_HEIGHT = height - 100  # высота пола
    clock = pygame.time.Clock()

    # создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    floors = pygame.sprite.Group()

    # подключение таймера
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 100)

    dinosaur = Dinosaur(load_image('dino.png', -1), 5, 1, 50, 50, GROUND_HEIGHT, all_sprites)

    # создание препятствий
    MINGAP = 200
    MAXGAP = 600
    lastObstacle = width

    for i in range(4):
        lastObstacle += MINGAP + (MAXGAP - MINGAP) * random.random()
        Obstacle(load_image('cactus.png', -1), 4, 1, lastObstacle, 50, GROUND_HEIGHT, obstacles)

    # создание пола
    Floor(load_image('floor.png', -1), 0, GROUND_HEIGHT, floors)

    white = 255, 255, 255
    while True:
        score += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # прыжок преснонажа
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            dinosaur.jump()

        if dinosaur.update(obstacles):
            # заненсение результата в бд
            con = sqlite3.connect('data/records.db')
            cur = con.cursor()
            cur.execute(f"""INSERT INTO dinosaur VALUES (?)""", (score,))
            con.commit()
            return screen, 'dinosaur', score

        screen.fill(white)

        for obs in obstacles:
            # обновление препятствий и изменение координат
            obs.update()
            if obs.checkOver():
                lastObstacle += MINGAP + (MAXGAP - MINGAP) * random.random()
                obs.rect.x = lastObstacle

        for f in floors:
            # обновление пола
            if f.update():
                Floor(load_image('floor.png', -1), screen.get_width() - 1, GROUND_HEIGHT, floors)

        # рисование объектов
        floors.draw(screen)
        obstacles.draw(screen)
        all_sprites.draw(screen)

        lastObstacle -= 20

        # вывод счетчика
        text = text_format(str(score), "data/fonts/EvilEmpire-4BBVK.ttf", 70, pygame.color.Color('grey'))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 30))

        pygame.display.flip()
        clock.tick(15 + score // 100)
