import pygame as pg
import random
import time
import sys

def update_window_during_kruskals(clock, maze, window, fps):
    clock.tick(fps)
    maze.draw(window)
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

def kruskals(maze, window, fps):
    clock = pg.time.Clock()
    for weight, cell1, edge_cell, cell2 in maze.edges:

        edge_cell.object_type = 'edge_being_considered'
        cell1.object_type = 'connection_being_considered'
        cell2.object_type = 'connection_being_considered'
        update_window_during_kruskals(clock, maze, window, fps)

        if maze.disjointed_set.union(cell1, cell2):
            edge_cell.convert_to_path()
        else:
            edge_cell.convert_to_wall()
        
        cell1.object_type = 'path'
        cell2.object_type = 'path'
        
        update_window_during_kruskals(clock, maze, window, fps)
        
        
class Cell:
    colors = {'wall':(0,0,0), 'undecided':(0,150,150), 'path':(255,255,255), 
              'edge_being_considered': (150,0,0),'connection_being_considered': (0,150,0)}

    def __init__(self, object_type, x_cord, y_cord):
        self.object_type = object_type
        self.x_cord = x_cord
        self.y_cord = y_cord
    
    def convert_to_wall(self):
        self.object_type = 'wall'

    def convert_to_path(self):
        self.object_type = 'path'


class Maze:
    def __init__(self, maze_height, maze_width, cell_width, cell_height, max_edge_weight, window, fps):
        self.max_edge_weight = max_edge_weight
        self.width = maze_width
        self.height = maze_height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.grid = [[Cell('undecided', x, y) for x in range(self.width)] for y in range(self.height)]
        self.place_out_walls()
        self.place_out_paths()
        self.edges = self.create_edges()
        self.disjointed_set = self.create_disjointed_set()
        kruskals(self, window, fps)

    def draw(self, window):
        for y in range(self.height):
            for x in range(self.width):
                start_x, start_y = x * self.cell_width, y * self.cell_height
                end_x, end_y = start_x + self.cell_width, start_y + self.cell_height
                pg.draw.polygon(window, Cell.colors[self.grid[y][x].object_type],
                ((start_x, start_y), (end_x, start_y), (end_x, end_y), (start_x, end_y)))

    def place_out_walls(self):
        for y in range(1, self.height-1, 2):
            for x in range(1, self.width-1, 2):
                self.grid[y][x].convert_to_wall()
    
    def place_out_paths(self):
        for y in range(0, self.height, 2):
            for x in range(0, self.width, 2):
                self.grid[y][x].convert_to_path()
    
    def create_edges(self):
        #[node1, node2, edge_cell]
        edges = []
        for node1_ypos in range(0, self.height, 2):
            for node1_xpos in range(0, self.width, 2):
                if node1_xpos < self.width-1:
                    horisontal_edge = [random.randint(1, self.max_edge_weight),self.grid[node1_ypos][node1_xpos],
                                        self.grid[node1_ypos][node1_xpos+1], self.grid[node1_ypos][node1_xpos+2]]
                    edges.append(horisontal_edge)
                if node1_ypos < self.height-1:
                    vertical_edge = [random.randint(1, self.max_edge_weight),self.grid[node1_ypos][node1_xpos],
                                        self.grid[node1_ypos+1][node1_xpos], self.grid[node1_ypos+2][node1_xpos]]
                    edges.append(vertical_edge)
        edges.sort(key=lambda edge:edge[0])
        return edges

    def create_disjointed_set(self):
        disjointed_set = Disjointed_set()
        for row in self.grid:
            for cell in row:
                disjointed_set.parent[cell] = cell
                disjointed_set.rank[cell] = 0
        return disjointed_set

class Disjointed_set:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def union(self, cell1, cell2):
        parent1 = self.find(cell1)
        parent2 = self.find(cell2)
        if parent1 == parent2:
            return False
        if self.rank[parent1] == self.rank[parent2]:
            self.rank[parent1] += 1
            self.parent[parent2] = parent1
        elif self.rank[parent1] > self.rank[parent2]:
            self.parent[parent2] = parent1
        else:
            self.parent[parent1] = parent2
        return True

    def find(self, cell):
        if self.parent[cell] == cell:
            return cell
    
        self.parent[cell] = self.find(self.parent[cell])
        return self.parent[cell]


        
           