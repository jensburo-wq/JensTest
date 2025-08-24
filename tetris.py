"""Graphical Tetris implemented with pygame.

This version extends the original terminal based game by
rendering coloured blocks in a window, showing the upcoming
piece, and tracking score/level progression.
"""

import pygame
import random


# Grid configuration
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
SIDE_PANEL = 150

WINDOW_WIDTH = GRID_WIDTH * BLOCK_SIZE + SIDE_PANEL
WINDOW_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
FPS = 60


# Tetrimino definitions
SHAPES = {
    "I": [[1, 1, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "Z": [[1, 1, 0], [0, 1, 1]],
}


COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (255, 0, 255),  # Magenta
    (255, 0, 0),    # Red
    (255, 255, 255) # White
]


def rotate(shape):
    """Rotate a matrix clockwise."""
    return [list(row) for row in zip(*shape[::-1])]


def check_collision(board, shape, offset):
    """Return True if the shape at offset would collide."""
    off_y, off_x = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if not cell:
                continue
            if x + off_x < 0 or x + off_x >= GRID_WIDTH:
                return True
            if y + off_y >= GRID_HEIGHT:
                return True
            if y + off_y >= 0 and board[y + off_y][x + off_x]:
                return True
    return False


def merge(board, shape, offset, color):
    """Merge a falling shape into the board."""
    off_y, off_x = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and y + off_y >= 0:
                board[y + off_y][x + off_x] = color


def clear_lines(board):
    """Remove filled lines from the board."""
    new_board = [row for row in board if 0 in row]
    cleared = GRID_HEIGHT - len(new_board)
    while len(new_board) < GRID_HEIGHT:
        new_board.insert(0, [0] * GRID_WIDTH)
    return new_board, cleared


def new_piece():
    key = random.choice(list(SHAPES))
    shape = SHAPES[key]
    color = random.randint(1, len(COLORS))
    return shape, color


def draw_board(screen, board, current, offset, next_piece, score, level):
    screen.fill((0, 0, 0))

    # Draw placed blocks and grid
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if cell:
                pygame.draw.rect(screen, COLORS[cell - 1], rect)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)

    # Draw current piece
    shape, color = current
    off_y, off_x = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and y + off_y >= 0:
                rect = pygame.Rect(
                    (x + off_x) * BLOCK_SIZE,
                    (y + off_y) * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
                pygame.draw.rect(screen, COLORS[color - 1], rect)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)

    # Side panel information
    font = pygame.font.SysFont("Arial", 24)
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)),
                (GRID_WIDTH * BLOCK_SIZE + 10, 20))
    screen.blit(font.render(f"Level: {level}", True, (255, 255, 255)),
                (GRID_WIDTH * BLOCK_SIZE + 10, 50))
    screen.blit(font.render("Next:", True, (255, 255, 255)),
                (GRID_WIDTH * BLOCK_SIZE + 10, 90))

    next_shape, next_color = next_piece
    for y, row in enumerate(next_shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    GRID_WIDTH * BLOCK_SIZE + 10 + x * BLOCK_SIZE // 2,
                    120 + y * BLOCK_SIZE // 2,
                    BLOCK_SIZE // 2,
                    BLOCK_SIZE // 2,
                )
                pygame.draw.rect(screen, COLORS[next_color - 1], rect)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)

    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current = new_piece()
    next_piece = new_piece()
    offset = [0, GRID_WIDTH // 2 - len(current[0][0]) // 2]
    score = 0
    lines = 0
    level = 1
    drop_time = 500  # milliseconds
    last_drop = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(board, current[0], (offset[0], offset[1] - 1)):
                        offset[1] -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(board, current[0], (offset[0], offset[1] + 1)):
                        offset[1] += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(board, current[0], (offset[0] + 1, offset[1])):
                        offset[0] += 1
                elif event.key in (pygame.K_UP, pygame.K_SPACE):
                    rotated = rotate(current[0])
                    if not check_collision(board, rotated, offset):
                        current = (rotated, current[1])

        if now - last_drop > drop_time:
            last_drop = now
            if not check_collision(board, current[0], (offset[0] + 1, offset[1])):
                offset[0] += 1
            else:
                merge(board, current[0], offset, current[1])
                board, cleared = clear_lines(board)
                if cleared:
                    lines += cleared
                    score += (cleared ** 2) * 100
                    level = lines // 10 + 1
                    drop_time = max(100, 500 - (level - 1) * 50)
                current = next_piece
                next_piece = new_piece()
                offset = [0, GRID_WIDTH // 2 - len(current[0][0]) // 2]
                if check_collision(board, current[0], offset):
                    running = False

        draw_board(screen, board, current, offset, next_piece, score, level)

    # Game over screen
    font = pygame.font.SysFont("Arial", 48)
    screen.blit(font.render("Game Over", True, (255, 255, 255)),
                (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 40))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                waiting = False
        clock.tick(15)

    pygame.quit()


if __name__ == "__main__":
    main()

