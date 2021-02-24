from abc import abstractmethod
from random import choice

import pygame

FPS = 15
MYEVENTTYPE = pygame.USEREVENT + 1
all_sprites = pygame.sprite.Group()
currect_sprites = pygame.sprite.Group()
notcurrect_sprites = pygame.sprite.Group()


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


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, color, *group):
        super().__init__(*group)
        self.a = 45
        self.image = pygame.Surface((self.a, self.a),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, color,
                         (0, 0, self.a, self.a), 0)
        self.top, self.left = 10, 10
        self.w, self.h = 10, 20
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y, self.rect.size = self.a * (self.w // 2 + self.x) + self.left, \
                                                   self.a * (0 - self.y) + self.top, (self.a, self.a)

    def update(self):
        global notcurrect_sprites, all_sprites, currect_sprites
        if not pygame.sprite.spritecollideany(self, notcurrect_sprites) or self.rect.x > 500:
            self.rect = self.rect.move(0, self.a)
        else:
            notcurrect_sprites = all_sprites
            self.kill()
            color, next_color = get_color(), get_color()
            figure, next_figure = get_figure(), get_figure()
            pygame.time.set_timer(MYEVENTTYPE, 1000)
            for i in figure:
                Square(*i, color, currect_sprites, all_sprites)

    def turn(self):
        self.rect = self.rect.move(self.a * (-self.x - self.y), self.a * (self.y - self.x))
        self.x, self.y = -self.y, self.x

    def right(self):
        self.rect = self.rect.move(self.a, 0)

    def left_(self):
        self.rect = self.rect.move(-self.a, 0)

    def down(self):
        self.update()
        self.update()


def tetris(screen):
    global all_sprites, currect_sprites, notcurrect_sprites
    board = [[0 for _ in range(10)] for _ in range(20)]
    clock = pygame.time.Clock()
    running = True
    color, next_color = get_color(), get_color()
    figure, next_figure = get_figure(), get_figure()
    pygame.time.set_timer(MYEVENTTYPE, 1000)
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
            for i in currect_sprites:
                i.right()
        if keys[pygame.K_LEFT]:
            for i in currect_sprites:
                i.left_()
        if keys[pygame.K_DOWN]:
            for i in currect_sprites:
                i.down()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    tetris(screen)
    pygame.quit()
