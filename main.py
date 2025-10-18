import pygame
import sys
import random

# pygame setup
pygame.init()
pygame.display.set_caption("Relaxing Fish Game")

# DEFINITIONS
BLUE = (0, 0, 255)
SKY_BLUE = (85, 156, 195)
Ocean_color = (2, 62, 138)
OCEAN_TOP = (7, 107, 171)
OCEAN_BOTTOM = (2, 62, 138)
SAND_COLOR = (242, 224, 159)
BUBBLE_COLOR = (200, 225, 255, 100)
BORDER_BLUE = (72, 118, 255)

# sizes
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))

CONTAINER_PADDING = 20
BORDER_WIDTH = 5

container = pygame.Rect(
    CONTAINER_PADDING,
    CONTAINER_PADDING,
    screen_width - CONTAINER_PADDING * 2,
    screen_height - CONTAINER_PADDING * 2,
)

bubbles = []
clock = pygame.time.Clock()

running = True
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # X button
            running = False

    # bubbles
    if random.randint(1, 60) == 1:
        x_pos = random.randint(CONTAINER_PADDING, screen_width - CONTAINER_PADDING)
        radius = random.randint(10, 30)
        speed = random.uniform(0.5, 2.5)
        new_bubble = {
            'x': x_pos,
            'y': screen_height + radius,
            'radius': radius,
            'speed': speed
        }
        bubbles.append(new_bubble)

    # bubble are going up
    for bubble in bubbles:
        bubble['y'] -= bubble['speed']

    # removing bubbles that go off the screen
    bubbles = [bubble for bubble in bubbles if bubble['y'] > -bubble['radius']]

    # drawing
    screen.fill(Ocean_color)

    # Draw bubbles
    for bubble in bubbles:
        pygame.draw.circle(screen, SKY_BLUE, (bubble['x'], bubble['y']), bubble['radius'])

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
sys.exit()