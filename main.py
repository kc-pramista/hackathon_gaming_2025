import pygame
import sys
import random

# pygame setup
pygame.init()
pygame.display.set_caption("Relaxing Fish Game")

# DEFINITIONS
SKY_BLUE = (85, 156, 195)
Ocean_color = (2, 62, 138)
BUBBLE_COLOR = (200, 225, 255, 100)
REFLECTION_COLOR = (255, 255, 255, 120)

# sizes
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))

CONTAINER_PADDING = 20

bg = pygame.image.load("assets/ocean_bg.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))

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
    if random.randint(1, 80) == 1:
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
    screen.blit(bg, (0,0))

    # Draw bubbles
    for bubble in bubbles:
        radius = int(bubble['radius'])
        bubble_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        pygame.draw.circle(bubble_surface, BUBBLE_COLOR, (radius, radius), radius)

        # reflection in bubble
        reflection_width = int(radius * 0.7)
        reflection_height = int(radius * 0.4)
        reflection_rect = pygame.Rect(0, 0, reflection_width, reflection_height)
        reflection_rect.center = (radius + int(radius * 0.2), radius - int(radius * 0.2))
        
        pygame.draw.ellipse(bubble_surface, REFLECTION_COLOR, reflection_rect)

        top_left_x = bubble['x'] - radius
        top_left_y = bubble['y'] - radius
        screen.blit(bubble_surface, (top_left_x, top_left_y))

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
sys.exit()