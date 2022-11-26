from .settings import *


def pos_to_ij(x: int, y: int) -> tuple[int, int]:
    """_summary_: Converts a position to an index.

    Args:
        x (int): x position.
        y (int): y position.

    Returns:
        tuple[int, int]: i, j index.
    """
    return x*GRID_SIZE//WINDOW_SIZE[0], y*GRID_SIZE//WINDOW_SIZE[1]


def ij_to_pos(i: int, j: int) -> tuple[int, int]:
    """_summary_: Converts an index to a position.

    Args:
        i (int): i index.
        j (int): j index.

    Returns:
        tuple[int, int]: x, y position.
    """
    return i*WINDOW_SIZE[0]//GRID_SIZE+1, j*WINDOW_SIZE[1]//GRID_SIZE+1