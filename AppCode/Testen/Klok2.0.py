
import pygame

from Testen.Functies_TestKlok import *


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
w = screen.width
h = screen.height


klokvlak = pygame.Surface((1280,720), pygame.SRCALPHA)
klokvlak.set_colorkey('black')



HighlightRect_width = 200
HighlightRect_height = 50
HighlightColor = pygame.Color(30,130,30,140)

highlight_rect = pygame.Rect(w/2-HighlightRect_width/2,h/2-HighlightRect_height/2,HighlightRect_width,HighlightRect_height)

Klok_font= pygame.Font(None,30)

Klok_uur = KlokScroll(klokvlak,0,highlight_rect,100,50,20,Klok_font)
Klok_min = KlokScroll(klokvlak,1,highlight_rect,100,50,20,Klok_font)

'''---------------------------------------------------------------------------------------------------------------'''
while running:
    screen.fill("white")
    klokvlak.fill("white")


    mouse = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_justpressed = pygame.mouse.get_just_pressed()


    pygame.draw.rect(klokvlak,HighlightColor,highlight_rect,0,10)
    
    
    UurSelect = Klok_uur.draw(mouse_justpressed,mouse,mouse_pos)
    MinSelect = Klok_min.draw(mouse_justpressed,mouse,mouse_pos)

    
    
    screen.blit(klokvlak,(0,0))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(60)  # limits FPS to 60

pygame.quit()



