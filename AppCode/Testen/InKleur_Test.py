import pygame
import sys
import os
import numpy
basis = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, basis)

from Functies import *
# pygame setup________________________________________________________________________________
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
#Surfaces_______________________________________________________________________________
buttonVlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
overlay = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
MeldingVlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
tekenVlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)

for surface in (buttonVlak, overlay, MeldingVlak,tekenVlak):
    surface.set_colorkey('green')
overlay.fill((0,0,0))


# Inputs________________________________________________________________________________
BlackFont = os.path.join(basis,"Fonts", "Montserrat-Black.ttf")
RegularFont = os.path.join(basis,"Fonts","Montserrat-Regular.ttf")

Font_Titel = pygame.font.Font(BlackFont,32)
Font_Txt = pygame.font.Font(BlackFont,16)



GraphicsMap = os.path.join(basis,"Graphics")
InkleurMap = os.path.join(GraphicsMap,"Inkleur")

def laad_symbool(map,bestand):
    return pygame.image.load(os.path.join(map, bestand)).convert_alpha()

Duikbril_kleur = laad_symbool(InkleurMap,"Duikbril_Kleur.png")
Duikbril_leeg = laad_symbool(InkleurMap,"Duikbril_Leeg.png")
Badmuts_kleur = laad_symbool(InkleurMap,"Badmuts_Kleur.png")
Badmuts_leeg = laad_symbool(InkleurMap,"Badmuts_Leeg.png")
Handdoek_kleur = laad_symbool(InkleurMap,"Handdoek_Kleur.png")
Handdoek_leeg = laad_symbool(InkleurMap,"Handdoek_Leeg.png")
Zwembroek_kleur = laad_symbool(InkleurMap,"Zwembroek_Kleur.png")
Zwembroek_leeg = laad_symbool(InkleurMap,"Zwembroek_Leeg.png")


SymboolMap = os.path.join(GraphicsMap,"Symbolen")

Sym_voetbal = laad_symbool(SymboolMap,"Sym_Voetbal.png")
Sym_rugby = laad_symbool(SymboolMap,"Sym_Rugby.png")
Sym_volley = laad_symbool(SymboolMap,"Sym_Volley.png")
Sym_basket = laad_symbool(SymboolMap,"Sym_Basket.png")
Sym_andere = laad_symbool(SymboolMap,"Sym_Andere.png")
Sym_muziek = laad_symbool(SymboolMap,"Sym_Muziek.png")
Sym_zwemmen = laad_symbool(SymboolMap,"Zwemmen.svg")



StreakMap = os.path.join(GraphicsMap,"Streak")





# Data______________________________________________________________________________________________________________
#Lijst ["Titel", [Uur zak maken], 2[Uur vertrekken], 3[Benodigdheden],4[Symbolen],5_Symbool activiteit]
Activiteit = ["Zwemmen",[0,9,3,0],[1,0,0,0],["Handdoek","Zwemboek","Badmuts","Duikbril"],[Handdoek_kleur,Zwembroek_kleur,Badmuts_kleur,Duikbril_kleur],[Handdoek_leeg,Zwembroek_leeg,Badmuts_leeg,Duikbril_leeg],Sym_zwemmen]

State = "Beginscherm"


Buttons = []
Nbenodigdheden = len(Activiteit[4])
Button_Y = 0.35*height
Breedte = width/(Nbenodigdheden+0.5*(Nbenodigdheden-1)+2*0.6)
X_spacing = 0.5*Breedte
randSpacing = 0.6*Breedte
Benodigdheden = []
for i in range(Nbenodigdheden):
    X = randSpacing+ i*(Breedte+X_spacing)
    rect = pygame.Rect(X,Button_Y,Breedte,1*Breedte)
    Benodigdheden.append(rect)
   


     
Kleurvakken = []

for i in range(Nbenodigdheden):
    KleurVak = inKleurButton(Activiteit[5][i], Activiteit[4][i],width,height, buttonVlak, tekenVlak,Benodigdheden[i].centerx,Benodigdheden[i].centery)
    Kleurvakken.append(KleurVak)






# GAMELOOP____________________________________________________________________________________
while running:
    mouse = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_justpressed = pygame.mouse.get_just_pressed()

    # ← events eerst verwerken, vóór draw
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for kleurvak in Kleurvakken:
            kleurvak.handle_event(event)  # ← muisbeweging vloeiend verwerken

    for i,rect in enumerate(Benodigdheden):
        pygame.draw.rect(buttonVlak,(120,120,120,60),rect,0,20)
        Kleurvakken[i].draw(mouse, mouse_pos)
        
        txt = Font_Txt.render(Activiteit[3][i],1,(255,255,255))
        buttonVlak.blit(txt,(rect.centerx-txt.width/2,rect.bottom-txt.height))

    screen.fill((0,240,240))
    screen.blit(buttonVlak,(0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()