# Example file showing a basic pygame "game loop"
import pygame
from Functies import *
from subprocess import call
pygame.init()
import os
import sys



basis = os.path.dirname(__file__)
c =CallPy()

info = pygame.display.Info()


if sys.platform == "linux":
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((0.8*info.current_w, 0.8*info.current_h))

width = screen.get_width()
height = screen.get_height()
screenRect = pygame.Rect(0,0,width,height)
clock = pygame.time.Clock()
running = True

#Algemeen________________________________________________
Actieve_Status = 'Hoofdscherm'
BlackFont = os.path.join(basis,"Fonts", "Montserrat-Black.ttf")
RegularFont = os.path.join(basis,"Fonts","Montserrat-Regular.ttf")

PlanningsApp = os.path.join(basis,"PlanningApp.py")
ZakMaakApp = os.path.join(basis,'ZakMaakApp.py')
OverzichtApp = os.path.join(basis,'OverzichtApp.py')

Apps = [OverzichtApp,ZakMaakApp,PlanningsApp]


#Fonts___________________________________________________
Font_Acti = pygame.font.Font(BlackFont,16)



#Afbeelding______________________________________________
GraphicsMap = os.path.join(basis,"Graphics")
Voetbalveld_img = pygame.image.load(os.path.join(GraphicsMap,"Voetbalveld_Vooraanzicht.png")).convert()
Voetbalveld_img = pygame.transform.scale(Voetbalveld_img,(screen.get_width(), screen.get_height()))

Achtergrond_Foto = Voetbalveld_img


#Surfaces________________________________________________
Achtergrondvlak = pygame.Surface((screen.get_width(),screen.get_height()))
Bovenvlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
overlay = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)

for surface in (Achtergrondvlak, Bovenvlak):
    surface.set_colorkey((10,10,10))

Achtergrondvlak.blit(Achtergrond_Foto,(0,0))
overlay.fill((0,0,0))
overlay.set_alpha(60)


#StartKnoppen___________________________________________
Knop_Titels = ["Week overzicht", "Zak maken", "Planning maken",]
Knop_width = width/(len(Knop_Titels)+1)
Knop_height = 0.5*Knop_width
Knop_gap = 0.01*width
Knop_startX = screenRect.centerx- (len(Knop_Titels)*Knop_width+ (len(Knop_Titels)-1) *Knop_gap)/2
Knop_color = pygame.Color(120,220,120,230)
Knoppen = []
Knop_Action =[]


for i in range(len(Knop_Titels)):
    Knop = Button_Rechthoek(Knop_width,Knop_height,0,Knop_color,Bovenvlak,Knop_startX + i*(Knop_width+Knop_gap),screenRect.centery-Knop_height/2,Font_Acti,(255,255,255),Knop_Titels[i])
    Knoppen.append(Knop)
    Knop.radius=40
    Knop_Action.append(False)










#________________________________________________________________________________________________________________________
while running:
    mouse = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    for surface in (Bovenvlak,):
        surface.fill((10,10,10))

    if Actieve_Status=="Hoofdscherm":
        for i,Knop in enumerate(Knoppen):
            if Knop.draw(1,mouse,mouse_pos):
                c.call_python_file(Apps[i])




            









#________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    for surface in (Achtergrondvlak, overlay,Bovenvlak):
        screen.blit(surface,(0,0))

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()