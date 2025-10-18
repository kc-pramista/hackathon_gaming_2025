import pygame
import sys
import random

# pygame setup
pygame.init()
pygame.display.set_caption("Relaxing Fish Game")

# DEFINITIONS

Ocean_color = (2, 62, 138)
BUBBLE_COLOR = (200, 225, 255, 100)
REFLECTION_COLOR = (255, 255, 255, 120)

# sizes
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))

background_image = pygame.image.load('assets/ocean_bg.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

CONTAINER_PADDING = 20
BORDER_WIDTH = 5
SEABED_HEIGHT = 60

top_bar_rect = pygame.Rect(0, 0, screen_width, 60)
drop_zone = pygame.Rect(0, 0, screen_width, 60)

container = pygame.Rect(
    CONTAINER_PADDING,
    CONTAINER_PADDING,
    screen_width - CONTAINER_PADDING * 2,
    screen_height - CONTAINER_PADDING * 2,
)

class Food:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.is_falling = False
        self.is_dragged = False

    def move(self):
        if self.is_falling:
            self.rect.y += 5

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

foods = [
    Food(300, 100, (255, 0, 0)),
    Food(400, 100, (0, 255, 0)),
    Food(500, 100, (0, 0, 255)),
    Food(600, 100, (255, 255, 0)),
    Food(700, 100, (255, 0, 255)),
]
dragged_food = None
bubbles = []
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                for food in foods:
                    # You can only pick up food that isn't already falling
                    if food.rect.collidepoint(event.pos) and not food.is_falling:
                        food.is_dragged = True
                        dragged_food = food
                        break
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragged_food is not None:
                dragged_food.is_dragged = False
                # If the food is released below the drop zone, it starts falling
                if not drop_zone.contains(dragged_food.rect):
                    dragged_food.is_falling = True
                dragged_food = None
        
        elif event.type == pygame.MOUSEMOTION:
            if dragged_food is not None:
                dragged_food.rect.center = event.pos
                dragged_food.rect.clamp_ip(container)


        for food in foods[:]: # Iterate over a copy
            food.move()
        # Remove food that has fallen off the bottom of the screen
            if food.rect.top > container.bottom:
                foods.remove(food)

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
    bubbles = [bubble for bubble in bubbles if bubble['y'] > top_bar_rect.bottom]

    # drawing
    screen.blit(background_image, (0,0))

    # Draw bubbles
    for bubble in bubbles:
        bubble_surface = pygame.Surface((bubble['radius'] * 2, bubble['radius'] * 2), pygame.SRCALPHA)
        pygame.draw.circle(bubble_surface, BUBBLE_COLOR, (bubble['radius'], bubble['radius']), bubble['radius'])
        screen.blit(bubble_surface, (bubble['x'] - bubble['radius'], bubble['y'] - bubble['radius']))



    # draw food 
    for food_item in foods:
        food_item.draw(screen)
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()
sys.exit()
