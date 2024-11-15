import pygame_widgets as pg_widgets
import pygame as pg

from button import *
from maze import * 
from constants import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox



def main():
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pg.time.Clock()

    # Create two sliders for adjusting the maze's width and height, each with a corresponding text box
    height_slider = Slider(window, SLIDER_X_CORD, WINDOW_HEIGHT//4, SLIDER_LENGTH, SLIDER_THICKNESS, 
                           min=MIN_MAZE_HEIGHT, max=MAX_MAZE_HEIGHT, step=2, initial=MIN_MAZE_HEIGHT)
    width_slider = Slider(window, SLIDER_X_CORD, WINDOW_HEIGHT//2, SLIDER_LENGTH, SLIDER_THICKNESS, 
                          min=MIN_MAZE_WIDTH, max=MAX_MAZE_WIDTH, step=2, initial=MIN_MAZE_WIDTH)
    
    height_box = TextBox(window, BOX_X_CORD , WINDOW_HEIGHT//4 - 1.2*SLIDER_BOX_WIDTH, 
                        SLIDER_BOX_WIDTH, SLIDER_BOX_WIDTH, fontSize=FONT_SIZE)
    width_box = TextBox(window, BOX_X_CORD , WINDOW_HEIGHT//2 - 1.2*SLIDER_BOX_WIDTH, 
                        SLIDER_BOX_WIDTH, SLIDER_BOX_WIDTH, fontSize=FONT_SIZE)
    
    height_box.disable() # Makes boxes act only as labels, and not as input fields
    width_box.disable()

    start_button = Button(START_BUTTON_X_CORD, START_BUTTON_Y_CORD, START_BUTTON_WIDTH, 
                          BUTTON_HEIGHT, START_BUTTON_COLOR, START_BUTTON_TEXT)
    
    reset_button = Button(RESET_BUTTON_X_CORD, RESET_BUTTON_Y_CORD, RESET_BUTTON_WIDTH, 
                          BUTTON_HEIGHT, RESET_BUTTON_COLOR, RESET_BUTTON_TEXT)

    maze_width = MIN_MAZE_WIDTH
    maze_height = MIN_MAZE_HEIGHT
    maze = None
    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if start_button.is_pressed(event):
                maze = Maze(maze_height, maze_width)
                
            if reset_button.is_pressed(event):
                maze = None

            if event.type == pg.QUIT: 
                running = False

        if maze is None: # Draws the maze is the algorithm is not started
            height_slider.value = adjust_slider(height_slider.value)
            width_slider.value = adjust_slider(width_slider.value)
            maze_width = width_slider.getValue()
            maze_height = height_slider.getValue()
            height_box.setText(height_slider.getValue())
            width_box.setText(width_slider.getValue())
                    
            window.fill(BACKGROUND_COLOR)
            draw_maze(window, maze_width, maze_height)
            pg.draw.polygon(window, SIDEBAR_COLOR,  # Draws sidebar
                ((MAX_GRAPHICAL_MAZE_WIDTH, 0), (MAX_GRAPHICAL_MAZE_WIDTH + SIDEBAR_WIDTH, 0),
                (MAX_GRAPHICAL_MAZE_WIDTH + SIDEBAR_WIDTH, WINDOW_HEIGHT), (MAX_GRAPHICAL_MAZE_WIDTH, WINDOW_HEIGHT)))
            
            start_button.draw(window)
            reset_button.draw(window)
            pg_widgets.update(events)

        elif len(maze.edges) > 0: #Executes one iteration of kruskals algorithm
            maze.kruskals_step(window, clock)
            maze.draw(window)

        pg.display.update()


#Draws maze in a checkered pattern
#Does not create the actual maze
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
    main()