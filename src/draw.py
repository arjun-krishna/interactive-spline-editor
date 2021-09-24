"""
filename: draw.py
desc:
Contains drawing primitives
"""
from splines import bezier_interpolation_at_t, bezier_interpolation_of_points, bspline_interpolation_of_points_v2, c2_interpolation_of_points, catmullrom_interpolation_of_points, linear_interpolation_of_points
import pygame
from constants import *
from world import World
import os

def drawCommands(window: pygame.Surface, params: dict):
    """
    draw the command helper
    """
    font = pygame.font.SysFont('Comic Sans MS', 20)
    ts = font.render("Quick Commands", False, TEXT_COLOR)
    window.blit(ts, (10, 10))
    pygame.draw.lines(window, TEXT_COLOR, False, [(10, 40), (200, 40)], 2)

    cmd_font = pygame.font.SysFont('Comic Sans MS', 17)
    # q command
    window.blit(cmd_font.render("Quit              -  q", False, TEXT_COLOR), (10, 50))
    # i command
    window.blit(cmd_font.render("Insert Point  -  i", False, TEXT_COLOR), (10, 80))
    # x command
    window.blit(cmd_font.render("Delete Point  -  x", False, TEXT_COLOR), (10, 110))
    # c command
    window.blit(cmd_font.render("Clear World  -  d", False, TEXT_COLOR), (10, 140))
    # Esc command
    window.blit(cmd_font.render("Clear Modes  -  ESC", False, TEXT_COLOR), (10, 170))
    
    # mode indicator
    window.blit(font.render("Mode Indicators", False, TEXT_COLOR), (10, 210))
    pygame.draw.lines(window, TEXT_COLOR, False, ([(10, 240), (200, 240)]))

    m_rect = pygame.Rect(10, 255, 80, 40)
    col = ACTIVE_COLOR if params['insert_mode'] else INACTIVE_COLOR
    pygame.draw.rect(window, col, m_rect, 0)
    window.blit(cmd_font.render("Insert", False, WINDOW_BACKGROUND), (23, 260))

    m_rect = pygame.Rect(100, 255, 80, 40)
    col = ACTIVE_COLOR if params['delete_mode'] else INACTIVE_COLOR
    pygame.draw.rect(window, col, m_rect, 0)
    window.blit(cmd_font.render("Delete", False, WINDOW_BACKGROUND), (113, 260))
    
    # animator
    window.blit(font.render("Animator", False, TEXT_COLOR), (10, 310))
    pygame.draw.lines(window, TEXT_COLOR, False, ([(10, 340), (200, 340)]))
    
    skip_back_btn = pygame.image.load(os.path.join('assets', 'skip-backward-btn.png'))
    skip_frwd_btn = pygame.image.load(os.path.join('assets', 'skip-forward-btn.png'))
    loop_btn = pygame.image.load(os.path.join('assets', 'arrow-repeat.png'))
    anim_btn = pygame.image.load(os.path.join('assets', 'stop-btn.png')) if params['animation_mode'] else pygame.image.load(os.path.join('assets', 'play-btn.png')) 
    
    window.blit(skip_back_btn, (10, 345))
    window.blit(anim_btn, (65, 345))
    window.blit(skip_frwd_btn, (120, 345))
    col = LOOP_ACTIVE_COLOR if params['animation_loop'] else LOOP_INACTIVE_COLOR
    l_rect = pygame.Rect(175, 350, 42, 42)
    pygame.draw.rect(window, col, l_rect, 0)
    window.blit(loop_btn, (175, 352))

    # interpolators
    window.blit(font.render("Interpolators", False, TEXT_COLOR), (10, 440))
    pygame.draw.lines(window, TEXT_COLOR, False, ([(10, 470), (200, 470)]))
    
    # l command
    window.blit(cmd_font.render("Linear                   -  l", False, TEXT_COLOR), (10, 475))
    # z command
    window.blit(cmd_font.render("Bezier                  -  z", False, TEXT_COLOR), (10, 505))
    # b command
    window.blit(cmd_font.render("B-Splines             -  b", False, TEXT_COLOR), (10, 535))
    # r command
    window.blit(cmd_font.render("Catmull-Rom        -  r", False, TEXT_COLOR), (10, 565))
    # c command
    window.blit(cmd_font.render("C2-interpolating  -  c", False, TEXT_COLOR), (10, 595))
    i_rect = pygame.Rect(10, 630, 160, 40)
    pygame.draw.rect(window, TEXT_COLOR, i_rect, 1)
    if params['interpolator'] is not None:
        window.blit(cmd_font.render(params['interpolator'], False, TEXT_COLOR), (15, 635))

    # mouse indicator
    window.blit(cmd_font.render("Mouse Pointer", False, TEXT_COLOR), (10, 680))
    window.blit(cmd_font.render("X", False, TEXT_COLOR), (10, 723))
    window.blit(cmd_font.render("Y", False, TEXT_COLOR), (110, 723))
    mx_rect = pygame.Rect(30, 722, 60, 30)
    pygame.draw.rect(window, TEXT_COLOR, mx_rect, 1)
    my_rect = pygame.Rect(130, 722, 60, 30)
    pygame.draw.rect(window, TEXT_COLOR, my_rect, 1)

    
