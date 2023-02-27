import pygame
from ..settings import *


class Button:
    def __init__(
        self,
        text: str = "Insert text here", 
        font_size: int = 20, 
        dim: tuple[int, int] = (200, 100), 
        center_pos: tuple[int, int] = (100, 50), 
        topleft_pos:  tuple[int, int] | None = None, 
        bg_color: tuple[int, int, int] = (154, 171, 170), 
        bg_tocolor: tuple[int, int, int] = (110, 122, 122),
        callback: callable = None,
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
            callback (callable | None, optional): callback function. Defaults to None.
        """
        
        self.font = pygame.font.Font("freesansbold.ttf", font_size)
        self.text = text
        self.bg_color = bg_color
        self.bg_tocolor = bg_tocolor
        self.callback = callback

        if not topleft_pos:
            self.rect = pygame.Rect(center_pos, dim)
            self.rect.center = center_pos
        else:
            self.rect = pygame.Rect(topleft_pos, dim)
            
        self.screen = pygame.display.get_surface()
        self.clicking = False

    def draw(self):
        """Draws the button to the screen.
        """
        if self.hovering():
            pygame.draw.rect(self.screen, self.bg_tocolor, self.rect)
        else:
            pygame.draw.rect(self.screen, self.bg_color, self.rect)

        text_surface = self.font.render(self.text, True, DARKGRAY)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)
        
    def update(self):
        """Updates the button every frame.
        """
        self.check_click()

    def hovering(self):
        """Checks if the mouse is hovering the button.

        Returns:
            bool: True if hovering, False otherwise.
        """
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my):
            return True
        return False
    
    def check_click(self):
        """Checks if the button is being clicked. If so, calls the callback function.
        """        
        clicking = pygame.mouse.get_pressed()[0]
        
        if self.hovering() and clicking and not self.clicking:
            if self.callback:
                self.callback()
                
        self.clicking = clicking

def write_text(
    text: str = 'Insert text here', 
    center_pos: tuple[int, int] = (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), 
    topleft_pos:  tuple[int, int] | None = None, 
    font_size: int = 50, 
    color: tuple[int, int, int] = (0, 0, 0), 
):
    """Writes text to the screen. Can specify center position or topleft position.

    Args:
        text (str, optional): text to write. Defaults to 'Insert text here'.
        center_pos (tuple[int, int], optional): center position. Defaults to (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2).
        topleft_pos (tuple[int, int] | None, optional): topleft position. Defaults to None.
        font_size (int, optional): font size. Defaults to 50.
        color (tuple[int, int, int], optional): RGB color. Defaults to (0, 0, 0).
    """
    
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont("arial", font_size, bold=True)
    text_surf = font.render(text, True, color)
    if not topleft_pos:
        text_rect = text_surf.get_rect(center=center_pos)
    else:
        text_rect = text_surf.get_rect(topleft=topleft_pos)
    screen.blit(text_surf, text_rect)


def draw_transparent_rect(
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
    screen = pygame.display.get_surface()

    if topleft_pos:
        screen.blit(s, topleft_pos)
    else:
        screen.blit(s, (center_pos[0]-dim[0]//2, center_pos[1]-dim[1]//2))
