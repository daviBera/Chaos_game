# the VertexExcluder object allows to decide wich vertices esclude in as explained in the README.txt
import pygame
from math import cos, sin, pi

from constants import night_mode
from interaction_objects.buttons import CircleButton

class VertexExcluder:
    def __init__(self, n: int, Surface: pygame.Surface, pos, bg_color) -> None:
        self.n = n

        self.Surface = Surface
        self.W, self.H = Surface.get_size()
        self.pos = self.x, self.y = pos

        self.side = min(self.W, self.H)
        self.Radius = int(0.7*self.side//2)
        self.radius = int(0.09*self.side//2)

        self.bg_color = bg_color
        self.big_circle_color = night_mode["text_color"]

        self.circle_buttons_color1 = night_mode["circle_buttons_color1"]
        self.circle_buttons_color2 = night_mode["circle_buttons_color2"]

        self.update_circles(n)

    def update_circles(self, n: int) -> None:
        circles = []
        self.n = n

        if self.n>1:
            delta_angle = 360/self.n
            for i in range(self.n):
                t = (90+i*delta_angle) * pi / 180
                x = cos(t)*self.Radius + self.W/2
                y = - sin(t)*self.Radius + self.H/2

                circles.append(CircleButton(self.radius, int(x), int(y), self.circle_buttons_color1, self.circle_buttons_color2))
                
        self.circles = circles

    def recolor_circles(self, list) -> None:
        for circle in self.circles:
            circle.color1, circle.color2 = self.circle_buttons_color1, self.circle_buttons_color2
        for i in list:
            self.circles[i].change()

    def show(self, dest_surface: pygame.Surface) -> None:

        #x, y sono la posizione relativa a setting_Surface
        self.Surface.fill(self.bg_color)
        pygame.gfxdraw.aacircle(self.Surface, self.W//2, self.H//2, self.Radius, self.big_circle_color)

        if self.circles != []:
            pygame.gfxdraw.aacircle(self.Surface, self.circles[0].x, self.circles[0].y, self.circles[0].radius + 2, self.circles[0].color1)

        for circle in self.circles:
            circle.show(self.Surface)
        
        dest_surface.blit(self.Surface, self.pos)