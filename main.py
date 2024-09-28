import pygame as pg
import sys

from algorithms import *

MAX_WINDOW_WIDTH = 1240
MAX_WINDOW_HEIGHT = 630
FPS = 10


def get_user_input():
    cell_width = int(input('Enter cell width: '))
    max_maze_height = int(((MAX_WINDOW_HEIGHT / cell_width) - 3)/2)
    max_maze_width = int(((MAX_WINDOW_WIDTH / cell_width) - 3)/2)
    maze_width = 2*int(input(f'Enter maze_width between 0 and {max_maze_width}: ')) + 3
    maze_height = 2*int(input(f'Enter maze height between 0 and {max_maze_height}: ')) + 3
    max_edge_weight = int(input('Enter max edge weight:'))
    window_height = cell_width * maze_height
    window_width = cell_width * maze_width
    assert window_width <= MAX_WINDOW_WIDTH, 'WindowWidthError: Window to wide, chose smaller maze width.'
    assert window_height <= MAX_WINDOW_HEIGHT, 'WindowHeightError: Window to tall, chose smaller maze height.'
    assert window_width > 0, 'WindowWidthError: Window to small, chose larger maze width.'
    assert window_height > 0, 'WindowHeightError: Window to small, chose larger maze height.'
    return cell_width, maze_height, maze_width, window_height, window_width, max_edge_weight


def update_screen(maze, window):
    maze.draw(window)
    pg.display.flip()

def check_user_quit(running):
    for event in pg.event.get():
        if event.type in [pg.QUIT] :
            running = False

    return running

def main(fps):
    pg.init()
    CELL_WIDTH, MAZE_HEIGHT, MAZE_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH, MAX_EDGE_WEIGHT = get_user_input()
    WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    maze = Maze(MAZE_HEIGHT, MAZE_WIDTH, CELL_WIDTH, CELL_WIDTH, MAX_EDGE_WEIGHT, WINDOW, FPS)
    running = True
    clock = pg.time.Clock()
    while running:
        running = check_user_quit(running)
        update_screen(maze, WINDOW)
        clock.tick(fps)
    sys.exit()

if __name__ == '__main__':
    main(FPS)