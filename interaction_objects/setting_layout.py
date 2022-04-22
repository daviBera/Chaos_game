# definion of the variables that define the layout of the setting window
# button istances declaration
import pygame

from constants import night_mode 

from interaction_objects.buttons import Button

#############################################   LAYOUT VARIABLES #############################################

setting_width, setting_height = 200, 405

l = 22 #button height
Dy = 5

info_X, info_Y = 5,  10
VertexButtons_X, VertexButtons_Y = setting_width//2+l,  info_Y + 2*(l+Dy)
MemoryButtons_X, MemoryButtons_Y = VertexButtons_X,  info_Y + 3*(l+Dy)

VertExc_Y = MemoryButtons_Y + l + Dy

ColorMode_button_X, ColorMode_button_Y = VertexButtons_X, VertExc_Y + setting_width 
Preset_button_X, Preset_button_Y =  VertexButtons_X-l//2, ColorMode_button_Y + l + Dy

#############################################   SETTING'S BUTTONS ISTANCES #############################################

c1, c2 = night_mode["buttons_color1"], night_mode["buttons_color2"]

AddVertex = Button("+", pygame.Rect(VertexButtons_X, VertexButtons_Y, l, l), c1, c2,)
RemoveVertex = Button("-", pygame.Rect(VertexButtons_X+l, VertexButtons_Y, l, l), c1, c2)

Memory1 = Button("1", pygame.Rect(MemoryButtons_X, MemoryButtons_Y, l, l), c2, c1)
Memory2 = Button("2", pygame.Rect(MemoryButtons_X+l, MemoryButtons_Y, l, l), c1, c2)

RandomizeVertExc = Button("RANDOM", pygame.Rect(setting_width//2-45, VertExc_Y+setting_width//2-l//2, 90, l), c1, c2)

ColorModeDown = Button("<", pygame.Rect(ColorMode_button_X, ColorMode_button_Y, l, l), c1, c2)
ColorModeUp = Button(">", pygame.Rect(ColorMode_button_X+l, ColorMode_button_Y, l, l), c1, c2)

PresetDown = Button("<", pygame.Rect(Preset_button_X,Preset_button_Y, l, l), c1, c2)
SavePreset = Button("S", pygame.Rect(Preset_button_X+l, Preset_button_Y, l, l), c1, c2)
PresetUp = Button(">", pygame.Rect(Preset_button_X+2*l, Preset_button_Y, l, l), c1, c2)

CleanScreen = Button("CLEAN SCREEN", pygame.Rect(setting_width//2-70, Preset_button_Y+l+2*Dy, 140, l), c1, c2)

buttons = [AddVertex, RemoveVertex, Memory1, Memory2, CleanScreen, RandomizeVertExc, PresetUp, PresetDown, SavePreset, ColorModeDown, ColorModeUp]