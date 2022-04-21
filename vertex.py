# definition of the Vertex object

import pygame
from pygame import gfxdraw
import numpy as np

from constants import white, vertex_size

class Vertex:
    def __init__(self, x: float or int, y: float or int):
        self.x, self.y = int(x), int(y)
        self.color = white

        # offset for draging
        self.offsetX = 0
        self.offsetY = 0
    
    @property
    def pos(self):
        return np.array([self.x, self.y], int)

    @property
    def Rect(self):
        l = 10
        return pygame.Rect((self.x - l, self.y -l), (2*l, 2*l))
    
    def draw(self, Surface: pygame.Surface, size: int=vertex_size):
        
        gfxdraw.filled_circle(Surface, self.x, self.y, size, self.color)
        gfxdraw.aacircle(Surface, self.x, self.y, size, self.color)
    
    def drag(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x + self.offset_x
        self.y = mouse_y + self.offset_y