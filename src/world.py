from typing import Tuple
import numpy as np

class World:
    control_points = np.array([]).reshape(0, 2)
    object_pos = [-1, -1]
    t = 0
    dt = 1
    show_grid = True
    show_axes = True
    show_control_points = True
    show_interpol = True

    def __init__(self, start_x, window_width, window_height, grid_size, closeness):
        assert (type(grid_size) == int)
        self.min_xs = start_x
        self.max_xs = window_width
        self.min_ys = 0
        self.max_ys = window_height
        self.grid_size = grid_size
        self.closeness = closeness

        self.xo = (self.max_xs + self.min_xs) // 2
        self.yo = (self.max_ys - self.min_ys) // 2

    def get_origin(self) -> Tuple[int, int]:
        return [self.xo, self.yo]

    def transform_screen_xy(self, xs, ys) -> Tuple[int, int]:
        x = (xs - self.xo) / self.grid_size
        y = (self.yo - ys) / self.grid_size
        return [x, y]

    def is_inscreen(self, xs: int, ys: int) -> bool:
        return (xs >= self.min_xs and xs <= self.max_xs) and \
         (ys >= self.min_ys and ys <= self.max_ys)
    
    def add_control_point(self, x: int, y: int):
        if self.is_inscreen(x, y):
            self.control_points = np.vstack([self.control_points, [x, y]])
    
    def clear_control_points(self):
        self.control_points = np.array([]).reshape(0, 2)
    
    def get_closest_control_point_index(self, x: int, y: int) -> int: 
        if self.control_points.size == 0:
            return None
        C = np.broadcast_to([x, y], self.control_points.shape)
        # manhattan distance
        md = np.isclose(self.control_points, C, atol=self.closeness).sum(axis=1) == C.shape[1]
        if md.any():
            return np.argmax(md)
        else:
            return None
    
    def update_control_point(self, idx: int, x: int, y: int) -> None:
        if self.is_inscreen(x, y):
            self.control_points[idx] = [x, y]

    def delete_control_point(self, idx: int) -> None:
        self.control_points = np.delete(self.control_points, idx, 0)

    def increment_dt(self):
        if self.dt < 20:
            self.dt += 2

    def decrement_dt(self):
        if self.dt > 2:
            self.dt -= 2