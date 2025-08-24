# JensTest

This repository contains a graphical Tetris clone written in Python
using the `pygame` library. Blocks are rendered in a window and the
next piece, score and level are displayed on a side panel.

## Running

Install the pygame dependency if necessary:

```bash
pip install pygame
```

Then run:

```bash
python tetris.py
```

## Controls

- Left Arrow: move piece left
- Right Arrow: move piece right
- Down Arrow: soft drop
- Up Arrow or Space: rotate piece

Lines are cleared as you complete them. Clearing multiple lines at once
awards more points and increases your level, which speeds up the
falling blocks. The game ends when new pieces can no longer enter the
board.
