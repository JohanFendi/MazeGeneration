import pygame_widgets
import pygame 
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


pygame.init()

SIDEBAR_WIDTH = 400
WINDOW_WIDTH = 1240 
MAX_MAZE_GRAPHICS_WIDTH = WINDOW_WIDTH - SIDEBAR_WIDTH
WINDOW_HEIGHT = 630
FPS = 10

x_cord = 200
y_cord = 200
length = 200
thickness = 20
min_width = 3
max_width = 99
min_height = 3
max_height = 99

window_width =1000
window_height = 500
box_side = 50
box_middle_x = x_cord + length // 2 - box_side // 2
box_y = y_cord - box_side*2 
spacing = 200

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))



def get_user_input(x_cord, y_cord, length, thickness, min_width, max_width, window, min_height, max_height, spacing):
    height_slider = Slider(window, x_cord, y_cord, length, thickness, min=min_height, max=max_height, step=2)
    width_slider = Slider(window, x_cord, y_cord+spacing, length, thickness, min=min_width, max=max_width, step=2)
    height_label = TextBox(window, box_middle_x ,box_y, box_side, box_side, fontSize=30)
    width_label = TextBox(window, box_middle_x ,box_y + spacing, box_side, box_side, fontSize=30)
    height_label.disable()  # Act as label instead of textbox
    width_label.disable()

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_s:
                    return height_slider.getValue(), width_slider.getValue()
            
        window.fill((255, 255, 255))

        height_label.setText(height_slider.getValue())
        width_label.setText(width_slider.getValue())
        pygame_widgets.update(events)

        pygame.display.update()

height, width = get_user_input(x_cord, y_cord, length, thickness, min_width, max_width, WINDOW, min_height, max_height, spacing)
print(height, width)
