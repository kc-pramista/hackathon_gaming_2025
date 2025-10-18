
import pygame

class Button:
    def __init__(self, surface, color, pos_x, pos_y, radius, name):
        self.surface = surface
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.name = name

    def draw(self):
        # pygame.draw.circle(self.surface, self.color, (self.pos_x, self.pos_y), self.radius)
        font = pygame.font.SysFont('Arial', 22)
        text = font.render(self.name, True, (220, 220, 220))
        self.surface.blit(text, (self.pos_x - self.radius, self.pos_y - self.radius / 2))

    def is_hovering(self, mouse_pos):
        return (mouse_pos[0] - self.pos_x) ** 2 + (mouse_pos[1] - self.pos_y) ** 2 < self.radius ** 2