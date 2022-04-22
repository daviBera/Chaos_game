# that's the main script. Execute this script to start the app.

import random
import pygame

from interaction_objects.setting_layout import *
from constants import night_mode, day_mode , font_big, font

from interaction_objects.setting_window import SettingWindow
from interaction_objects.vertex_excluder import VertexExcluder
from chaos_game import ChaosGame
from vertex import Vertex

class Game:
    def __init__(self):
        # initialise pygame and the app window. 

        pygame.init()
        pygame.display.set_caption('Chaos Game')

        self.size = self.width, self.height = 900, 600
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

        # the following values changes when the window is resized
        self.iterations = 50000     # -> the number of iteration done by every simulation of the chaos game
        self.fast_iterations = 8000 # -> the number of iteration done when draging or changing the value of alpha
        self.frames = 1000

        self.mode = night_mode

        self.HelperButton = Button("?", pygame.Rect(self.width-l-Dy, self.height-l-Dy, l, l), self.mode["buttons_color1"], self.mode["buttons_color2"])

    def init_variables(self):
        # initialise variables and clean up the screen       
        self.refresh = True
        self.placing_vertices = True
        self.draging = False
        self.pressing = False
        self.end_animation = False

        setting_Rect = pygame.Rect(self.width-setting_width, 0, setting_width, setting_height)
        VertExc = VertexExcluder(0, pygame.Surface((setting_width, setting_width)), (0, VertExc_Y), self.mode["setting_color"])
        self.SettWind = SettingWindow(setting_Rect, VertExc, self.mode["setting_color"], self.mode["text_color"])
        
        self.ChaosG = ChaosGame([], Vertex(self.width//2, self.height//2))

        self.clean_screen()
        

    def resize(self, new_width, new_height):
        # resize window and changes the number of iterations
        self.size = self.width, self.height = new_width, new_height
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        
        self.iterations = max(int(new_width*new_height/(10*10000))*10000, self.fast_iterations)

        self.SettWind.Rect = pygame.Rect(self.width-setting_width, 0, setting_width, setting_height)
        self.HelperButton.Rect = pygame.Rect(self.width-l-Dy, self.height-l-Dy, l, l)

    def clean_screen(self):
        self.screen.fill(self.mode["bg_color"])
        self.ChaosG.points_on_screen = 0
        self.ChaosG.draw_vertices(self.screen)
        self.SettWind.show_all(self.screen, self.ChaosG)
        self.HelperButton.show(self.screen)
    
    def change_mode(self):
        if self.mode == night_mode:
            self.mode = day_mode
        else:
            self.mode = night_mode
        
        # change bottons' color
        for button in self.SettWind.buttons:
            button.color1, button.color2 = self.mode["buttons_color1"], self.mode["buttons_color2"]
        
        # 'click' the right memory button
        if self.ChaosG.memory == 1:
            Memory1.change()
        else:
            Memory2.change()

        # change the setting window's colors
        self.SettWind.bg_color, self.SettWind.text_color = self.mode["setting_color"], self.mode["text_color"]
        self.SettWind.VertExc.bg_color = self.mode["setting_color"]
        self.SettWind.VertExc.big_circle_color = self.mode["text_color"]
         
        self.HelperButton.color1, self.HelperButton.color2 = self.mode["buttons_color1"], self.mode["buttons_color2"]

    def show_commands(self):
        # shows informations about the possible keyboard interactions
        bg, text_col = self.mode["bg_color"], self.mode["text_color"]
        self.screen.fill(bg)
        text =[
        font.render("INPUT DA TASTIERA", True, text_col, bg),
        font.render("", True, text_col, bg),
        font.render("'SPACE'               ->      avviare il gioco o fare nuove iterazioni", True, text_col, bg),
        font.render("'N', 'M'               ->      dimuire e aumentare alpha", True, text_col, bg),
        font.render("'A', 'D', 'W', 'S'     ->      traslare i vertici", True, text_col, bg),
        font.render("'Q', 'E'               ->      zoomare", True, text_col, bg),
        font.render("'B'                    ->      passare da night_mode a light_mode e viceversa", True, text_col, bg)
        ]

        back = font.render("PREMI UN TASTO PER TORNARE AL GIOCO", True, text_col, bg)

        for i, line in enumerate(text):
            self.screen.blit(line, (100, 100 + i*30))

        w, h = back.get_size()
        W, H = self.screen.get_size()
        self.screen.blit(back, ((W-w)//2, H-h-50))

        pygame.display.update()
                
        while not pygame.event.peek([pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]):
            pygame.time.wait(100)
        
        pygame.event.clear()
        return

    def show_starting_quote(self):
        text = font.render("Scegli i vertici del tuo poligono e premi 'SPAZIO' per iniziare!", True, self.mode["text_color"], self.mode["bg_color"])

        w, h = text.get_size()
        W, H = self.screen.get_size()
        self.screen.blit(text, ((W-w)//2, (H-h)//2))

        pygame.display.update()


    def handle_mouse_click(self):
        mouseX, mouseY = pygame.mouse.get_pos()

        #####################   SETTING MANAGEMENT  #####################
        if self.SettWind.Rect.collidepoint(mouseX, mouseY) or self.HelperButton.click((mouseX, mouseY)):
            self.handle_VertExc_click()
            self.handle_button_click()

        #####################   VERTEX INTERACTION  #####################
        else:
            # if the click is next to a vertex is to drag it, that's managed by the ChaosG method
            self.draging = self.ChaosG.handle_vertices_click()  
            
            # if the click is not close to a vertex a new vertex is added
            if not self.draging:
                self.ChaosG.add_vertex(mouseX, mouseY)
                self.SettWind.VertExc.update_circles(self.ChaosG.num_vertices)

    def handle_button_click(self):
        settWind = self.SettWind
        chaosG = self.ChaosG

        x, y = pygame.mouse.get_pos()
        if self.HelperButton.click((x, y)):
            self.show_commands()
        
        r_pos = x-settWind.pos[0], y-settWind.pos[1]    # -> mouse coordinates relative to the setting window
        for button in settWind.buttons:
            if button.click(r_pos):
                if button == Memory2 and chaosG.memory == 1:
                    chaosG.memory = 2
                    Memory1.change()
                    Memory2.change()
                
                if button == Memory1 and chaosG.memory == 2:
                    chaosG.memory = 1
                    Memory1.change()
                    Memory2.change()
                
                else:
                    # while the mouse is kept pressed the button color stays changed
                    button.temporary_change(settWind, self.screen)
                    if button == AddVertex:
                        n = len(chaosG.vertices) + 1
                        self.ChaosG.change_vertices(n, self.width, self.height)
                        self.SettWind.VertExc.update_circles(n)

                    if button == RemoveVertex:
                        n = settWind.VertExc.n - 1
                        if n > 0:
                            self.ChaosG.change_vertices(n, self.width, self.height)
                            self.SettWind.VertExc.update_circles(n)
                    
                    if button == RandomizeVertExc and self.ChaosG.num_vertices>1:
                        num_excluded_vertices = random.randint(1, self.ChaosG.num_vertices-1)
                        self.ChaosG.excluded_vertices = random.sample(range(self.ChaosG.num_vertices), num_excluded_vertices)
                        self.SettWind.VertExc.recolor_circles(self.ChaosG.excluded_vertices)

                    if button == PresetUp:
                        if self.ChaosG.preset == None:
                            self.ChaosG.preset = 0
                        else:
                            self.ChaosG.preset = (self.ChaosG.preset+1)%self.ChaosG.num_presets
                        
                        self.ChaosG.use_preset(self.SettWind, Memory1, Memory2, self.width, self.height)
                    
                    if button == PresetDown:
                        if self.ChaosG.preset == None:
                            self.ChaosG.preset = self.ChaosG.num_presets-1
                        else:
                            self.ChaosG.preset = (self.ChaosG.preset-1)%self.ChaosG.num_presets
                        
                        self.ChaosG.use_preset(self.SettWind, Memory1, Memory2, self.width, self.height)

                    if button == SavePreset:
                        self.ChaosG.save_preset()
                        self.refresh = False
                    
                    if button == CleanScreen:
                        aux = self.ChaosG.color_mode
                        self.init_variables()
                        self.ChaosG.color_mode = aux
                        if chaosG.memory == 2:
                            # se prima avevo memory = 2 e clicco clean screen allora ChaosG.memory va a 1 e allora devo mettere giusti i  bottoni
                            Memory1.change()
                            Memory2.change()

                    if button == ColorModeUp:
                        self.ChaosG.color_mode = (self.ChaosG.color_mode + 1)%len(self.ChaosG.color_modes)
                        self.ChaosG.color_vertices()
                        self.show_color_mode()
                    
                    if button == ColorModeDown:
                        self.ChaosG.color_mode = (self.ChaosG.color_mode - 1)%len(self.ChaosG.color_modes)
                        self.ChaosG.color_vertices()
                        self.show_color_mode()

    def handle_VertExc_click(self):
        x, y = pygame.mouse.get_pos()
        sx, sy = self.SettWind.pos
        r_pos = x-sx-self.SettWind.VertExc.x, y-sy-self.SettWind.VertExc.y  # -> mouse coordinates relative to the vertex excluder

        for i, circle in enumerate(self.SettWind.VertExc.circles):
            if circle.click(r_pos):

                if i in self.ChaosG.excluded_vertices:
                    circle.change()
                    self.ChaosG.excluded_vertices.remove(i)

                elif len(self.ChaosG.excluded_vertices)<self.ChaosG.num_vertices-1:
                    circle.change()
                    self.ChaosG.excluded_vertices.append(i)
        
    def handle_draging(self, event):
        if event.type == pygame.MOUSEMOTION and not self.SettWind.Rect.collidepoint(pygame.mouse.get_pos()):
            self.ChaosG.dragged_vertex.drag()

        if event.type == pygame.MOUSEBUTTONUP and self.draging:
            self.ChaosG.dragged_vertex = None
            self.draging = False
            if not self.placing_vertices:
                self.end_animation = True

    def handle_keydown(self, event):
        keys = pygame.key.get_pressed()
                    
        # whith 'SPACE' the game starts
        if keys[pygame.K_SPACE] and self.ChaosG.num_vertices>0:
            if self.placing_vertices:
                self.placing_vertices = False
            else:
                # if 'SPACE' is pressed more times, more iterations are don
                self.ChaosG.compute_relative_vertices(self.iterations)
                self.ChaosG.play(self.screen, self.iterations, 1000, self.SettWind)
                self.refresh = False

        # whith 'I' the game is reinitialised
        elif keys[pygame.K_i]:
            self.init_variables()
            
        # whith numeric keyboard a gìregular polygon is created
        elif 1 <= event.key - 1073741912 <= 9:
            n = event.key - 1073741912
            self.ChaosG.change_vertices(n, self.width, self.height)
            self.SettWind.VertExc.update_circles(n)
        
        elif keys[pygame.K_b]:
            self.change_mode()

        else:
            self.pressing = True

    def handle_keypressed(self, event):
        keys = pygame.key.get_pressed()
        # whith 'M' and 'N' the parameter alpha i changed
        if keys[pygame.K_n]:
            self.ChaosG.alpha +=0.005
            
        if keys[pygame.K_m] and self.ChaosG.alpha>0:
            self.ChaosG.alpha -=0.005

        # translations
        elif keys[pygame.K_w]:
                self.ChaosG.move(0, -5)
            
        elif keys[pygame.K_s]:
            self.ChaosG.move(0, 5)

        elif keys[pygame.K_a]:
            self.ChaosG.move(-5, 0)
        
        elif keys[pygame.K_d]:
            self.ChaosG.move(5, 0)

        # zooms
        elif keys[pygame.K_q]:
            self.ChaosG.zoom(0.97, (self.width//2, self.height//2))

        elif keys[pygame.K_e]:
            self.ChaosG.zoom(1.03, (self.width//2, self.height//2))
        
        if event.type == pygame.KEYUP:
            if not self.placing_vertices:
                self.end_animation = True
            self.pressing = False

    def refresh_screen(self):
        self.clean_screen()
        if not self.placing_vertices:
            # if a vertex is dragged or alpha is being changed the a single frame animation with less iteration is made
            if self.draging or self.pressing:
                self.ChaosG.play(self.screen, self.fast_iterations, 1, self.SettWind)

            # when a vertex just stopped being dragged or alpha being changed an animation is made to reach maximum itarations
            elif self.end_animation:
                self.ChaosG.play(self.screen, self.fast_iterations, 1, self.SettWind)
                self.ChaosG.play(self.screen, self.iterations-self.fast_iterations, self.frames, self.SettWind)
                self.end_animation = False

            # in all the other cases the sequence of chosen vertices has to be recomputed (verteces changed, a vertex is excluded, ...)
            else:
                self.ChaosG.compute_relative_vertices(self.iterations)
                self.ChaosG.play(self.screen, self.iterations, self.frames, self.SettWind)
        
        self.refresh = False
        pygame.display.update()

    def show_color_mode(self):
        text = font_big.render(self.ChaosG.color_modes[self.ChaosG.color_mode], True, self.mode["text_color"], self.mode["bg_color"])
                
        w, h = text.get_size()
        self.screen.blit(text, (self.width//2-w//2, self.height//2-h//2))
        
        pygame.display.update()
        
        time = pygame.time.get_ticks()
        while pygame.time.get_ticks()-time<1000:
            if pygame.event.peek([pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]):
                break

    def run(self):
        '''
        The main method; the game is initialised and cycle of events starts
        '''
        self.init_variables()
        self.show_starting_quote()
        self.refresh = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    return

                if event.type == pygame.VIDEORESIZE:
                    self.refresh = True
                    self.resize(event.w, event.h)

                ###########à##########   MOUSE CLICK  #######################
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.refresh = True
                    self.handle_mouse_click()

                #########################  DRAGING  #########################
                elif self.draging:
                    self.refresh = True
                    self.handle_draging(event)

                #####################   KEYBOARD INPUT  #####################
                elif event.type == pygame.KEYDOWN:
                    self.refresh = True
                    self.handle_keydown(event)
                
                if self.pressing:
                    self.refresh = True
                    self.handle_keypressed(event)

                    
            ###############   SCREEN REFRESH ###############
            if self.refresh:
                self.refresh_screen()


if __name__ == "__main__":
    Game = Game()
    Game.run()
