import pygame
import sys
import random
import webbrowser

from button import Button

class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/Bass.png")
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

    def lifespan(self):
        if(self.currentlife > 0):
            self.currentlife = self.currentlife - 1
        elif(self.currentlife == 0):
            if(self.alive): 
                self.image = pygame.transform.rotate(self.image, 180)
                self.alive = False


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
BUTTON_COLOR = (72, 118, 255)
BUTTON_SHADOW_COLOR = (41, 67, 145)

# sizes
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
shop_button_rect = pygame.Rect(screen_width - 170, 20, 130, 40)

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
button_font = pygame.font.SysFont('Calibri', 18, bold=True)

food_counts = {
    'Food 1' : 3,
    'Food 2' : 2,
    'Food 3' : 5
}

balance = 100

food_keys = ['Food 1', 'Food 2', 'Food 3']
top_bar_rect = pygame.Rect(0,0,screen_width, 80)

class Food:
    def __init__(self, x, y, color, food_type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.is_falling = False
        self.is_dragged = True # Start in dragged state
        self.food_type = food_type

    def move(self):
        if self.is_falling:
            self.rect.y += 5

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

foods = []
dragged_food = None
label_rects = {}
bubbles = []
clock = pygame.time.Clock()

running = True

sprites = pygame.sprite.Group()
fish = Fish()
sprites.add(fish)

showShop = False # Flag to indicate if the shop interface is active
feedingEnabled = True

mouseClicked = False

shopFoodOne = Button(screen, "green", 300, 200, 30)
foodOneCost = 10
shopFoodTwo = Button(screen, "green", 400, 200, 30)
foodTwoCost = 20
shopFoodThree = Button(screen, "green", 500, 200, 30)
foodThreeCost = 30

balance = 100 # starting currency balance

mousePosX = 0
mousePosY = 0
def getMousePosition():
    global mousePosX, mousePosY
    mousePosX, mousePosY = pygame.mouse.get_pos()

def drawShopInterface():
    # Draw the shop interface background
    pygame.draw.rect(screen, "brown", (200 , 100, 600, 420))
    shopFoodOne.draw()
    shopFoodTwo.draw()
    shopFoodThree.draw()

def refreshButtons():
    global mouseClicked
    mouseClicked = False

def toggleShopInterface():
    global showShop
    global feedingEnabled
    feedingEnabled = not feedingEnabled
    showShop = not showShop

while running:
    # poll for events
    for event in pygame.event.get():
                #check if shop should be opened when mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if shop_button_rect.collidepoint(event.pos):
                toggleShopInterface()
                feedingEnabled = not feedingEnabled
        if event.type == pygame.QUIT:  # X button
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for food_name, rect in label_rects.items():
                    if rect.collidepoint(event.pos) and food_counts[food_name] > 0:
                        food_counts[food_name] -= 1
                        new_food = Food(event.pos[0], event.pos[1], (255, 0, 0), food_name)
                        print(food_name)
                        foods.append(new_food)
                        dragged_food = new_food
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseClicked = True
            if event.button == 1 and dragged_food is not None:
                dragged_food.is_dragged = False
                dragged_food.is_falling = True
                dragged_food = None
        elif event.type == pygame.MOUSEMOTION:
            if dragged_food is not None:
                dragged_food.rect.center = event.pos

    for food in foods[:]:
        food.move()
        if food.rect.top > screen_height:
            foods.remove(food)

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
        label_rects[food_name] = label_rect
        screen.blit(label_surface, label_rect)

        #value left of the food
        count_surface = count_font.render(str(count), True, UI_COUNT_COLOR)
        count_rect = count_surface.get_rect(center=(column_x, 55))
        screen.blit(count_surface, count_rect)

    #button for shop
    pygame.draw.rect(screen, BUTTON_COLOR, shop_button_rect, border_radius = 10)
    
    shop_text_surface = count_font.render("Shop", True, UI_TEXT_COLOR)
    shop_text_rect = shop_text_surface.get_rect(center=shop_button_rect.center)
    screen.blit(shop_text_surface, shop_text_rect)
    
    balance_text = count_font.render("$" + str(balance), True, UI_TEXT_COLOR)
    screen.blit(balance_text, (20, 20))

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

    for food in foods:
        food.draw(screen)
        
    sprites.draw(screen)
    sprites.update()
    
    getMousePosition()

    if showShop:
        drawShopInterface()
        
        if mouseClicked:
            if shopFoodOne.is_hovering((mousePosX, mousePosY)) and balance >= foodOneCost:
                # Add food one to inventory and subtract currency
                food_counts['Food 1'] += 1
                balance -= foodOneCost
            elif shopFoodTwo.is_hovering((mousePosX, mousePosY)) and balance >= foodTwoCost:
                # Add food two to inventory and subtract currency
                food_counts['Food 2'] += 1
                balance -= foodTwoCost
            elif shopFoodThree.is_hovering((mousePosX, mousePosY)) and balance >= foodThreeCost:
                # Add food three to inventory and subtract currency
                food_counts['Food 3'] += 1
                balance -= foodThreeCost

    refreshButtons()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()