def drawWorld(world: World, window: pygame.Surface, params: dict):
    drawCoAxis(world, window, params)
    drawMouseXY(world, window, params)
    ips = draw_interpol(world, window, params)
    if world.show_control_points:
        drawControlPoints(world, window, params)
    pygame.draw.lines(window, TEXT_COLOR, False, ([(world.min_xs, 0), (world.min_xs, world.max_ys)]), 2)
    if params['animation_mode']:
        return drawAnimation(world, window, ips, params)
    else:
        return False
    

def drawAnimation(world, window, ips, params):
    if world.t < len(ips):
        world.object_pos = ips[world.t]
        world.t += world.dt
        pygame.draw.circle(window, OBJECT_COLOR, world.object_pos, 4*CONTROL_POINT_RADIUS)
        return True
    else:
        return False   

def drawControlPoints(world: World, window: pygame.Surface, params: dict):
    for cp in world.control_points:
        pygame.draw.circle(window, CONTROL_POINT_COLOR, cp, CONTROL_POINT_RADIUS)
    if params['grabbed_idx'] is not None:
        pygame.draw.circle(window, CONTROL_POINT_COLOR, world.control_points[params['grabbed_idx']], 2*CONTROL_POINT_RADIUS, 2)

def draw_interpol(world: World, window: pygame.Surface, params: dict):
    if params['interpolator'] == 'linear':
        ips = linear_interpolation_of_points(world.control_points)
    elif params['interpolator'] == 'bezier':
        ips = bezier_interpolation_of_points(world.control_points)
    elif params['interpolator'] == 'b-splines':
        ips = bspline_interpolation_of_points_v2(world.control_points)
    elif params['interpolator'] == 'catmull-rom':
        ips = catmullrom_interpolation_of_points(world.control_points)
    elif params['interpolator'] == 'c2-interpolating':
        ips = c2_interpolation_of_points(world.control_points)
    else:
        ips = []
    if len(ips) < 2 or not world.show_interpol: # needs atleast two points
        return ips
    for p0, p1 in zip(ips[:-1], ips[1:]):
        pygame.draw.lines(window, CURVE_COLOR, False, [p0, p1], 2)
    return ips

def drawCoAxis(world: World, window: pygame.Surface, params: dict):
    """
    draws the co-ordinate axis
    """
    if world.show_grid:
        drawXYGrid(world, window, params)
    if world.show_axes:
        drawXYAxes(world, window, params)

def drawXYGrid(world: World, window: pygame.Surface, params: dict):
    """
    draws a rectangular grid
    """
    xo, yo = world.get_origin()
    for x in range(xo, world.max_xs, world.grid_size):
        for y in range(yo - world.grid_size, world.min_ys, -world.grid_size):
            rect = pygame.Rect(x, y, world.grid_size, world.grid_size)
            pygame.draw.rect(window, GRID_COLOR, rect, 1)
        for y in range(yo, world.max_ys, world.grid_size):
            rect = pygame.Rect(x, y, world.grid_size, world.grid_size)
            pygame.draw.rect(window, GRID_COLOR, rect, 1)
    for x in range(xo - world.grid_size, world.min_xs, -world.grid_size):
        for y in range(yo - world.grid_size, world.min_ys, -world.grid_size):
            rect = pygame.Rect(x, y, world.grid_size, world.grid_size)
            pygame.draw.rect(window, GRID_COLOR, rect, 1)
        for y in range(yo, world.max_ys, world.grid_size):
            rect = pygame.Rect(x, y, world.grid_size, world.grid_size)
            pygame.draw.rect(window, GRID_COLOR, rect, 1)

def drawXYAxes(world: World, window: pygame.Surface, params: dict):
    """
    draws the XY axis
    """
    xo, yo = world.get_origin()
    pygame.draw.lines(window, X_AXIS_COLOR, False, [(world.min_xs, yo), (world.max_xs, yo)], 2)
    pygame.draw.lines(window, Y_AXIS_COLOR, False, [(xo, world.min_ys), (xo, world.max_ys)], 2)

def drawMouseXY(world: World, window: pygame.Surface, params: dict):
    xs, ys = pygame.mouse.get_pos()
    if world.is_inscreen(xs, ys):
        if params['grabbed_idx'] is None and pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_CROSSHAIR:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        x, y = world.transform_screen_xy(xs, ys)
        font = pygame.font.SysFont('Comic Sans MS', 18)
        window.blit(font.render(f"{x}", False, TEXT_COLOR), (35, 725))
        window.blit(font.render(f"{y}", False, TEXT_COLOR), (135, 725))
        cid = world.get_closest_control_point_index(xs, ys)
        if cid is not None:
            cfont = pygame.font.SysFont('Comic Sans MS', 14)
            window.blit(cfont.render(f"V{cid}", False, TEXT_COLOR), (xs+10, ys+10))
    else:
        if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)