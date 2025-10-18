import pygame
import random
vec = pygame.math.Vector2




class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Assets/Images/Bass.png")
        self.rect = self.image.get_rect()

        self.rect.x = 500
        self.rect.y = 320
        self.speed = 2

    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 975:
            self.speed = -self.speed
        if self.rect.x <= 15:
            self.speed = -self.speed  

    def render(self, display):
        display.blit(self.image, (self.x_pos, self.y_pos))


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1000, 720))
pygame.display.set_caption("fish tank")
clock = pygame.time.Clock()
running = True

sprites = pygame.sprite.Group()
fish = Fish()
sprites.add(fish)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    sprites.update()

    screen.fill("blue")
    sprites.draw(screen)

    # RENDER YOUR GAME HER
    



    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()