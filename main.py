import pygame
from button import Button # type : ignore

pygame.init()
screen = pygame.display.set_mode((1000, 720))
clock = pygame.time.Clock()
running = True

showShop = False # Flag to indicate if the shop interface is active

mouseClicked = False

itemBar = pygame.image.load("assets/item_bar.jpg")

def getMousePosition():
    global mousePosX, mousePosY
    mousePosX, mousePosY = pygame.mouse.get_pos()

def drawShopInterface():
    # Draw the shop interface background
    screen.fill("gray")

def drawFishWindow():
    # Draw the fish window background
    screen.fill("blue")
    pygame.Surface.blit(itemBar, screen, (0, 620))
    # Function calls for fish elements

def refreshButtons():
    global mouseClicked
    mouseClicked = False

button = Button(screen, "red", 1100, 600, 50)

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
        
    else:
        drawFishWindow()
        
    # Top Layer of drawing frame
    button.draw()

    if button.is_hovering((mousePosX, mousePosY)) and mouseClicked:
        showShop = not showShop

    refreshButtons()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()