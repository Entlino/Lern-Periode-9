import pygame
import snake
import tower_defense
import tetris

pygame.init()
fenster = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Spiele")

class Button:
    def __init__(self, rect, farbe, text, text_farbe):
        self.rect = pygame.Rect(rect)
        self.farbe = farbe
        self.text = text
        self.text_farbe = text_farbe
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.farbe, self.rect)
        text_surface = self.font.render(self.text, True, self.text_farbe)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

button_snake = Button(rect=(300, 150, 200, 50), farbe=(0, 200, 0), text="Snake", text_farbe=(255, 255, 255))
button_tower = Button(rect=(300, 250, 200, 50), farbe=(200, 0, 0), text="Tower Defense", text_farbe=(255, 255, 255))
button_tetris = Button(rect=(300, 350, 200, 50), farbe=(0, 0, 200), text="Tetris", text_farbe=(255, 255, 255))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if button_snake.is_clicked(pos):
                print("Snake starten ...")
                snake.start_game()
            elif button_tower.is_clicked(pos):
                print("Tower Defense starten ...")
                tower_defense.start_game()
            elif button_tetris.is_clicked(pos):
                print("Tetris starten ...")
                tetris.start_game()

    fenster.fill((0, 0, 0))
    button_snake.draw(fenster)
    button_tower.draw(fenster)
    button_tetris.draw(fenster)
    pygame.display.flip()

pygame.quit()