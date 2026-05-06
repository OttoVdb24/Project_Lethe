# Example file showing a basic pygame "game loop"
import pygame
import sys
import os
from Functies import *
import math

basis = os.path.dirname(__file__)

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


#Fonts_____________________________________________________________________________________________________
BlackFont = os.path.join(basis,"Fonts", "Montserrat-Black.ttf")
RegularFont = os.path.join(basis,"Fonts","Montserrat-Regular.ttf")

Font_Titel = pygame.font.Font(BlackFont,32)
Font_Acti = pygame.font.Font(BlackFont,16)
Font_PlanTitel = pygame.font.Font(RegularFont,30)
Font_PlanKop1 = pygame.font.Font(BlackFont,20)
Font_PlanKop2 = pygame.font.Font(RegularFont,18)
Font_KnopText = pygame.font.Font(BlackFont,16)
Font_Klok = pygame.font.Font(RegularFont,20)
Font_GeplandeActi = pygame.font.Font(BlackFont,16)
Font_Keyboard = pygame.font.Font(BlackFont,28)





# Grpahics__________________________________________________________________________________________________________________
GraphicsMap = os.path.join(basis,"Graphics")

Exit_img = pygame.image.load(os.path.join(GraphicsMap,"Exit_teken.png")).convert_alpha()
Exit_img = pygame.transform.scale_by(Exit_img, 0.03)

Map = os.path.join(GraphicsMap,"Symbolen")
def laad_symbool(map,bestand):
    return pygame.image.load(os.path.join(map, bestand)).convert_alpha()

Sym_voetbal = laad_symbool(Map,"Sym_Voetbal.png")
Sym_rugby = laad_symbool(Map,"Sym_Rugby.png")
Sym_volley = laad_symbool(Map,"Sym_Volley.png")
Sym_basket = laad_symbool(Map,"Sym_Basket.png")
Sym_andere = laad_symbool(Map,"Sym_Andere.png")
Sym_muziek = laad_symbool(Map,"Sym_Muziek.png")
Sym_zwemmen = laad_symbool(Map,"Zwemmen.svg")


Map = os.path.join(GraphicsMap,"Benodigdheden")

Sym_Handdoek = laad_symbool(Map,"Handdoek.svg")
Sym_Badmuts = laad_symbool(Map,"Badmuts.svg")
Sym_Zwembril = laad_symbool(Map,"Zwembril.svg")
Sym_zwembroek = laad_symbool(Map,"Zwembroek.svg")




#Algemene variabelen ----------------------------------------------------------------------------------------------
Annuleer_kleur = pygame.Color(120,120,120,60)
Bevestig_kleur = pygame.Color(180,220,180)
achtergrondKleur = pygame.Color(188,229,255)
buttonKleur = pygame.Color(10,10,10,20)

Overlay_alpha = 100
TekstKleur_licht = pygame.Color(255,255,255)
TekstKleur_donker = pygame.Color(10,10,10)
KeyboardColor = [(2,0,83),(18,38,133)]

#Surfaces_____________________________________________________________________________________________________________
buttonVlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
overlay = pygame.Surface((screen.get_width(),screen.get_height()))
MeldingVlak = pygame.Surface((screen.get_width(),screen.get_height()))

for surface in (buttonVlak, overlay, MeldingVlak):
    surface.set_colorkey(achtergrondKleur)


# Data______________________________________________________________________________________________________________
#Lijst ["Titel", [Uur zak maken], [Uur vertrekken], [Benodigdheden],[Symbolen],Symbool activiteit]
Activiteit = ["Zwemmen",[0,9,3,0],[1,0,0,0],["Handdoek","Badmuts", "Zwembril","Zwembroek"],[Sym_Handdoek,Sym_Badmuts,Sym_Zwembril,Sym_zwembroek],Sym_zwemmen]


State = "Beginscherm"

# Scherm Layout____________________________________________________________________________________________________

    #Activiteit symbool
actiSymbool_width = 0.3*height
actiSymbool = pygame.transform.scale_by(Activiteit[5],(actiSymbool_width/Activiteit[5].width))
actiSymboolRect = pygame.Rect((screenRec.width-actiSymbool_width)/2,0.05*height, actiSymbool_width, actiSymbool.height)




titel_txt = Font_Titel.render(Activiteit[0],1,(255,255,255))
titelRect_width = titel_txt.get_width()
titelRect_height = titel_txt.get_height()
titelRect = pygame.Rect((screenRec.width-titelRect_width)/2,actiSymboolRect.bottom,
                        titelRect_width,titelRect_height)

#Knoppen_____________________________________________________________________________________________________________

benodigdhedenButtons = maakBenodigdhedenButtons(
    Activiteit, buttonVlak, width, height, Font_PlanKop1, buttonKleur, titelRect.bottom
)


#Game loop ____________________________________________________________________________________________________________
while running:
    for surface in (screen, buttonVlak,MeldingVlak):
        surface.fill(achtergrondKleur)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_justpressed = pygame.mouse.get_just_pressed()
    mouse_justpressed = mouse_justpressed[0]



    if State == "Beginscherm":
        #Symbool en titel 
        buttonVlak.blit(actiSymbool,actiSymboolRect.topleft)

        buttonVlak.blit(titel_txt,titelRect.topleft)
        for button in benodigdhedenButtons:
            button.draw(mouse_pos,mouse_justpressed)


        # Blitten naar screen
        screen.blit(buttonVlak,(0,0))
    










    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
