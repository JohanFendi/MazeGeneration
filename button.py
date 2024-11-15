import pygame as pg
from constants import *

class Button:
    def __init__(self, corner_x, corner_y, width, height, color1, text):
        self.corner_x = corner_x
        self.corner_y = corner_y
        self.width = width
        self.height = height
        self.color1 = color1
        self.text = text
        
    
    def draw(self, window):
        pg.draw.polygon(window, self.color1, ((self.corner_x , self.corner_y),
                                              (self.corner_x + self.width, self.corner_y), 
                                              (self.corner_x + self.width, self.corner_y + self.height), 
                                              (self.corner_x, self.corner_y + self.height)))
        text = FONT.render(self.text, True, BUTTON_TEXT_COLOR)
        center_x = self.corner_x + self.width // 2
        center_y = self.corner_y + self.height // 2
        word_width = FONT_SIZE * len(self.text) // 3
        window.blit(text, (center_x - word_width, center_y - FONT_SIZE // 2))
    
    #Checks if mouse button is inside the box and pressed down
    def is_pressed(self, event):
        mouse_x_cord, mouse_y_cord = pg.mouse.get_pos()
        in_button_horisontally = self.corner_x <= mouse_x_cord <= self.corner_x + self.width
        in_button_vertically = self.corner_y <= mouse_y_cord <= self.corner_y + self.height
        mouse_pressed = event.type == pg.MOUSEBUTTONDOWN
        return in_button_horisontally and in_button_vertically and mouse_pressed

        

       
    