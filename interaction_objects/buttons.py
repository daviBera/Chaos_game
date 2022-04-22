# costruisco i bottoni 

import string
import pygame

from constants import font


class Button:
 
    def __init__(self, text: string, Rect: pygame.Rect, color1, color2, border_width: int=1) -> None:
        self.Rect = Rect
        self.border_width = border_width

        self.text = text
        self.color1 = color1
        self.color2 = color2
    
    def show(self, Surface: pygame.Surface) -> None:
        self.rtext = font.render(self.text, True, self.color2, self.color1)
        
        pygame.draw.rect(Surface, self.color1, self.Rect)
        pygame.draw.rect(Surface, self.color2, self.Rect, self.border_width)
        W, H = self.Rect.size
        w, h = self.rtext.get_size()
        Surface.blit(self.rtext, self.Rect.move((W-w)//2, (H-h)//2))
    
    def click(self, r_mouse_pos) -> bool:
        return self.Rect.collidepoint(r_mouse_pos)

    def change(self) -> None:
        self.color1, self.color2 = self.color2, self.color1 

    def temporary_change(self, settWind, dest_surface: pygame.Surface) -> None:
        # fa un change temporaneo fino a che il non smetto di tenere cliccato col mouse
        self.change()
        settWind.show_buttons(dest_surface)        
        pygame.display.update(settWind.Rect)

        while True:
            pygame.time.wait(10)
            if pygame.event.peek(pygame.MOUSEBUTTONUP):
                break
        self.change()

        settWind.show_buttons(dest_surface)        
        pygame.display.update(settWind.Rect)


class CircleButton:
    def __init__(self, radius: int, centerX: int, centerY: int, color1, color2) -> None:
        self.radius = radius
        self.x, self.y = centerX, centerY
        self.color1 = color1
        self.color2 = color2

        # ogni volta che  
        r = radius
        self.Rect = pygame.Rect(self.x - r , self.y - r, 2*r, 2*r)

    def show(self, Surface: pygame.Surface):
        pygame.gfxdraw.filled_circle(Surface, self.x, self.y, self.radius, self.color1)
        pygame.gfxdraw.aacircle(Surface, self.x, self.y, self.radius, self.color1)
        self.Surface = Surface
    
    def click(self, r_mouse_pos) -> bool:
        return self.Rect.collidepoint(r_mouse_pos)
    
    def change(self) -> None:
        self.color1, self.color2 = self.color2, self.color1