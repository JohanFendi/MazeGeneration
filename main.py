import pygame_widgets as pg_widgets
import pygame as pg

from maze import * 
from constants import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox



def main():
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("Press S to start algorithm, and R to reset")

    # Create two sliders for adjusting the maze's width and height, each with a corresponding text box
    height_slider = Slider(window, SLIDER_X_CORD, WINDOW_HEIGHT//4, SLIDER_LENGTH, 
                           SLIDER_THICKNESS, min=MIN_MAZE_HEIGHT, max=MAX_MAZE_HEIGHT, step=2, initial=MIN_MAZE_HEIGHT)
    width_slider = Slider(window, SLIDER_X_CORD, WINDOW_HEIGHT//2, SLIDER_LENGTH, 
                          SLIDER_THICKNESS, min=MIN_MAZE_WIDTH, max=MAX_MAZE_WIDTH, step=2, initial=MIN_MAZE_WIDTH)
    height_box = TextBox(window, BOX_X_CORD , WINDOW_HEIGHT//4 - 1.2*SLIDER_BOX_WIDTH, 
                        SLIDER_BOX_WIDTH, SLIDER_BOX_WIDTH, fontSize=FONT_SIZE)
    width_box = TextBox(window, BOX_X_CORD , WINDOW_HEIGHT//2 - 1.2*SLIDER_BOX_WIDTH, 
                        SLIDER_BOX_WIDTH, SLIDER_BOX_WIDTH, fontSize=FONT_SIZE)
    height_box.disable() # Makes boxes act only as labels, and not as input fields
    width_box.disable()

    running = True
    maze_reseted = True
    maze_width = MIN_MAZE_WIDTH
    maze_height = MAX_MAZE_HEIGHT
    while running:
        events = pg.event.get()
        for event in events:

            if event.type == pg.QUIT: 
                running = False

            if event.type == pg.KEYDOWN:  
                if event.key == pg.K_s and maze_reseted: # Starts algorithm
                    corner_x = MAX_GRAPHICAL_MAZE_WIDTH // 2 - (maze_width * CELL_WIDTH) // 2
                    corner_y = WINDOW_HEIGHT // 2 - (maze_height * CELL_WIDTH) // 2
                    maze = Maze(maze_height, maze_width, CELL_WIDTH, 30, corner_x, corner_y)
                    maze.kruskals(window)
                    maze_reseted = False
                
                if event.key == pg.K_r: # Resets the maze
                    maze_reseted = True

        
        if maze_reseted: # Draws the initial maze layout without any algorithm applied
            height_slider.value = adjust_slider(height_slider.value)
            width_slider.value = adjust_slider(width_slider.value)
            maze_width = width_slider.getValue()
            maze_height = height_slider.getValue()
            height_box.setText(height_slider.getValue())
            width_box.setText(width_slider.getValue())
                    
    
            window.fill((255, 255, 255))
            draw_maze(window, maze_width, maze_height)
            pg.draw.polygon(window, SIDE_BAR_COLOR,  # Draws sidebar
                ((MAX_GRAPHICAL_MAZE_WIDTH, 0), (MAX_GRAPHICAL_MAZE_WIDTH + SIDEBAR_WIDTH, 0),
                (MAX_GRAPHICAL_MAZE_WIDTH + SIDEBAR_WIDTH, WINDOW_HEIGHT), (MAX_GRAPHICAL_MAZE_WIDTH, WINDOW_HEIGHT)))

            pg_widgets.update(events)
            pg.display.update()


#Draws maze in a checkered pattern
def draw_maze(window, maze_width, maze_height):
    graphical_corner_x = MAX_GRAPHICAL_MAZE_WIDTH // 2 - (maze_width * CELL_WIDTH) // 2
    graphical_corner_y = WINDOW_HEIGHT // 2 - (maze_height * CELL_WIDTH) // 2

    for y in range(maze_height):
        for x in range(maze_width):
            x_cord = graphical_corner_x + x * CELL_WIDTH
            y_cord = graphical_corner_y + y * CELL_WIDTH
            color = (-1,-1,-1)

            if y % 2 == 0:  # If y is even, then alternate between path and undecided cells
                if x % 2 == 1:
                    color = MAZE_COLORS[UNDECIDED]
                else:
                    color = MAZE_COLORS[PATH]
            else: # If y is odd, then alternate between undecided and wall cells
                if x % 2 == 0:
                    color = MAZE_COLORS[UNDECIDED]
                else:
                    color = MAZE_COLORS[WALL]
        
            pg.draw.polygon(window, color, 
                            ((x_cord, y_cord),(x_cord + CELL_WIDTH, y_cord),
                             (x_cord + CELL_WIDTH, y_cord + CELL_WIDTH), (x_cord, y_cord + CELL_WIDTH)))


def adjust_slider(value): # Adjust sliders to display values following the formula 2k + 3
    return value if (value - 3) % 2 == 0 else value - 1


if __name__ == '__main__':
    pg.init()
    pg.font.init()
    main()