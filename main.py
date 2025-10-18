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
        
        self.seek_speed = 5         
        self.target_food = None       
        self.facing_right = True   

        self.maxlife = 600
        self.currentlife = 600
        self.alive = True


    def update(self, foods_list): 
        if(self.alive):
            
            
            # Check if our current target still exists
            if self.target_food and self.target_food not in foods_list:
                self.target_food = None
            
            # Find a new target if we don't have one
            if self.target_food is None:
                for food in foods_list:
                    if food.is_falling:
                        self.target_food = food
                        break

            
            if self.target_food:
                target_x, target_y = self.target_food.rect.center
                fish_x, fish_y = self.rect.center
                
                dx, dy = target_x - fish_x, target_y - fish_y
                # Calculate distance to normalize the speed
                distance = (dx**2 + dy**2)**0.5

                current_speed_x = 0
                
                if distance > 1: # Avoid division by zero and jittering
                    # Calculate velocity vector
                    current_speed_x = (dx / distance) * self.seek_speed
                    current_speed_y = (dy / distance) * self.seek_speed
                    
                    self.rect.x += current_speed_x
                    self.rect.y += current_speed_y

                # eating
                if self.rect.colliderect(self.target_food.rect):
                    foods_list.remove(self.target_food) # Remove the food
                    self.target_food = None
                    self.currentlife = min(self.maxlife, self.currentlife + 100) 
                
                # Handle flipping
                if current_speed_x > 0 and not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.facing_right = True
                elif current_speed_x < 0 and self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.facing_right = False

            else:
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                
                # Handle flipping
                if self.speedx > 0 and not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.facing_right = True
                elif self.speedx < 0 and self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.facing_right = False
                
                # Handle wall bouncing
                if self.rect.x >= 975:
                    self.speedx = -abs(self.speedx) # Flip velocity
                if self.rect.x <= 15:
                    self.speedx = abs(self.speedx) # Flip velocity
                if self.rect.y <= 15:
                    self.speedy = abs(self.speedy)
                if self.rect.y >= 700:
                    self.speedy = -abs(self.speedy)
        
        else: # Fish is dead
            new_a = self.image.get_alpha() - (255/120)
            if(new_a <0):
                new_a = 0
            
            self.rect.y -= 1 # Float up
            self.image.set_alpha(new_a)


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

bg = pygame.image.load("assets/ocean_bg.jpeg").convert()
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
    'Food 1' : 5,
    'Food 2' : 0,
    'Food 3' : 0
}

balance = 100

food_keys = ['Food 1', 'Food 2', 'Food 3']
top_bar_rect = pygame.Rect(0,0,screen_width, 80)

food_drop_sound = pygame.mixer.Sound('sounds/food_dropping.mp3')

class Food:
    def __init__(self, x, y, color, food_type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.is_falling = False
        self.is_dragged = True # Start in dragged state
        self.food_type = food_type

    def move(self):
        if self.is_falling:
            self.rect.y += 3

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

showShop = False 
feedingEnabled = True

mouseClicked = False

shop_width = 300
shop_height = 200

button_start_point = screen_width / 2 - shop_width / 2 + 50
button_start_height = screen_height / 2 

shopFoodOne = Button(screen, "green", button_start_point, button_start_height, 30, "Food 1", 10)
foodOneCost = 10
shopFoodTwo = Button(screen, "green", button_start_point + 100, button_start_height, 30, "Food 2", 20)
foodTwoCost = 20
shopFoodThree = Button(screen, "green", button_start_point + 200, button_start_height, 30, "Food 3", 30)
foodThreeCost = 30


fish_multiplier = 1

balance = 20 

mousePosX = 0
mousePosY = 0
def getMousePosition():
    global mousePosX, mousePosY
    mousePosX, mousePosY = pygame.mouse.get_pos()

def drawShopInterface():
    # Draw the shop interface background
    pygame.draw.rect(screen, (50, 50, 50, 120), (screen_width / 2 - shop_width / 2, screen_height / 2 - shop_height / 2, shop_width, shop_height))
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
    
dt = 0

while running:
    # poll for events
    for event in pygame.event.get():
                #check if shop should be opened when mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if shop_button_rect.collidepoint(event.pos):
                toggleShopInterface()
                # feedingEnabled = not feedingEnabled # This line was redundant
        if event.type == pygame.QUIT:  # X button
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # --- MODIFIED: Check if feeding is enabled ---
                if feedingEnabled:
                    for food_name, rect in label_rects.items():
                        if rect.collidepoint(event.pos) and food_counts[food_name] > 0:
                            food_counts[food_name] -= 1
                            new_food = Food(event.pos[0], event.pos[1], (255, 0, 0), food_name)
                            #print(food_name)
                            foods.append(new_food)
                            dragged_food = new_food
                            break
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseClicked = True
            if event.button == 1 and dragged_food is not None:
                dragged_food.is_dragged = False
                dragged_food.is_falling = True # This flags the fish to chase it

                if food_drop_sound:
                    food_drop_sound.play()

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
    bubbles = [bubble for bubble in bubbles if bubble['y'] > top_bar_rect.bottom + radius]

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
    if(showShop):
        shop_text_surface = count_font.render("Close", True, UI_TEXT_COLOR)
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
    # --- MODIFIED: Pass the 'foods' list to the update method ---
    sprites.update(foods) 
    
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
    
    dt += 1
    
    if dt % 180 == 0:
        balance += 1 * fish_multiplier
    
    if dt > 360:
        dt = 0
    clock.tick(60)
pygame.quit()
sys.exit()