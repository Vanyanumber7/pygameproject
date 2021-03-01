from random import choice
import pygame
import sqlite3

FPS = 15
MYEVENTTYPE = pygame.USEREVENT + 1

# создание группы спрайтов
all_sprites = pygame.sprite.Group()
currect_sprites = pygame.sprite.Group()
notcurrect_sprites = pygame.sprite.Group()

# создание поля
board = [[0 for _ in range(10)] for _ in range(20)]

# создание группы спрайтов
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
borders = pygame.sprite.Group()

# флаг и ширина квадрата
flag = False
a = 17


def text_format(message, font, size, color):
    new_font = pygame.font.Font(font, size)
    new_text = new_font.render(message, 0, color)
    return new_text


def get_color():
    # получение цвета
    colors = ['red', 'orange', 'yellow', 'blue', 'purple', 'green', 'pink']
    return pygame.color.Color(choice(colors))


def get_figure():
    # получение фигуры
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
            self.image.fill((255, 255, 255))
            self.rect = pygame.Rect(x1, y1, 5, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 5])
            self.image.fill((255, 255, 255))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 5)


class Square(pygame.sprite.Sprite):
    # класс квадратиков
    def __init__(self, x, y, top, left, color, *group):
        super().__init__(*group)
        self.a = 27
        self.image = pygame.Surface((self.a - 2, self.a - 2),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, color,
                         (0, 0, self.a, self.a), 0)
        self.w, self.h = 10, 20

        # смещение от точки (0;0)
        self.top = top
        self.left = left

        # координаты на поле
        self.x, self.y = x, y
        self.xx = self.x + self.w // 2
        self.yy = abs(self.y)

        self.rect = self.image.get_rect()
        self.rect.x = self.a * (self.w // 2 + self.x) + 1 + self.left
        self.rect.y = self.a * (0 - self.y) + self.top + 1

    def update(self):
        global notcurrect_sprites, all_sprites, currect_sprites, flag, horizontal_borders
        self.rect = self.rect.move(0, self.a)
        if pygame.sprite.spritecollideany(self, notcurrect_sprites) or \
                pygame.sprite.spritecollideany(self, horizontal_borders) or board[self.yy][self.xx]:
            # проверка на столкновение
            flag = True
        self.rect = self.rect.move(0, -self.a)

    def turn(self):
        # проверка на поворот фигуры
        self.rect = self.rect.move(self.a * (-self.x - self.y), self.a * (self.y - self.x))
        if pygame.sprite.spritecollideany(self, notcurrect_sprites) or \
                pygame.sprite.spritecollideany(self, borders):
            # проверка на столкновение
            self.rect = self.rect.move(self.a * (self.x + self.y), self.a * (-self.y + self.x))
            return False
        self.rect = self.rect.move(self.a * (self.x + self.y), self.a * (-self.y + self.x))
        return True

    def right(self):
        # проверка на возможность сдвига вправо
        self.rect = self.rect.move(self.a, 0)
        if pygame.sprite.spritecollideany(self, notcurrect_sprites) or \
                pygame.sprite.spritecollideany(self, vertical_borders) or board[self.yy][self.xx]:
            # проверка на столкновение
            self.rect = self.rect.move(-self.a, 0)
            return False
        self.rect = self.rect.move(-self.a, 0)
        return True

    def left_(self):
        # проверка на возможность сдвига влево
        self.rect = self.rect.move(-self.a, 0)
        if pygame.sprite.spritecollideany(self, notcurrect_sprites) or \
                pygame.sprite.spritecollideany(self, vertical_borders) or board[self.yy][self.xx]:
            # проверка на столкновение
            self.rect = self.rect.move(self.a, 0)
            return False
        self.rect = self.rect.move(self.a, 0)
        return True


def tetris(screen):
    global all_sprites, currect_sprites, notcurrect_sprites, flag, board

    clock = pygame.time.Clock()
    img = pygame.transform.scale(pygame.image.load('data/image/fon.jpg'), (800, 600))
    running = True

    # получение фигур и цветов
    color, next_color = get_color(), get_color()
    figure, next_figure = get_figure(), get_figure()

    pygame.time.set_timer(MYEVENTTYPE, 1000)
    w, h, a = 10, 20, 27
    top = screen.get_height() // 2 - h // 2 * a
    left = screen.get_width() // 4 - w // 2 * a

    # создание стенок
    Border(left - 5, top - 5, left + 10 * a + 5, top - 5)
    Border(left - 5, top + 20 * a, left + 10 * a + 5, top + 20 * a)
    Border(left - 5, top - 5, left - 5, top + 20 * a + 5)
    Border(left + 10 * a, top - 5, left + 10 * a, top + 20 * a + 5)

    # подключение шрифтов
    main_font = ('data/fonts/font.ttf', 65)
    font = ('data/fonts/font.ttf', 45)

    # создание текстов
    title_tetris = text_format('TETRIS', *main_font, pygame.Color('darkorange'))
    title_score = text_format('score:', *font, pygame.Color('green'))
    title_record = text_format('level:', *font, pygame.Color('purple'))
    # показ новой фигуры
    for i in next_figure:
        pygame.draw.rect(screen, next_color, (i[0] * a + 580, i[1] * a + 380, a, a), 0)

    score, levels = 0 , 1

    for i in figure:
        Square(*i, top, left, color, currect_sprites, all_sprites)

    while running:
        # проверка на завершение игры
        if sum(board[0]) > 0:
            con = sqlite3.connect('data/records.db')
            cur = con.cursor()
            cur.execute(f"""INSERT INTO tetris VALUES (?)""", (score, ))
            con.commit()
            return screen, 'tetris', score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # поворот фигуры
                    if all(i.turn() for i in currect_sprites):
                        for i in currect_sprites:
                            i.rect = i.rect.move(i.a * (-i.x - i.y), i.a * (i.y - i.x))
                            i.xx += -i.y - i.x
                            i.yy += i.y - i.x
                            i.x, i.y = -i.y, i.x

            if event.type == MYEVENTTYPE:
                # автоматическое перемещение фигуры вниз
                currect_sprites.update()
                if flag:
                    for i in currect_sprites:
                        board[i.yy][i.xx] = 1
                    notcurrect_sprites = all_sprites.copy()
                    currect_sprites = pygame.sprite.Group()
                    color, next_color = next_color, get_color()
                    figure, next_figure = next_figure, get_figure()
                    for i in figure:
                        Square(*i, top, left, color, currect_sprites, all_sprites)
                    flag = False
                else:
                    for i in currect_sprites:
                        i.rect = i.rect.move(0, i.a)
                        i.yy += 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            # сдвиг вправо
            if all(i.right() for i in currect_sprites):
                for i in currect_sprites:
                    i.rect = i.rect.move(i.a, 0)
                    i.xx += 1

        if keys[pygame.K_LEFT]:
            # сдвиг влево
            if all(i.left_() for i in currect_sprites):
                for i in currect_sprites:
                    i.rect = i.rect.move(-i.a, 0)
                    i.xx -= 1

        if keys[pygame.K_DOWN]:
            pygame.event.post(pygame.event.Event(MYEVENTTYPE))

        screen.blit(img, (0, 0))

        for y in range(len(board)):
            # проверка на заполненность ряда
            if sum(board[y]) == 10:
                score += 100
                for i in notcurrect_sprites:
                    if i.yy == y:
                        i.kill()
                    else:
                        if i.yy < y:
                            i.yy += 1
                            i.rect = i.rect.move(0, i.a)
                board = [list(0 for i in range(10))] + board[:y] + board[y + 1:]

        # обновление уровня
        if levels < score // 4000 + 1:
            levels = score // 4000 + 1
            pygame.time.set_timer(MYEVENTTYPE, (6 - levels) * 100)

        # отрисовка отбъектов и следующей фигуры
        all_sprites.draw(screen)
        borders.draw(screen)
        for i in next_figure:
            pygame.draw.rect(screen, next_color, (2 * i[0] * a + 1 + screen.get_width() // 4 * 3 - a,
                                                  2 * -i[1] * a + 1 + screen.get_height() // 3, 2 * a - 4, 2 * a - 4),
                             0)

        screen.blit(title_tetris,
                    (screen.get_width() // 4 * 3 - title_tetris.get_width() // 2, screen.get_height() // 32))
        screen.blit(title_score, (screen.get_width() // 4 * 3 - title_score.get_width() // 2, screen.get_height() // 2))
        text = text_format(str(score), *font, pygame.color.Color('blue'))
        screen.blit(text, (screen.get_width() // 4 * 3 - text.get_width() // 2, screen.get_height() // 10 * 6))
        screen.blit(title_record,
                    (screen.get_width() // 4 * 3 - title_record.get_width() // 2, screen.get_height() // 4 * 3))
        text = text_format(str(levels), *font, pygame.color.Color('blue'))
        screen.blit(text, (screen.get_width() // 4 * 3 - text.get_width() // 2, screen.get_height() // 6 * 5))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    tetris(screen)
    pygame.quit()
