# definition of SettingWindow object

import pygame

from constants import font
from interaction_objects.setting_layout import buttons, info_X, info_Y, Dy, l, VertexButtons_Y, MemoryButtons_Y, ColorMode_button_Y, Preset_button_Y
from interaction_objects.vertex_excluder import VertexExcluder

class SettingWindow:
    def __init__(self, Rect: pygame.Rect, VertExc: VertexExcluder, my_bg_color: tuple, my_text_color: tuple) -> None:
        self.Rect = Rect
        self.Surface = pygame.Surface(Rect.size)
        
        self.buttons = buttons
        self.VertExc = VertExc

        self.bg_color = my_bg_color
        self.text_color = my_text_color
    
    @property
    def pos(self) -> tuple:
        return self.Rect.topleft

    def show_info(self, dest_surface: pygame.Surface, ChaosG) -> None:
        text1 = font.render("Iterations: %d" % ChaosG.points_on_screen, True, self.text_color, self.bg_color)
        text2 = font.render("Alpha: %.3f" %ChaosG.alpha, True, self.text_color, self.bg_color)
        text3 = font.render("Vertices: %.f" %ChaosG.num_vertices, True, self.text_color, self.bg_color)
        text4 = font.render("Memory: ", True, self.text_color, self.bg_color)
        
        text5 = font.render("Color mode: ", True, self.text_color, self.bg_color)
        if ChaosG.preset == None:
            text6 = font.render("Preset: ", True, self.text_color, self.bg_color)
        else:
            text6 = font.render("Preset: %d" %(ChaosG.preset+1), True, self.text_color, self.bg_color)

        self.Surface.fill(self.bg_color, text1.get_rect().move(info_X+20, info_Y)) # per coprire le cifre scritte in precedenza da text
        self.Surface.blit(text1, (info_X, info_Y))
        self.Surface.blit(text2, (info_X, info_Y+Dy+l))
        self.Surface.blit(text3, (info_X, VertexButtons_Y))
        self.Surface.blit(text4, (info_X, MemoryButtons_Y))

        self.Surface.blit(text5, (info_X, ColorMode_button_Y))
        self.Surface.blit(text6, (info_X, Preset_button_Y))

        dest_surface.blit(self.Surface, self.pos)

    def show_VertexExcluder(self, dest_surface: pygame.Surface) -> None:
        self.VertExc.show(self.Surface)

        dest_surface.blit(self.Surface, self.pos)

    def show_buttons(self, dest_surface: pygame.Surface) -> None:
        for button in self.buttons:
            button.show(self.Surface)
        
        dest_surface.blit(self.Surface, self.pos)

    def show_all(self, dest_surface: pygame.Surface, ChaosG) -> None:

        self.Surface.fill(self.bg_color)
        
        self.show_info(dest_surface, ChaosG)
        self.show_VertexExcluder(dest_surface)
        pygame.draw.rect(self.Surface, self.text_color, self.Surface.get_rect(), 1)
        self.show_buttons(dest_surface)
        
        pygame.display.update(self.Rect)   