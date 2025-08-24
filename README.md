# JensTest

This repository contains a simple terminal-based Tetris game written in Python using the `curses` module.

## Running

Ensure you are in a terminal that supports `curses` and run:

```bash
python tetris.py
```

## Controls

- `a` or Left Arrow: move left
- `d` or Right Arrow: move right
- `s` or Down Arrow: move down
- `w`, Up Arrow, Space, or Enter: rotate piece

Lines are cleared as you complete them and the score is displayed on the right. The game ends when new pieces can no longer enter the board.
