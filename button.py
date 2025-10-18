
import pygame

class Button:
    def __init__(self, surface, color, pos_x, pos_y, radius):
        self.surface = surface
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (self.pos_x, self.pos_y), self.radius)

    def is_hovering(self, mouse_pos):
        return (mouse_pos[0] - self.pos_x) ** 2 + (mouse_pos[1] - self.pos_y) ** 2 < self.radius ** 2