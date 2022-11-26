from .settings import *


def pos_to_ij(x: int, y: int) -> tuple[int, int]:
    return x*GRID_SIZE//WINDOW_SIZE[0], y*GRID_SIZE//WINDOW_SIZE[1]


def ij_to_pos(i: int, j: int) -> tuple[int, int]:
    return i*WINDOW_SIZE[0]//GRID_SIZE+1, j*WINDOW_SIZE[1]//GRID_SIZE+1