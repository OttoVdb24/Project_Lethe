import pygame
import sys
import os
from Functies import *
import time
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
Font_PlanKop1 = pygame.font.Font(BlackFont,24)
Font_PlanKop2 = pygame.font.Font(RegularFont,18)
Font_KnopText = pygame.font.Font(BlackFont,16)
Font_Klok = pygame.font.Font(RegularFont,20)
Font_GeplandeActi = pygame.font.Font(BlackFont,16)
Font_Keyboard = pygame.font.Font(BlackFont,28)





# Grpahics__________________________________________________________________________________________________________________
GraphicsMap = os.path.join(basis,"Graphics")

Exit_img = pygame.image.load(os.path.join(GraphicsMap,"Exit_teken.png")).convert_alpha()
Exit_img = pygame.transform.scale_by(Exit_img, 0.03)

SymboolMap = os.path.join(GraphicsMap,"Symbolen")
def laad_symbool(map,bestand):
    return pygame.image.load(os.path.join(map, bestand)).convert_alpha()

Sym_voetbal = laad_symbool(SymboolMap,"Sym_Voetbal.png")
Sym_rugby = laad_symbool(SymboolMap,"Sym_Rugby.png")
Sym_volley = laad_symbool(SymboolMap,"Sym_Volley.png")
Sym_basket = laad_symbool(SymboolMap,"Sym_Basket.png")
Sym_andere = laad_symbool(SymboolMap,"Sym_Andere.png")
Sym_muziek = laad_symbool(SymboolMap,"Sym_Muziek.png")
Sym_zwemmen = laad_symbool(SymboolMap,"Zwemmen.svg")


BenodigdhedenMap = os.path.join(GraphicsMap,"Benodigdheden")
StreakMap = os.path.join(GraphicsMap,"Streak")
InkleurMap = os.path.join(GraphicsMap,"Inkleur")

Duikbril_kleur = laad_symbool(InkleurMap,"Duikbril_Kleur.png")
Duikbril_leeg = laad_symbool(InkleurMap,"Duikbril_Leeg.png")
Badmuts_kleur = laad_symbool(InkleurMap,"Badmuts_Kleur.png")
Badmuts_leeg = laad_symbool(InkleurMap,"Badmuts_Leeg.png")
Handdoek_kleur = laad_symbool(InkleurMap,"Handdoek_Kleur.png")
Handdoek_leeg = laad_symbool(InkleurMap,"Handdoek_Leeg.png")
Zwembroek_kleur = laad_symbool(InkleurMap,"Zwembroek_Kleur.png")
Zwembroek_leeg = laad_symbool(InkleurMap,"Zwembroek_Leeg.png")






#Algemene variabelen ----------------------------------------------------------------------------------------------
Annuleer_kleur = pygame.Color(120,120,120,60)
Bevestig_kleur = pygame.Color(180,220,180)
achtergrondKleur = pygame.Color(188,229,255)
buttonKleur = pygame.Color(10,10,10,20)
Fout_kleur = pygame.Color(241,98,113)
Overlay_alpha = 100
TekstKleur_licht = pygame.Color(255,255,255)
TekstKleur_donker = pygame.Color(10,10,10)
KeyboardColor = [(2,0,83),(18,38,133)]

#Surfaces_____________________________________________________________________________________________________________
buttonVlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
overlay = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
MeldingVlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
tekenVlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
KleurVlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)


for surface in (buttonVlak, overlay, MeldingVlak,tekenVlak,KleurVlak):
    surface.set_colorkey('green')
overlay.fill(achtergrondKleur)

# Data______________________________________________________________________________________________________________
#Lijst ["Titel", [Uur zak maken], [Uur vertrekken], [Benodigdheden],[Symbolen],Symbool activiteit]
Activiteit = ["Zwemmen",[0,9,3,0],[1,0,0,0],["Handdoek","Zwemboek","Badmuts","Duikbril"],[Handdoek_kleur,Zwembroek_kleur,Badmuts_kleur,Duikbril_kleur],[Handdoek_leeg,Zwembroek_leeg,Badmuts_leeg,Duikbril_leeg],Sym_zwemmen]


State = "Beginscherm"

#TITEL____________________________________________________________________________________________________________

    #Activiteit symbool
actiSymbool_width = 0.3*height
actiSymbool = pygame.transform.scale_by(Activiteit[6],(actiSymbool_width/Activiteit[6].width))
actiSymboolRect = pygame.Rect((screenRec.width-actiSymbool_width)/2,0.05*height, actiSymbool_width, actiSymbool.height)




titel_txt = Font_Titel.render(Activiteit[0],1,(255,255,255))
titelRect_width = titel_txt.get_width()
titelRect_height = titel_txt.get_height()
titelRect = pygame.Rect((screenRec.width-titelRect_width)/2,actiSymboolRect.bottom,
                        titelRect_width,titelRect_height)

#Melding______________________________________________________________________________________________________________
MeldingRect_width = 0.5*width
MeldingRect_height = 0.4*height
MeldingRect = pygame.Rect((screen.width-MeldingRect_width)/2,(screen.height-MeldingRect_height)/2,MeldingRect_width,MeldingRect_height)

#Knoppen_____________________________________________________________________________________________________________


buttonStatus = [0]*len(Activiteit[3])    #Status van alle benodigdheden knoppen
Nbenodigdheden = len(Activiteit[4])
Button_Y = 0.45*height
Breedte = width/(Nbenodigdheden+0.2*(Nbenodigdheden-1)+2*0.2)
X_spacing = 0.2*Breedte
randSpacing = 0.2*Breedte
BenodigdhedenRects = []
for i in range(Nbenodigdheden):
    X = randSpacing+ i*(Breedte+X_spacing)
    rect = pygame.Rect(X,Button_Y,Breedte,1*Breedte)
    BenodigdhedenRects.append(rect)
   
