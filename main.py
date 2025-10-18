import pygame
import sys
import random

pygame.init()

#DEFINITIONS
BLUE = (0, 0, 255)
SKY_BLUE = (85, 156, 195)

# sizes
screen_width, screen_height = 720, 720
screen = pygame.display.set_mode((screen_width, screen_height))

bubbles = []
clock = pygame.time.Clock()

pygame.display.set_caption("Blue Canvas")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #X button
            running = False


    #bubbles
    if random.randint(1,60) == 1:
        x_pos = random.randint(0, screen_width)
        radius = random.randint(10,30)
        speed = random.uniform(0.5, 2.5)
        new_bubble = {
            'x': x_pos,
            'y': screen_height + radius,
            'radius': radius,
            'speed': speed
        }
        bubbles.append(new_bubble)

    #bubble are going up
    for bubble in bubbles:
        bubble['y'] -= bubble['speed']

    #removing bubbles that go off the screen
    bubbles = [bubble for bubble in bubbles if bubble['y'] > -bubble['radius']]

    #drawing
    screen.fill(BLUE)
    for bubble in bubbles:
        pygame.draw.circle(screen, SKY_BLUE, (bubble['x'], bubble['y']), bubble['radius'])
    
    pygame.display.flip()

    clock.tick(100)

pygame.quit()
sys.exit()
