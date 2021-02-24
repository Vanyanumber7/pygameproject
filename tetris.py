from abc import abstractmethod
from random import choice
import pprint
import pygame

FPS = 15
MYEVENTTYPE = pygame.USEREVENT + 1
all_sprites = pygame.sprite.Group()
currect_sprites = pygame.sprite.Group()
notcurrect_sprites = pygame.sprite.Group()

board = [[0 for _ in range(10)] for _ in range(20)]

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
borders = pygame.sprite.Group()
flag = False
n = 0
a = 17


def get_color():
    colors = ['red', 'orange', 'yellow', 'blue', 'purple', 'green', 'pink']
    return pygame.color.Color(choice(colors))


def get_figure():
    figures = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (1, 0), (0, 0)],
               [(0, -1), (-1, 0), (1, -1), (0, 0)],
               [(-1, 0), (0, 0), (0, -1), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (1, -1)],
               [(0, -1), (-1, -1), (1, 0), (1, -1)],
               [(0, 0), (0, -1), (-1, -1), (-1, 0)]]
    return choice(figures)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(borders)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([5, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 5, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 5])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 5)


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, color, *group):
        super().__init__(*group)
        self.a = 17
        self.image = pygame.Surface((self.a - 2, self.a - 2),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, color,
                         (0, 0, self.a, self.a), 0)
        self.top, self.left = self.a * 2, self.a * 2
        self.w, self.h = 10, 20
        self.x, self.y = x, y
        self.xx, self.yy = 0, 0
        self.xxx, self.yyy = 0, 0
        self.xx += self.x + self.w // 2
        self.yy += abs(self.y)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.a * (self.w // 2 + self.x) + 1 + self.left, \
                                   self.a * (0 - self.y) + self.top + 1

    def update(self):
        global notcurrect_sprites, all_sprites, currect_sprites, flag, n, horizontal_borders
        self.rect = self.rect.move(0, self.a)
        if pygame.sprite.spritecollideany(self, notcurrect_sprites) or \
                pygame.sprite.spritecollideany(self, horizontal_borders) or board[self.yy][self.xx]:
            flag = True
        else:
            n += 1
        self.rect = self.rect.move(0, -self.a)

    def turn(self):
        self.rect = self.rect.move(self.a * (-self.x - self.y), self.a * (self.y - self.x))
        if pygame.sprite.spritecollideany(self, notcurrect_sprites) or \
                pygame.sprite.spritecollideany(self, borders):
            self.rect.move(self.a * (self.x + self.y), self.a * (-self.y + self.x))
            return
        self.xx += -self.y - self.x
        self.yy += self.y - self.x
        self.x, self.y = -self.y, self.x


    def right(self):
        self.rect = self.rect.move(self.a, 0)
        if pygame.sprite.spritecollideany(self, notcurrect_sprites) or \
                pygame.sprite.spritecollideany(self, vertical_borders) or board[self.yy][self.xx]:
            self.rect = self.rect.move(-self.a, 0)
            return False
        self.rect = self.rect.move(-self.a, 0)
        return True

    def left_(self):
        self.rect = self.rect.move(-self.a, 0)
        if pygame.sprite.spritecollideany(self, notcurrect_sprites) or \
                pygame.sprite.spritecollideany(self, vertical_borders) or board[self.yy][self.xx]:
            self.rect = self.rect.move(self.a, 0)
            return False
        self.rect = self.rect.move(self.a, 0)
        return True

    def down(self):
        self.update()


def tetris(screen):
    global all_sprites, currect_sprites, notcurrect_sprites, flag, n, board
    clock = pygame.time.Clock()
    img = pygame.transform.scale(pygame.image.load('data/sprites/backgrounds/bg2.png'), (800, 600))
    running = True
    color, next_color = get_color(), get_color()
    figure, next_figure = get_figure(), get_figure()
    pygame.time.set_timer(MYEVENTTYPE, 1000)
    a = 17
    Border(2 * a - 5, 2 * a - 5, 12 * a + 5, 2 * a - 5)
    Border(2 * a - 5, 22 * a, 12 * a + 5, 22 * a)
    Border(2 * a - 5, 2 * a - 5, 2 * a - 5, 22 * a + 5)
    Border(12 * a, 2 * a - 5, 12 * a, 22 * a + 5)

    main_font = pygame.font.Font('data/fonts/font.ttf', 65)
    font = pygame.font.Font('data/fonts/font.ttf', 45)

    title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
    title_score = font.render('score:', True, pygame.Color('green'))
    title_record = font.render('record:', True, pygame.Color('purple'))

    score, lines = 0, 0
    scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    for i in figure:
        Square(*i, color, currect_sprites, all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    for i in currect_sprites:
                        i.turn()

            if event.type == MYEVENTTYPE:
                currect_sprites.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if all(i.right() for i in currect_sprites):
                for i in currect_sprites:
                    i.rect = i.rect.move(i.a, 0)
                    i.xx += 1

        if keys[pygame.K_LEFT]:
            if all(i.left_() for i in currect_sprites):
                for i in currect_sprites:
                    i.rect = i.rect.move(-i.a, 0)
                    i.xx -= 1
        if keys[pygame.K_DOWN]:
            for i in currect_sprites:
                i.down()
        screen.blit(img, (0, 0))
        if flag:
            for i in currect_sprites:
                board[i.yy][i.xx] = 1
            notcurrect_sprites = all_sprites.copy()
            currect_sprites = pygame.sprite.Group()
            color, next_color = get_color(), get_color()
            figure, next_figure = get_figure(), get_figure()
            pygame.time.set_timer(MYEVENTTYPE, 1000)
            for i in figure:
                Square(*i, color, currect_sprites, all_sprites)
            flag = False
        else:
            if n > 0:
                for i in currect_sprites:
                    i.rect = i.rect.move(0, i.a)
                    i.yy += 1
                n -= 4
        for y in range(len(board)):
            if sum(board[y]) == 10:
                for i in notcurrect_sprites:
                    if i.yy == y:
                        i.kill()
                    else:
                        if i.yy < y:
                            i.yy += 1
                            i.rect = i.rect.move(0, i.a)
                board = [list(0 for i in range(10))] + board[:y] + board[y + 1:]
        pprint.pprint(board)
        all_sprites.draw(screen)
        borders.draw(screen)

        screen.blit(title_tetris, (485, -10))
        screen.blit(title_score, (535, 780))
        screen.blit(font.render(str(score), True, pygame.Color('white')), (550, 840))
        screen.blit(title_record, (525, 650))


        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    tetris(screen)
    pygame.quit()