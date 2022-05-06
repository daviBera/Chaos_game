# The ChaosGame object. Its characterised by the vertices, exluded vertices, alpha and other parameters.
# The most important method is play() that makes the animation of the chaos game's simulation

import pygame
import numpy as np
from colorsys import hsv_to_rgb

from constants import *
from helpers import init_polygon, random_rgb

from vertex import Vertex


class ChaosGame:
    def __init__(self, vertices: list, starting_point: Vertex, point_size=point_size, color_mode = 0) -> None:
        self.vertices = vertices
        self.starting_point = starting_point
        
        self.excluded_vertices = []
        
        self.point_size = point_size
        
        self.color_mode = color_mode
        self.color_modes = ['HSV COLORS', 'RED COLORS', 'GREEN COLORS', 'BLUE COLORS', 'RANDOM COLORS', 'WHITE COLOR', 'BLACK COLOR']
        self.starting_point.color = gray
        self.color_vertices()
        
        self.points_on_screen = 0
        self.dragged_vertex = None

        self.alpha = 0.5
        self.memory = 1

        self.preset = None
        f = open("presets.txt", "r")
        self.num_presets = len(f.readlines())
        f.close()
    
    @property
    def num_vertices(self):
        return len(self.vertices)

    def add_vertex(self, x, y) -> None:
        self.vertices.append(Vertex(x, y))
        self.excluded_vertices = []
        self.color_vertices()

    def change_vertices(self, n: int, width: int, height: int) -> None:
        self.vertices = init_polygon(n, 0, 0, width, height, 50)
        self.excluded_vertices = []
        self.color_vertices()

    def move(self, dx: int, dy: int) -> None:
        for vertex in self.vertices:
            vertex.x += dx
            vertex.y += dy

    def zoom(self, k, center) -> None:
        centerX, centerY = center
        for vertex in self.vertices:
            vertex.x = centerX + round((vertex.x-centerX)*k)
            vertex.y = centerY + round((vertex.y-centerY)*k)

    def handle_vertices_click(self) -> None:
        '''
        If the click is next to a vertex, this is assigned to self.dragged_vertex and True is returned.
        Else returns False.
        '''
        mouseX, mouseY = pygame.mouse.get_pos()
        for vertex in self.vertices + [self.starting_point]:
            if vertex.Rect.collidepoint(mouseX, mouseY):
                self.dragged_vertex = vertex
                vertex.offset_x = vertex.x - mouseX
                vertex.offset_y = vertex.y - mouseY
                return True
        return False

    def color_vertices(self) -> None:
        '''
        By defaul verteces are white, with this method their color is changed.
        '''
        color_mode = self.color_modes[self.color_mode]
        for i, vertex in enumerate(self.vertices):
            if color_mode == 'WHITE COLOR':
                vertex.color = white
            
            if color_mode == 'BLACK COLOR':
                vertex.color = black

            if color_mode == 'RANDOM COLORS':
                vertex.color = random_rgb()
            
            if color_mode == 'HSV COLORS':
                vertex.color = [int(255*c) for c in hsv_to_rgb(i/len(self.vertices), 0.8, 1)]

            if color_mode == "RED COLORS":
                vertex.color = [int(255*c) for c in hsv_to_rgb(0.33*i/len(self.vertices), 0.8, 1)]
            
            if color_mode == "GREEN COLORS":
                vertex.color = [int(255*c) for c in hsv_to_rgb(0.33 +0.33*i/len(self.vertices), 0.8, 1)]
            
            if color_mode == "BLUE COLORS":
                vertex.color = [int(255*c) for c in hsv_to_rgb(0.66 +0.33*i/len(self.vertices), 0.8, 1)]

    def draw_vertices(self, Surface, draw_starting_point=True):
        for vertex in self.vertices:
            vertex.draw(Surface)
        
        if draw_starting_point:
            self.starting_point.draw(Surface, size=vertex_size-1)      

    def use_preset(self, SettWind, Memory1, Memory2, width, height):
        # presets are saved in presets.txt with "/ " as separator:
        # num_vertices/ alpha/ memory/ color_mode/ excluded_vertices

        f = open("presets.txt", "r")
        presets = f.readlines()
        f.close()

        my_preset = presets[self.preset].rsplit("/ ")
        
        # show mwmory button with the correct colors
        if int(my_preset[2])== 2 and self.memory == 1:
            Memory1.change()
            Memory2.change()
        
        if int(my_preset[2])==1 and self.memory == 2:
            Memory1.change()
            Memory2.change()

        # change the parameters
        self.change_vertices(int(my_preset[0]), width, height)
        self.alpha = float(my_preset[1])
        self.memory = int(my_preset[2])
        self.color_mode = int(my_preset[3])
        if my_preset[4] == '\n' or my_preset[4] == '':
            self.excluded_vertices = []
        else:
            self.excluded_vertices = [int(vertex) for vertex in my_preset[4].rsplit(", ")]

        SettWind.VertExc.update_circles(int(my_preset[0]))
        SettWind.VertExc.recolor_circles(self.excluded_vertices)

    def save_preset(self):
        if self.num_vertices<3:
            return
            
        f = open("presets.txt", "a")

        excluded_vertices = ", ".join([str(vertex) for vertex in  self.excluded_vertices])
        
        f.write('\n')
        f.write(f"{self.num_vertices}/ {self.alpha}/ {self.memory}/ {self.color_mode}/ " + excluded_vertices)
        f.close()

    def compute_relative_vertices(self, iter: int, use_seed: bool=False) -> None:
        '''
        An array with the sequence of chosen verteces is created (self.relative_verteces).
        '''
        if use_seed:
            np.random.seed(1)

        # if no verteces are excluded
        if self.excluded_vertices == []:
            self.relative_vertices = np.random.randint(self.num_vertices, size=iter+1)

        else:
            self.relative_vertices = np.empty(iter+1, int)
            chosable = np.setdiff1d(np.arange(self.num_vertices), self.excluded_vertices)

            if self.memory==1:
                self.relative_vertices[1] = 0
                for i in range(1, iter):
                    self.relative_vertices[i+1] = np.random.choice(np.remainder(self.relative_vertices[i] + chosable, self.num_vertices))
            
            else:
                self.relative_vertices[1], self.relative_vertices[2] = 0, 0
                i = 2
                while i<iter:
                    potential_vertex = np.random.randint(self.num_vertices)
                    if not (self.relative_vertices[i]==self.relative_vertices[i-1] and potential_vertex in np.remainder(self.relative_vertices[i] + self.excluded_vertices, self.num_vertices)):                       
                        self.relative_vertices[i+1] = potential_vertex
                        i +=1
                
                for i in range(2, iter):
                    if self.relative_vertices[i]==self.relative_vertices[i-1]:
                        self.relative_vertices[i+1] = np.random.choice(np.remainder(self.relative_vertices[i] + chosable, self.num_vertices))
                    else:
                        self.relative_vertices[i+1] = np.random.randint(0, self.num_vertices)

    def use_sequence(self, iter: int):
        with open("sequence.txt", "r") as tf:
            periodic = np.array(tf.read().split(','), int)
        
        self.relative_vertices = np.tile(periodic, iter//periodic.size+1)




    def play(self, Surface: pygame.Surface, iter: int, frames: int, SettWindow) -> None:

        if self.vertices == []:
            return
            
        points = np.empty((iter+1, 2), int)
        # points[]

        points[0] = self.starting_point.pos
        vertices = np.array([vertex.pos for vertex in self.vertices])
        colors = np.array([vertex.color for vertex in self.vertices])

        # points[i+1] è il punto medio (la distanza alpha) tra points[i] e self.relative_vertices[i+1]
        for i in range (iter):
            points[i+1] = self.alpha*vertices[self.relative_vertices[i+1]] + (1-self.alpha)*points[i]
        
        # the animation is done in a number of frames equal to frames
        points_per_refresh = max(iter//frames, 1)

        for i, point in enumerate(points[1:]):
            if self.point_size<1:
                #screen.set_at(point, self.vertices[self.relative_vertices[i]].color)
                pygame.gfxdraw.pixel(Surface, point[0], point[1], colors[self.relative_vertices[i+1]])

            else:
                pygame.draw.circle(Surface, colors[self.relative_vertices[i+1]], point, self.point_size)

            if i%points_per_refresh == 0:
                self.points_on_screen += points_per_refresh
                SettWindow.show_info(Surface, self)

                # animation of the vertices
                pygame.draw.circle(Surface, violet, vertices[self.relative_vertices[i+1]], vertex_size+1)
                pygame.display.update()
                pygame.draw.circle(Surface, Surface.get_at((3, 3)), vertices[self.relative_vertices[i+1]], vertex_size+1)
                self.vertices[self.relative_vertices[i+1]].draw(Surface)

                if pygame.event.peek([pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]):
                    return

        SettWindow.show_info(Surface, self)
        pygame.display.update()