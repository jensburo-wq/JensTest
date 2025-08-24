import curses
import random
import time

WIDTH = 10
HEIGHT = 20
TICK = 0.5

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]],
}

COLORS = [curses.COLOR_CYAN, curses.COLOR_BLUE, curses.COLOR_YELLOW,
          curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_RED,
          curses.COLOR_WHITE]


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]


def check_collision(board, shape, offset):
    off_y, off_x = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if not cell:
                continue
            if x + off_x < 0 or x + off_x >= WIDTH:
                return True
            if y + off_y >= HEIGHT:
                return True
            if board[y + off_y][x + off_x]:
                return True
    return False


def merge(board, shape, offset, color):
    off_y, off_x = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + off_y][x + off_x] = color


def remove_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared = HEIGHT - len(new_board)
    while len(new_board) < HEIGHT:
        new_board.insert(0, [0 for _ in range(WIDTH)])
    return new_board, cleared


def draw_board(stdscr, board, current, offset):
    stdscr.clear()
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                stdscr.addstr(y, x * 2, '[]', curses.color_pair(cell))
    shape, color = current
    off_y, off_x = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and y + off_y >= 0:
                stdscr.addstr(y + off_y, (x + off_x) * 2, '[]', curses.color_pair(color))
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    for i, col in enumerate(COLORS, start=1):
        curses.init_pair(i, col, curses.COLOR_BLACK)

    board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    shape_key = random.choice(list(SHAPES))
    current = (SHAPES[shape_key], random.randint(1, len(COLORS)))
    offset = [0, WIDTH // 2 - len(current[0][0]) // 2]
    last_time = time.time()
    score = 0

    while True:
        now = time.time()
        if now - last_time > TICK:
            last_time = now
            if not check_collision(board, current[0], (offset[0] + 1, offset[1])):
                offset[0] += 1
            else:
                merge(board, current[0], offset, current[1])
                board, cleared = remove_lines(board)
                score += cleared
                shape_key = random.choice(list(SHAPES))
                current = (SHAPES[shape_key], random.randint(1, len(COLORS)))
                offset = [0, WIDTH // 2 - len(current[0][0]) // 2]
                if check_collision(board, current[0], offset):
                    break

        draw_board(stdscr, board, current, offset)
        stdscr.addstr(0, WIDTH * 2 + 2, f"Score: {score}")

        try:
            key = stdscr.getkey()
        except curses.error:
            key = None
        if key in ['a', 'KEY_LEFT']:
            if not check_collision(board, current[0], (offset[0], offset[1] - 1)):
                offset[1] -= 1
        elif key in ['d', 'KEY_RIGHT']:
            if not check_collision(board, current[0], (offset[0], offset[1] + 1)):
                offset[1] += 1
        elif key in ['s', 'KEY_DOWN']:
            if not check_collision(board, current[0], (offset[0] + 1, offset[1])):
                offset[0] += 1
        elif key in ['w', 'KEY_UP', ' ', 'KEY_ENTER']:
            rotated = rotate(current[0])
            if not check_collision(board, rotated, offset):
                current = (rotated, current[1])

    stdscr.nodelay(False)
    stdscr.addstr(HEIGHT // 2, WIDTH * 2 // 2 - 5, 'GAME OVER')
    stdscr.addstr(HEIGHT // 2 + 1, WIDTH * 2 // 2 - 7, f'Score: {score}')
    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    curses.wrapper(main)
