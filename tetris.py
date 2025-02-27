import pygame

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    board = create_board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

ROWS = 20
COLS = 10

TETROMINOS = {
    'I': [
        [1, 1, 1, 1]
    ],
    'O': [
        [1, 1],
        [1, 1]
    ],
    'T': [
        [0, 1, 0],
        [1, 1, 1]
    ],
    'S': [
        [0, 1, 1],
        [1, 1, 0]
    ],
    'Z': [
        [1, 1, 0],
        [0, 1, 1]
    ],
    'J': [
        [1, 0, 0],
        [1, 1, 1]
    ],
    'L': [
        [0, 0, 1],
        [1, 1, 1]
    ]
}

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def is_valid_position(board, shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board_x = offset_x + x
                board_y = offset_y + y
                # Prüfe Spielfeldgrenzen
                if board_x < 0 or board_x >= COLS or board_y >= ROWS:
                    return False
                # Falls board_y negativ ist (Tetromino erscheint oberhalb des sichtbaren Bereichs), überspringen
                if board_y >= 0 and board[board_y][board_x]:
                    return False
    return True

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

if __name__ == '__main__':
    start_game()
