import pygame
import sys

from pygame.constants import K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_a, K_b, K_c, K_d, K_h, K_l, K_o, K_q, K_i, K_r, K_x, K_z
from constants import *
from draw import *

class AppWindow:
    insert_mode = False
    delete_mode = False
    animation_mode = False
    interpolator = None
    grabbed_idx = None
    animation_loop = False

    def __init__(self) -> None:
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.world = World(COMMANDS_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, CLOSENESS_PX)
        # attributes
        pygame.display.set_caption("Interactive Spline Editor")
        pygame.font.init()
        self.window.fill(WINDOW_BACKGROUND)
        
        
        pygame.display.flip() # display the window
        self.run()

    def event_handler(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_q:
                sys.exit()
            if event.key == K_i:
                self.insert_mode = not self.insert_mode
                self.delete_mode = False
                self.animation_mode = False
                self.animation_loop = False
            if event.key == K_x:
                self.delete_mode = not self.delete_mode
                self.insert_mode = False
                self.animation_mode = False
                self.animation_loop = False
            if event.key == K_d:
                self.world.clear_control_points()
                self.interpolator = None
                self.insert_mode = False
                self.delete_mode = False
                self.animation_mode = False
                self.animation_loop = False
                self.world.object_pos = [-1, -1]
                self.world.t = 0
                self.world.dt = 1
            if event.key == K_ESCAPE:
                self.insert_mode = False
                self.delete_mode = False
                self.animation_mode = False
            if event.key == K_l:
                if not self.animation_mode: # no change during animation
                    self.interpolator = 'linear'
            if event.key == K_z:
                if not self.animation_mode:
                    self.interpolator = 'bezier'
            if event.key == K_b:
                if not self.animation_mode:
                    self.interpolator = 'b-splines'
            if event.key == K_r:
                if not self.animation_mode:
                    self.interpolator = 'catmull-rom'
            if event.key == K_c:
                if not self.animation_mode:
                    self.interpolator = 'c2-interpolating'
            if event.key == K_SPACE:
                self.animation_mode = not self.animation_mode
                self.animation_loop = False
                self.insert_mode = False
                self.delete_mode = False
                self.world.object_pos = [-1, -1]
                self.world.t = 0
                self.world.dt = 1
            if event.key == K_LEFT:
                if self.animation_mode:
                    self.world.decrement_dt()
            if event.key == K_RIGHT:
                if self.animation_mode:
                    self.world.increment_dt()
            if event.key == K_o: # loop
                if self.animation_mode:
                    self.animation_loop = not self.animation_loop
            if event.key == K_h:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.world.show_control_points = not self.world.show_control_points
                    self.world.show_interpol = not self.world.show_interpol
                else:
                    self.world.show_grid = not self.world.show_grid
                    self.world.show_axes = not self.world.show_axes
            

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_press(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            self.grabbed_idx = None
        if event.type == pygame.MOUSEMOTION:
            if self.grabbed_idx is not None:
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:                
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                xm, ym = pygame.mouse.get_pos()
                self.world.update_control_point(self.grabbed_idx, xm, ym)
            else:
                if pygame.mouse.get_cursor() == pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def handle_mouse_press(self, mos_pos):
        if self.insert_mode:
            self.world.add_control_point(mos_pos[0], mos_pos[1])
        elif self.delete_mode:
            di = self.world.get_closest_control_point_index(mos_pos[0], mos_pos[1])
            if di is not None:
                self.world.delete_control_point(di)
        else: # drag
            self.grabbed_idx = self.world.get_closest_control_point_index(mos_pos[0], mos_pos[1])
        
        checkRange = lambda mos_pos, mx, Mx, my, My : ((mos_pos[0] >= mx and mos_pos[0] <= Mx) and (mos_pos[1] >= my and mos_pos[1] <= My))
        # mode buttons
        if (checkRange(mos_pos, 10, 90, 255, 295)): # click inside insert box
            self.insert_mode = not self.insert_mode
            self.delete_mode = False
            self.animation_mode = False
            self.animation_loop = False
        if (checkRange(mos_pos, 100, 190, 255, 295)): # click inside delete box
            self.delete_mode = not self.delete_mode
            self.insert_mode = False
            self.animation_mode = False
            self.animation_loop = False
        
        # animation buttons
        if (checkRange(mos_pos, 10, 60, 345, 395)): # skip_back
            if self.animation_mode:
                self.world.decrement_dt()
        if (checkRange(mos_pos, 65, 115, 345, 395)): # anim_btn
            self.animation_mode = not self.animation_mode
            self.animation_loop = False
            self.insert_mode = False
            self.delete_mode = False
            self.world.object_pos = [-1, -1]
            self.world.t = 0
            self.world.dt = 1
        if (checkRange(mos_pos, 120, 170, 345, 395)): # skip_forward
            if self.animation_mode:
                self.world.increment_dt()
                175, 350, 42, 42
        if (checkRange(mos_pos, 175, 217, 350, 392)): # loop
            if self.animation_mode:
                self.animation_loop = not self.animation_loop

    def draw(self) -> None:
        params = {
            "grabbed_idx": self.grabbed_idx,
            "insert_mode": self.insert_mode,
            "delete_mode": self.delete_mode,
            "animation_mode": self.animation_mode,
            "interpolator": self.interpolator,
            "animation_loop": self.animation_loop
        }
        drawCommands(self.window, params)
        is_anim_running = drawWorld(self.world, self.window, params)
        if self.animation_mode:
            if not is_anim_running:
                self.world.t = 0
                if not self.animation_loop:
                    self.animation_mode = False
            
    def run(self) -> None:
        while True:
            self.window.fill(WINDOW_BACKGROUND)
            self.draw()
            for event in pygame.event.get():
                self.event_handler(event)
            pygame.display.update()