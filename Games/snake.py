import pygame
import random

from tetris import CELL_SIZE

pygame.init()
GRID_WIDTH = 20
GRID_HEIGHT = 20
CELL_SIZE = 20
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 36)

score = 0
high_score = 0

class Button:
    def __init__(self, rect, color, text, text_color, font):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))

def main_menu():
    menu_font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 24)
    title_text = menu_font.render("Snake", True, (0, 255, 0))
    start_button = Button((SCREEN_WIDTH//2 - 50, 200, 100, 50), (0, 200, 0), "Start", (255, 255, 255), small_font)
    highscore_button = Button((SCREEN_WIDTH//2 - 50, 270, 100, 50), (0, 0, 200), "High Scores", (255, 255, 255), small_font)

    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    menu_active = False
                elif highscore_button.is_clicked(event.pos):
                    show_high_scores()

        screen.fill((0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
        start_button.draw(screen)
        highscore_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)


def show_high_scores():
    global high_score
    info_font = pygame.font.Font(None, 36)
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                active = False
        screen.fill((50, 50, 50))
        hs_text = info_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        clock.tick(60)


def game_over_screen(score):
    global high_score
    game_over_font = pygame.font.Font(None, 48)
    info_font = pygame.font.Font(None, 24)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    score_text = info_font.render(f"Score: {score}", True, (255, 255, 255))
    restart_button = Button((SCREEN_WIDTH // 2 - 50, 250, 100, 50), (0, 200, 0), "Restart", (255, 255, 255), info_font)
    menu_button = Button((SCREEN_WIDTH // 2 - 50, 320, 100, 50), (0, 0, 200), "Menu", (255, 255, 255), info_font)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(event.pos):
                    return "restart"
                elif menu_button.is_clicked(event.pos):
                    return "menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_m:
                    return "menu"

        screen.fill((0, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 210))
        restart_button.draw(screen)
        menu_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)


def run_game():
    global score, high_score
    score = 0
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (0, -1)
    apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    MOVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE_EVENT, 150)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == MOVE_EVENT:
                head_x, head_y = snake[0]
                dx, dy = direction
                new_head = (head_x + dx, head_y + dy)

                if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                        new_head in snake):
                    running = False
                    continue

                snake.insert(0, new_head)
                if new_head == apple:
                    score += 1
                    while apple in snake:
                        apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                else:
                    snake.pop()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        screen.fill((0, 0, 0))
        draw_grid()

        apple_rect = pygame.Rect(apple[0] * CELL_SIZE, apple[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), apple_rect)

        for segment in snake:
            seg_rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), seg_rect)

        pygame.display.flip()
        clock.tick(60)

    if score > high_score:
        high_score = score
    return score


def start_game():
    while True:
        pygame.display.set_mode((400, 400))
        main_menu()
        current_score = run_game()
        option = game_over_screen(current_score)
        if option == "menu":
            continue
        elif option == "restart":

            continue


if __name__ == '__main__':
    start_game()
