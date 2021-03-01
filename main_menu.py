import pygame


def text_format(message, font, size, color):
    new_font = pygame.font.Font(font, size)
    new_text = new_font.render(message, 0, color)
    return new_text


font = "data/fonts/EvilEmpire-4BBVK.ttf"


def main_menu(screen):
    running = True
    list_of_elements = ['Dinosaur', 'Tetris', 'Exit']
    selected = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # выбор объекта
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
        # отрисовка элементов
        title = text_format("My world", font, 100, (255, 255, 255))
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

        pygame.display.update()
        pygame.time.Clock().tick(30)
