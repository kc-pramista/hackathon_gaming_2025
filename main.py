import pygame

from button import Button
from shop import Shop

pygame.init()
screen = pygame.display.set_mode((1000, 720))
clock = pygame.time.Clock()
running = True

showShop = False # Flag to indicate if the shop interface is active
feedingEnabled = True

mouseClicked = False

shopButton = Button(screen, "red", 900, 670, 30)

shopFoodOne = Button(screen, "green", 200, 200, 30)
shopFoodTwo = Button(screen, "green", 300, 200, 30)
shopFoodThree = Button(screen, "green", 400, 200, 30)

inventoryFoodOne = Button(screen, "yellow", 100, 670, 30)
inventoryFoodTwo = Button(screen, "yellow", 200, 670, 30)
inventoryFoodThree = Button(screen, "yellow", 300, 670, 30)

def getMousePosition():
    global mousePosX, mousePosY
    mousePosX, mousePosY = pygame.mouse.get_pos()

def drawShopInterface():
    # Draw the shop interface background
    screen.fill("gray")
    pygame.draw.rect(screen, "brown", (50 , 50, 900, 520))
    shopFoodOne.draw()
    shopFoodTwo.draw()
    shopFoodThree.draw()

def drawFishWindow():
    # Draw the fish window background
    screen.fill("blue")
    pygame.draw.rect(screen, "brown", (0, 620, 1000, 100))
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

    # Bottom Layer of drawing frame
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

    else:
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