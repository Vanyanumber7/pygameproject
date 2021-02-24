from abc import abstractmethod
from random import choice

import pygame

FPS = 15
MYEVENTTYPE = pygame.USEREVENT + 1
all_sprites = pygame.sprite.Group()
currect_sprites = pygame.sprite.Group()
notcurrect_sprites = pygame.sprite.Group()

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
               [(0, -1), (1, 0), (-1, 0), (0, 0)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, -1), (-1, -1), (-1, 0), (1, -1)],
               [(0, -1), (-1, -1), (1, 0), (1, -1)],
               [(0, 0), (0, -1), (-1, -1), (-1, 0)]]
    return choice(figures)


class Board:
    # создание поля
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.color = {0: pygame.Color('black'), 1: pygame.Color('green'), 2: pygame.Color('red'),
                      3: pygame.Color('blue')}

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    @abstractmethod
    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color('white'), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)
                pygame.draw.rect(screen, self.color[self.board[y][x]], (
                    x * self.cell_size + self.left + 1, y * self.cell_size + self.top + 1, self.cell_size - 2,
                    self.cell_size - 2))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
            return cell_x, cell_y

    @abstractmethod
    def on_click(self, cell):
        if cell:
            self.board[cell[1]][cell[0]] = int(not self.board[cell[1]][cell[0]])


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(borders)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([5, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 5])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, color, *group):
        super().__init__(*group)
        self.a = 17
        self.image = pygame.Surface((self.a - 2, self.a -2),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, color,
                         (0, 0, self.a, self.a), 0)
        self.top, self.left = self.a * 2, self.a * 2
        self.w, self.h = 10, 20
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.a * (self.w // 2 + self.x) + 1 + self.left, \
                                                   self.a * (0 - self.y) + self.top + 1

    def update(self):
        global notcurrect_sprites, all_sprites, currect_sprites, flag, n, horizontal_borders
        self.rect = self.rect.move(0, self.a)
        if pygame.sprite.spritecollideany(self, notcurrect_sprites) or \
                pygame.sprite.spritecollideany(self, borders) or self.rect.y > 400:
            self.rect = self.rect.move(0, -self.a)
            flag = True
        else:
            self.rect = self.rect.move(0, -self.a)
            n += 1

    def turn(self):
        self.rect = self.rect.move(self.a * (-self.x - self.y), self.a * (self.y - self.x))
        self.x, self.y = -self.y, self.x

    def right(self):
        self.rect = self.rect.move(self.a, 0)

    def left_(self):
        self.rect = self.rect.move(-self.a, 0)

    def down(self):
        self.update()


def tetris(screen):
    global all_sprites, currect_sprites, notcurrect_sprites, flag, n
    board = [[0 for _ in range(10)] for _ in range(20)]
    clock = pygame.time.Clock()
    img = pygame.transform.scale(pygame.image.load('data/sprites/backgrounds/bg2.png'), (800, 600))
    running = True
    color, next_color = get_color(), get_color()
    figure, next_figure = get_figure(), get_figure()
    pygame.time.set_timer(MYEVENTTYPE, 1000)
    a = 17
    Border(2 * a, 2 * a - 5, 12 * a + 5, 2 * a - 5)
    Border(2 * a, 22 * a, 12 * a + 5, 22 * a)
    Border(2 * a, 2 * a, 2 * a, 22 * a + 5)
    Border(12 * a, 2 * a, 12 * a, 22 * a + 5)

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
                print(currect_sprites.update())
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            for i in currect_sprites:
                i.right()
        if keys[pygame.K_LEFT]:
            for i in currect_sprites:
                i.left_()
        if keys[pygame.K_DOWN]:
            for i in currect_sprites:
                i.down()
        screen.blit(img, (0, 0))
        if flag:
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
                n -= 4
        all_sprites.draw(screen)
        borders.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    tetris(screen)
    pygame.quit()
