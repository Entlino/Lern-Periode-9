import pygame
import random

ROWS = 20
COLS = 10
score = 0
high_score = 0

TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]]
}

CELL_SIZE = 30
BOARD_OFFSET_X = (400 - COLS * CELL_SIZE) // 2
BOARD_OFFSET_Y = 0

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (200, 200, 200),
                                 (BOARD_OFFSET_X + x * CELL_SIZE, BOARD_OFFSET_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, (50, 50, 50),
                                 (BOARD_OFFSET_X + x * CELL_SIZE, BOARD_OFFSET_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def is_valid_position(board, shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board_x = offset_x + x
                board_y = offset_y + y
                if board_x < 0 or board_x >= COLS or board_y >= ROWS:
                    return False
                if board_y >= 0 and board[board_y][board_x]:
                    return False
    return True

def draw_tetromino(screen, tetromino):
    shape = tetromino.get_current_shape()
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (255, 0, 0),
                                 (BOARD_OFFSET_X + (tetromino.x + x) * CELL_SIZE, BOARD_OFFSET_Y + (tetromino.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def add_to_board(board, shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[offset_y + y][offset_x + x] = cell

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(COLS)])
    return new_board, lines_cleared


def game_over_screen(score, screen):
    # Erstelle einen kleineren Font für die Anzeige
    game_over_font = pygame.font.Font(None, 36)
    info_font = pygame.font.Font(None, 24)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    score_text = info_font.render(f"Score: {high_score}", True, (255, 255, 255))
    restart_text = info_font.render("Drücke R für Restart oder Q für Quit", True, (255, 255, 255))

    # Endlosschleife für den Game Over Bildschirm
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False  # Quit

        screen.fill((0, 0, 0))

        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 150))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 200))
        screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, 250))
        pygame.display.flip()


class Tetromino:
    def __init__(self, tetromino_type):
        self.type = tetromino_type
        self.rotation = 0
        self.shape = TETROMINOS[tetromino_type]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def get_current_shape(self):
        return self.shape


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


def show_high_scores(screen, font):
    high_scores_active = True
    while high_scores_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                high_scores_active = False

        screen.fill((50, 50, 50))
        score_text = font.render(f"High Scores: {score}", True, (255, 255, 255))
        screen.blit(score_text, (100, 250))
        pygame.display.flip()


def main_menu(screen):
    font = pygame.font.Font(None, 36)
    start_button = Button((150, 200, 100, 50), (0, 200, 0), "Start", (255, 255, 255), font)
    highscore_button = Button((150, 300, 100, 50), (0, 0, 200), "High Scores", (255, 255, 255), font)

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
                    show_high_scores(screen, font)

        screen.fill((0, 0, 0))
        start_button.draw(screen)
        highscore_button.draw(screen)
        pygame.display.flip()

def start_game():
    global score, high_score
    score = 0
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()


    main_menu(screen)


    board = create_board()
    font = pygame.font.Font(None, 48)

    active_tetromino = Tetromino(random.choice(list(TETROMINOS.keys())))

    DROP_EVENT = pygame.USEREVENT + 1
    drop_delay = 500
    pygame.time.set_timer(DROP_EVENT, drop_delay)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == DROP_EVENT:
                new_y = active_tetromino.y + 1
                if is_valid_position(board, active_tetromino.get_current_shape(), active_tetromino.x, new_y):
                    active_tetromino.y = new_y
                else:
                    add_to_board(board, active_tetromino.get_current_shape(), active_tetromino.x, active_tetromino.y)
                    board, lines_cleared = clear_lines(board)
                    score += lines_cleared * 100
                    new_tetromino = Tetromino(random.choice(list(TETROMINOS.keys())))
                    if not is_valid_position(board, new_tetromino.get_current_shape(), new_tetromino.x, new_tetromino.y):
                        print("Game Over! Score:", score)
                        if score > high_score:
                            high_score = score
                        restart = game_over_screen(score, screen)
                        if restart:
                            main_menu(screen)
                            board = create_board()
                        else:
                            running = False
                    else:
                        active_tetromino = new_tetromino

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_x = active_tetromino.x - 1
                    if is_valid_position(board, active_tetromino.get_current_shape(), new_x, active_tetromino.y):
                        active_tetromino.x = new_x
                elif event.key == pygame.K_RIGHT:
                    new_x = active_tetromino.x + 1
                    if is_valid_position(board, active_tetromino.get_current_shape(), new_x, active_tetromino.y):
                        active_tetromino.x = new_x
                elif event.key == pygame.K_DOWN:
                    new_y = active_tetromino.y + 1
                    if is_valid_position(board, active_tetromino.get_current_shape(), active_tetromino.x, new_y):
                        active_tetromino.y = new_y
                elif event.key == pygame.K_UP:
                    # Rotation: Hier erzeugen wir eine gedrehte Version der aktuellen Form.
                    rotated_shape = [list(row) for row in zip(*active_tetromino.get_current_shape()[::-1])]
                    if is_valid_position(board, rotated_shape, active_tetromino.x, active_tetromino.y):
                        active_tetromino.shape = rotated_shape



        screen.fill((0, 0, 0))
        draw_board(screen, board)
        draw_tetromino(screen, active_tetromino)
        score_surface = font.render(f"{score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    start_game()
