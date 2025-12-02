import pygame
from config import COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT

class Button:
    def __init__(self, rect, text, font, callback,
                 bg_color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=14)

        label = self.font.render(self.text, True, COLOR_TEXT)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
