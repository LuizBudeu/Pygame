import pygame
from .settings import *


class Button:
    def __init__(
        self,
        text: str = "Insert text here", 
        font_size: int = 20, 
        dim: tuple[int, int] = (200, 100), 
        center_pos: tuple[int, int] = (100, 50), 
        topleft_pos:  tuple[int, int] | None = None, 
        bg_color: tuple[int, int, int] = (154, 171, 170), 
        bg_tocolor: tuple[int, int, int] = (110, 122, 122)
    ):
        """Creates a button. Can specify center position or topleft position.

        Args:
            text (str, optional): text to write. Defaults to "Insert text here".
            font_size (int, optional): font size. Defaults to 20.
            dim (tuple[int, int], optional): Rect dimension. Defaults to (200, 100).
            center_pos (tuple[int, int], optional): center position. Defaults to (100, 50).
            topleft_pos (tuple[int, int] | None, optional): topleft position. Defaults to None.
            bg_color (tuple[int, int, int], optional): normal button background RGB color. Defaults to (154, 171, 170).
            bg_tocolor (tuple[int, int, int], optional): hovering button background RGB color. Defaults to (110, 122, 122).
        """
        
        self.font = pygame.font.Font("freesansbold.ttf", font_size)
        self.text = text
        self.bg_color = bg_color
        self.bg_tocolor = bg_tocolor

        if not topleft_pos:
            self.rect = pygame.Rect(
                center_pos[0] - dim[0]//2, center_pos[1] - dim[1]//2, dim[0], dim[1])
        else:
            self.rect = pygame.Rect(
                topleft_pos[0], topleft_pos[1], dim[0], dim[1])

    def draw(self, screen: pygame.Surface):
        """Draws the button to the screen.
        """
        if self.hovering():
            pygame.draw.rect(screen, self.bg_tocolor, self.rect)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)

        text_surface = self.font.render(self.text, True, DARKGRAY)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def hovering(self):
        """Checks if the mouse is hovering the button.

        Returns:
            bool: True if hovering, False otherwise.
        """
        mx, my = get_mouse_pos()
        if self.rect.collidepoint(mx, my):
            return True
        return False


def write_text(
    screen: pygame.Surface,
    text: str = 'Insert text here', 
    font_size: int = 50, 
    color: tuple[int, int, int] = (0, 0, 0), 
    center_pos: tuple[int, int] = (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), 
    topleft_pos:  tuple[int, int] | None = None, 
):
    """Writes text to the screen. Can specify center position or topleft position.

    Args:
        screen (pygame.Surface): game screen.
        text (str, optional): text to write. Defaults to 'Insert text here'.
        font_size (int, optional): font size. Defaults to 50.
        color (tuple[int, int, int], optional): RGB color. Defaults to (0, 0, 0).
        center_pos (tuple[int, int], optional): center position. Defaults to (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2).
        topleft_pos (tuple[int, int] | None, optional): topleft position. Defaults to None.
    """
    
    font = pygame.font.Font("freesansbold.ttf", font_size)
    text_surf = font.render(text, True, color)
    if not topleft_pos:
        text_rect = text_surf.get_rect(center=center_pos)
    else:
        text_rect = text_surf.get_rect(topleft=topleft_pos)
    screen.blit(text_surf, text_rect)


def draw_transparent_rect(
    screen: pygame.Surface,
    center_pos: tuple[int, int] = (100, 100), 
    topleft_pos: tuple[int, int] | None = None,
    dim: tuple[int, int] = WINDOW_SIZE, 
    color: tuple[int, int, int] =(255, 255, 255),
    alpha: int = 128
):
    """Draws a transparent rectangle to the screen. Can specify center position or topleft position.

    Args:
        screen (pygame.Surface): game screen.
        center_pos (tuple[int, int], optional): center position. Defaults to (100, 100).
        topleft_pos (tuple[int, int] | None, optional): topleft position. Defaults to None.
        dim (tuple[int, int], optional): Rect dimension. Defaults to WINDOW_SIZE.
        color (tuple[int, int, int], optional): RGB color. Defaults to (255, 255, 255).
        alpha (int, optional): alpha legel. Defaults to 128.
    """
    s = pygame.Surface(dim)  # the size of your rect
    s.set_alpha(alpha)                # alpha level
    s.fill(color)           # this fills the entire surface

    if topleft_pos:
        screen.blit(s, topleft_pos)
    else:
        screen.blit(s, (center_pos[0]-dim[0]//2, center_pos[1]-dim[1]//2))


def get_mouse_pos():
    """Gets the mouse x,y position.

    Returns:
        tuple[int, int]: mouse x,y position.
    """
    return pygame.mouse.get_pos()


def pprint_matrix(matrix: list[list]):
    """Prints a matrix in a nice way.

    Args:
        matrix (list[list]): matrix to print.
    """
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
