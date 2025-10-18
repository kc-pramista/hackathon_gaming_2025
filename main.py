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
        self.speedx = 2
        self.speedy = 1

        self.maxlife = 600
        self.currentlife = 600
        self.alive = True

    def update(self):
        if(self.alive):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.x >= 975:
                self.speedx = -self.speedx
                self.image = pygame.transform.flip(self.image, True, False)
            if self.rect.x <= 15:
                self.speedx = -self.speedx
                self.image = pygame.transform.flip(self.image, True, False) 
            if self.rect.y <= 15:
                self.speedy = -self.speedy
            if self.rect.y >= 700:
                self.speedy = -self.speedy
        else:
            new_a = self.image.get_alpha() - (255/120)
            if(new_a <0):
                new_a = 0
            
            self.rect.y = self.rect.y - self.speedx
            self.image.set_alpha(new_a)


    def render(self, display):
        display.blit(self.image, (self.x_pos, self.y_pos))

    def lifespan(self):
        if(self.currentlife > 0):
            self.currentlife = self.currentlife - 1
        elif(self.currentlife == 0):
            if(self.alive): 
                self.image = pygame.transform.rotate(self.image, 180)
                self.alive = False





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
    fish.lifespan()

    screen.fill("blue")
    sprites.draw(screen)

    # RENDER YOUR GAME HER
    



    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()