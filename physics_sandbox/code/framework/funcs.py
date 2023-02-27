import pygame


def get_mouse_pos():
    """Gets the mouse x,y position.

    Returns:
        tuple[int, int]: mouse x,y position.
    """
    return pygame.mouse.get_pos()


def pprint_matrix(matrix: list[list[any]]):
    """Prints a matrix in a nice way.

    Args:
        matrix (list[list[any]]): matrix to print.
    """
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))