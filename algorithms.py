import pygame as pg
import sys

def animate_kruskals(clock, maze, window, fps):
    clock.tick(fps)
    maze.draw(window)
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            pg.quit()
            sys.exit()

def kruskals(maze, window, fps):
    clock = pg.time.Clock()
    for _ , cell1, edge_cell, cell2 in maze.edges:

        edge_cell.object_type = 'edge_being_considered'
        cell1.object_type = 'connection_being_considered'
        cell2.object_type = 'connection_being_considered'
        animate_kruskals(clock, maze, window, fps)

        if maze.disjointed_set.union(cell1, cell2):
            edge_cell.convert_to_path()
        else:
            edge_cell.convert_to_wall()
        
        cell1.object_type = 'path'
        cell2.object_type = 'path'
        
        animate_kruskals(clock, maze, window, fps)
        
        

        
           