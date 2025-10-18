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
UI_BG_COLOR = (10, 25, 47, 180)
UI_TEXT_COLOR = (220, 220, 220)
UI_COUNT_COLOR = (255, 255, 255) 

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

label_font = pygame.font.SysFont('Arial', 22)
count_font = pygame.font.SysFont('Arial', 32, bold=True)

food_counts = {
    'Food 1' : 3,
    'Food 2' : 2,
    'Food 3' : 5
}
food_keys = ['Food 1', 'Food 2', 'Food 3']
top_bar_rect = pygame.Rect(0,0,screen_width, 80)

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
    bubbles = [bubble for bubble in bubbles if bubble['y'] > top_bar_rect.bottom]

    # drawing
    screen.blit(bg, (0,0))

    ui_surface = pygame.Surface((top_bar_rect.width, top_bar_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(ui_surface, UI_BG_COLOR, ui_surface.get_rect())
    screen.blit(ui_surface, (top_bar_rect.x, top_bar_rect.y))


    spacing = 300
    screen_center_x = screen_width/2

    column_positions = [
        screen_center_x - spacing,
        screen_center_x,
        screen_center_x + spacing
    ]

    for i, food_name in enumerate(food_keys):
        column_x = column_positions[i]

        count = food_counts[food_name]

        #putting name of the food
        label_surface = label_font.render(food_name, True, UI_TEXT_COLOR)
        label_rect = label_surface.get_rect(center=(column_x, 25))
        screen.blit(label_surface, label_rect)

        #value left of the food
        count_surface = count_font.render(str(count), True, UI_COUNT_COLOR)
        count_rect = count_surface.get_rect(center=(column_x, 55))
        screen.blit(count_surface, count_rect)



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