Kleurvakken = []

for i in range(Nbenodigdheden):
    KleurVak = inKleurButton(Activiteit[5][i], Activiteit[4][i],width,height, KleurVlak, tekenVlak,BenodigdhedenRects[i].centerx,BenodigdhedenRects[i].centery)
    Kleurvakken.append(KleurVak)






#Algemene knoppen________________________________________________________________________________________
meldingButton_width = 0.3*MeldingRect_width
meldingButton_heigt = 0.5*meldingButton_width
meldingJaButton = Button_Rechthoek(
    meldingButton_width, meldingButton_heigt, 0, Bevestig_kleur, MeldingVlak,
    MeldingRect.centerx- meldingButton_width -0.3*meldingButton_width,  
    MeldingRect.bottom - meldingButton_heigt,
    Font_Acti, 'white', "Ja"
)

meldingNeeButton = Button_Rechthoek(
    meldingButton_width, meldingButton_heigt, 0, Fout_kleur, MeldingVlak,
    MeldingRect.centerx + 0.3*meldingButton_width,                         # rechts van center
    MeldingRect.bottom - meldingButton_heigt,
    Font_Acti, 'white', "Nee"
)

AlgemeneExt_knop = Button(Exit_img,buttonVlak,(screen.get_width()-1.3*Exit_img.get_width()),0.3*Exit_img.get_height())



KlaaranimatieMap = os.path.join(GraphicsMap,"Animatie_succes")
Klaarframes = laad_frames(KlaaranimatieMap)
Klaaranimatie = LottieAnimatie(Klaarframes,1, fps=30)
"""
BalkanimatieMap = os.path.join(GraphicsMap,"Animatie_balk")
Balkframes = laad_frames(BalkanimatieMap)
Balkanimatie = LottieAnimatie(Balkframes,2,fps=30)
"""

klok = pygame.Clock()
startAnimatieTijd = 0
startdelayTijd = 0

#_______________________________________________________________________________________________________________________
#Game loop ____________________________________________________________________________________________________________
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for kleurvak in Kleurvakken:
            kleurvak.handle_event(event)  # ← muisbeweging vloeiend verwerken    


    screen.fill(achtergrondKleur)  # screen has no alpha
    for surface in (MeldingVlak, buttonVlak, KleurVlak):
        surface.fill((0, 0, 0, 0))  # proper transparent clear    
    mouse_pos = pygame.mouse.get_pos()
    mouse_justpressed = pygame.mouse.get_just_pressed()
    mouse_justpressed = mouse_justpressed[0]
    mouse = pygame.mouse.get_pressed()

    dt = klok.tick(60)




    if State == "Beginscherm":

        # Symbool en titel
        buttonVlak.blit(actiSymbool, actiSymboolRect.topleft)
        buttonVlak.blit(titel_txt, titelRect.topleft)

        #Knoppen 
        if AlgemeneExt_knop.draw(1, mouse, mouse_pos, mouse_justpressed):
            running = False
        """
        # Balk animatie tekenen
        Balkanimatie.update(dt)
        Balkanimatie_X = width-1.1*Balkanimatie.frames[Balkanimatie.huidig_frame].width
        Balkanimatie_Y = 0.75*height
        Balkanimatie.draw(buttonVlak, Balkanimatie_X, Balkanimatie_Y)

        # Klikdetectie op de balk animatie
        balk_rect = Balkanimatie.get_rect(Balkanimatie_X, Balkanimatie_Y)
        if mouse_justpressed and balk_rect.collidepoint(mouse_pos):
            Balkanimatie.toggle()
        """

        #Benodigdheden knoppen
        for i,rect in enumerate(BenodigdhedenRects):
            if Kleurvakken[i].klaar:
                buttonStatus[i]=True
                pygame.draw.rect(KleurVlak,(Bevestig_kleur),rect,0,20)
            else:
                pygame.draw.rect(KleurVlak,(120,120,120,60),rect,0,20)
            Kleurvakken[i].draw(mouse, mouse_pos)


            
            txt = Font_PlanKop1.render(Activiteit[3][i],1,(255,255,255))
            KleurVlak.blit(txt,(rect.centerx-txt.width/2,rect.bottom-txt.height))

        

        # Controle van de benodigdheden
        if buttonStatus == [True] * len(Activiteit[3]):
            if startdelayTijd==0:
                startdelayTijd=time.time()
            if time.time()-startdelayTijd >= 0.7:
                startdelayTijd = 0
                State = "Meldingscherm"

        screen.blit(buttonVlak, (0, 0))
        screen.blit(KleurVlak,(0,0))





    if State =="Meldingscherm":
        
        pygame.draw.rect(MeldingVlak,(120,120,120,90),MeldingRect,0,20)
        MeldingTitel = Font_PlanKop1.render("Zit alles in je zak?",1,'white')
        MeldingVlak.blit(MeldingTitel,(MeldingRect.centerx-MeldingTitel.width/2,1.1*MeldingRect.top))
        if meldingJaButton.draw(1,mouse,mouse_pos):
            State="Klaarscherm"
            Klaaranimatie.toggle()
            startAnimatieTijd = time.time()


        if meldingNeeButton.draw(1,mouse,mouse_pos):
            buttonStatus = [False]*len(Activiteit[3])
            State = 'Beginscherm'
        screen.blits([(overlay,(0,0)),(MeldingVlak,(0,0))])

        

    if State== "Klaarscherm":
        Klaaranimatie.update(dt)
        Klaaranimatie.draw(screen, width/2,height/2)
        if time.time()-startAnimatieTijd>8:
            running = False


    #ALGEMEEEN__________________________________________________________________________________________________________________________________


    pygame.display.flip()

