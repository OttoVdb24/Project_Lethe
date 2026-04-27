# Example file showing a basic pygame "game loop"
import pygame
import sys


# pygame setup
pygame.init()
info = pygame.display.Info()
if sys.platform == "linux":
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((0.8*info.current_w, 0.8*info.current_h))
    
width = screen.get_width()
height = screen.get_height()
screenRec = pygame.Rect(0,0,width,height)
clock = pygame.time.Clock()
running = True
Font = pygame.Font(None,40)
Font20 = pygame.Font(None,24)

Zak_txt = Font.render("Zak maak app",1,'white')
UnderConstruction_txt = Font20.render("UNDER CONSTRUCTION",1,(140,140,140))
Zak_rec = Zak_txt.get_rect(center = screenRec.center)
screen.blit(UnderConstruction_txt,(Zak_rec.centerx-UnderConstruction_txt.get_width()/2,Zak_rec.bottom))
screen.blit(Zak_txt,Zak_rec)


while running:









    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
