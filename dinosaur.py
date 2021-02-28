import pygame


class Dinosaurs(pygame.sprite.Sprite):
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
        self.yvelocity += -500 // 15 * 1.5# Gravity
        self.y += self.yvelocity // 15 * 1.5
        if self.y <= 0:
            self.y = 0
            self.yvelocity = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.rect.y = self.surfaceHeight - self.y - self.rect.y