# definisco le variabili costanti: dimensioni dello chermo, i font, i colori e alcuni parametri

import pygame
pygame.init()

font = pygame.font.SysFont("Calibri", 20)
font_big = pygame.font.SysFont("Calibri", 65)

######################################################  COLORS  ######################################################
white = (255, 255, 255)
black = (0, 0, 0)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

ligth_blue = (200, 250, 250)
deep_blue1 = (10, 20, 30)
deep_blue2 = (20, 30, 40)
deep_blue3 = (60, 70, 80)
gray = (100, 100, 100)
light_blue = (100, 255, 255)

ivory = (255, 255, 240)
violet = (238,130,238)
silver = (192, 192, 192)
light_gray = (245, 245, 245)

##################################################  GAME PARAMETERS  ##################################################
vertex_size = 4
point_size = 0.5

night_mode = {
    "bg_color": deep_blue1,
    "text_color": white,
    "setting_color": deep_blue2,
    "buttons_color1": deep_blue1,
    "buttons_color2": white,
    "circle_buttons_color1": violet,
    "circle_buttons_color2": red
    }

day_mode = {
    "bg_color": ivory,
    "text_color": deep_blue1,
    "setting_color": light_gray,
    "buttons_color1":  silver,
    "buttons_color2": deep_blue1,
    "circle_buttons_color1": violet,
    "circle_buttons_color2": red
    }