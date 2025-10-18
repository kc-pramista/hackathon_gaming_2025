import pygame
import os
import random

from button import Button


class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # self.image = pygame.image.load("Assets/Images/Bass.png")
        #self.rect = self.image.get_rect()

        #self.rect.x = 500
        #self.rect.y = 320

        self.x = 500
        self.y = 320
        self.speed = 2

    def update(self):
        # self.rect.x += self.speed
        # if self.rect.x >= 975:
            #self.speed = -self.speed
        #if self.rect.x <= 15:
            #self.speed = -self.speed  

        self.x += self.speed
        if self.x >= 975:
            self.speed = -self.speed
        if self.x <= 15:
            self.speed = -self.speed

    def render(self, display):
        #display.blit(self.image, (self.x_pos, self.y_pos))
        pygame.draw.circle(display, "white", (self.x, self.y), 20)

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((1000, 720))
pygame.display.set_caption("fish tank")
clock = pygame.time.Clock()
running = True

# sprites = pygame.sprite.Group()
fish = Fish()
# sprites.add(fish)

showShop = False # Flag to indicate if the shop interface is active
feedingEnabled = True

mouseClicked = False

shopButton = Button(screen, "red", 900, 670, 30)

shopFoodOne = Button(screen, "green", 300, 200, 30)
foodOneCost = 10
shopFoodTwo = Button(screen, "green", 400, 200, 30)
foodTwoCost = 20
shopFoodThree = Button(screen, "green", 500, 200, 30)
foodThreeCost = 30

balance = 100 # starting currency balance

inventoryFoodOne = Button(screen, "yellow", 100, 670, 30)
inventoryFoodTwo = Button(screen, "yellow", 200, 670, 30)
inventoryFoodThree = Button(screen, "yellow", 300, 670, 30)

def getMousePosition():
    global mousePosX, mousePosY
    mousePosX, mousePosY = pygame.mouse.get_pos()

def drawShopInterface():
    # Draw the shop interface background
    pygame.draw.rect(screen, "brown", (200 , 100, 600, 420))
    shopFoodOne.draw()
    shopFoodTwo.draw()
    shopFoodThree.draw()

def drawFishWindow():
    # Draw the fish window background
    pass
    # Function calls for fish elements

def drawConstantElements():
    # Draw the constant elements
    pygame.draw.rect(screen, "brown", (0, 620, 1000, 100))
    shopButton.draw()
    inventoryFoodOne.draw()
    inventoryFoodTwo.draw()
    inventoryFoodThree.draw()

def refreshButtons():
    global mouseClicked
    mouseClicked = False

def toggleShopInterface():
    global showShop
    global feedingEnabled
    feedingEnabled = not feedingEnabled
    showShop = not showShop


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouseClicked = True
    
    getMousePosition()

    #sprites.update()
    fish.update()

    # Bottom Layer of drawing frame
    screen.fill("blue")

    #sprites.draw(screen)
    fish.render(screen)

    if showShop:
        drawShopInterface()

        if mouseClicked:
            if shopFoodOne.is_hovering((mousePosX, mousePosY)):
                # Add food one to inventory and subtract currency
                print("Food One Purchased")
            elif shopFoodTwo.is_hovering((mousePosX, mousePosY)):
                # Add food two to inventory and subtract currency
                print("Food Two Purchased")
            elif shopFoodThree.is_hovering((mousePosX, mousePosY)):
                # Add food three to inventory and subtract currency
                print("Food Three Purchased")

    drawFishWindow()
    if feedingEnabled and mouseClicked:
        # Handle feeding logic if enabled
        if inventoryFoodOne.is_hovering((mousePosX, mousePosY)):
            # attach food to mouse cursor
            print("Fed with Food One")
        elif inventoryFoodTwo.is_hovering((mousePosX, mousePosY)):
            # attach food to mouse cursor
            print("Fed with Food Two")
        elif inventoryFoodThree.is_hovering((mousePosX, mousePosY)):
            # attach food to mouse cursor
            print("Fed with Food Three")
        
    # Top Layer of drawing frame
    drawConstantElements()  

    if shopButton.is_hovering((mousePosX, mousePosY)) and mouseClicked:
        toggleShopInterface()

    refreshButtons()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()