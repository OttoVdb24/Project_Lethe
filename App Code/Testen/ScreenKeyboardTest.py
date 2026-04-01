import pygame
from Functies import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
keyboardvlak = pygame.Surface((1280,720))
clock = pygame.time.Clock()
running = True

Font_Keyboard = pygame.font.Font("Montserrat-Black.ttf",24)
KeyboardColor = ["orange","green"]

Touch_Down = False
Touch_Down_prev = False
Mouse_JustPressed = False


Text_dict = {"PlanText_Active": False, "NieuweActiText_active": False, "User_IP":""}



while running:

    mouse_pos = pygame.mouse.get_pos()

    Keyboard(keyboardvlak,Text_dict,Mouse_JustPressed,mouse_pos,Font_Keyboard,KeyboardColor)




    screen.blit(keyboardvlak,(0,0))







    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.FINGERDOWN:
            Touch_Down = True

        elif event.type == pygame.FINGERUP:
            Touch_Down = False                      #Laag plaatsten
    

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

        
    # Rising edge detectie
    Mouse_JustPressed = (Touch_Down and not Touch_Down_prev)

    # Update vorige state
    Touch_Down_prev = Touch_Down

pygame.quit()