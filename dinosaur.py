import os
import sys
from random import choice

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
            quit()
        self.yvelocity += -500 // 15 * 1.5  # Gravity
        self.y += self.yvelocity // 15 * 1.5
        if self.y <= 0:
            self.y = 0
            self.yvelocity = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.rect.y = self.surfaceHeight - self.y - self.rect.y


class Obstacle(pygame.sprite.Sprite):
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
        if self.rect.x <= 0:
            return True
        else:
            return False


class Floor(pygame.sprite.Sprite):
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
            self.kill()
            return False
        elif -self.image.get_width() + 680 <= self.rect.x < -self.image.get_width() + 700:
            self.rect.x -= 20
            return True
        else:
            self.rect.x -= 20
            return False

    def checkOver(self):
        return False
