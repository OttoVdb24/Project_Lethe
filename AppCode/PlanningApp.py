import pygame
from Functies import *
import os
import sys


basis = os.path.dirname(__file__)


pygame.init()

Mouse_JustPressed = False
Actieve_Status = 'Hoofdscherm'

#Lettertypes aanmaken __________________________________________________________________________________________________

BlackFont = os.path.join(basis,"Fonts", "Montserrat-Black.ttf")
RegularFont = os.path.join(basis,"Fonts","Montserrat-Regular.ttf")


Font_Dagen = pygame.font.Font(BlackFont,24)
Font_Acti = pygame.font.Font(BlackFont,16)
Font_PlanTitel = pygame.font.Font(RegularFont,30)
Font_PlanKop1 = pygame.font.Font(RegularFont,20)
Font_PlanKop2 = pygame.font.Font(RegularFont,18)
Font_KnopText = pygame.font.Font(BlackFont,16)
Font_Klok = pygame.font.Font(RegularFont,20)
Font_GeplandeActi = pygame.font.Font(BlackFont,18)
Font_Keyboard = pygame.font.Font(BlackFont,28)


info = pygame.display.Info()
if sys.platform == "linux":
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((0.8*info.current_w, 0.8*info.current_h))

width = screen.get_width()
height = screen.get_height()

clock = pygame.time.Clock()
running = True


overlay = pygame.Surface((screen.get_width(),screen.get_height()))
overlay.set_alpha(0)  # 0 = volledig transparant, 255 = volledig ondoorzichtig
overlay.fill((0, 0, 0))  # zwarte overlay


#Graphics Importeren____________________________________________________________________________________________________
GraphicsMap = os.path.join(basis,"Graphics")

Exit_img = pygame.image.load(os.path.join(GraphicsMap,"Exit_teken.png")).convert_alpha()
Exit_img = pygame.transform.scale_by(Exit_img, 0.03)
Voetbalveld_img = pygame.image.load(os.path.join(GraphicsMap,"Voetbalveld_Vooraanzicht.png")).convert()
Voetbalveld_img = pygame.transform.scale(Voetbalveld_img,(screen.get_width(), screen.get_height()))
Ballet_img = pygame.image.load(os.path.join(GraphicsMap,"Balletzaal.png")).convert()
Ballet_img = pygame.transform.scale(Ballet_img,(screen.get_width(), screen.get_height()))
AchtergrondFoto = Voetbalveld_img

SymbolenMap = os.path.join(GraphicsMap,"Symbolen")
def laad_symbool(bestand):
    return pygame.image.load(os.path.join(SymbolenMap, bestand)).convert_alpha()

Sym_voetbal = laad_symbool("Sym_Voetbal.png")
Sym_rugby = laad_symbool("Sym_Rugby.png")
Sym_volley = laad_symbool("Sym_Volley.png")
Sym_basket = laad_symbool("Sym_Basket.png")
Sym_andere = laad_symbool("Sym_Andere.png")
Sym_muziek = laad_symbool("Sym_Muziek.png")
Sym_zwemmen = laad_symbool("Sym_Zwemmen.png")


Sym_voetbal = pygame.transform.scale_by(Sym_voetbal,0.8)
Sym_rugby = pygame.transform.scale_by(Sym_rugby,0.8)
Sym_volley = pygame.transform.scale_by(Sym_volley,0.8)
Sym_basket = pygame.transform.scale_by(Sym_basket,0.8)
Sym_andere = pygame.transform.scale_by(Sym_andere,0.8)
Sym_muziek = pygame.transform.scale_by(Sym_muziek,0.8)
Sym_zwemmen = pygame.transform.scale_by(Sym_zwemmen,0.8)





#Algemene variabelen ----------------------------------------------------------------------------------------------
Annuleer_kleur = pygame.Color(120,120,120,60)
Bevestig_kleur = pygame.Color(180,220,180)
Achtergrond_kleur = pygame.Color(235,241,248)
Overlay_alpha = 100
TekstKleur_licht = pygame.Color(255,255,255)
TekstKleur_donker = pygame.Color(10,10,10)
KeyboardColor = [(2,0,83),(18,38,133)]


StandaardActiviteiten = []
StandaardActiviteiten.append([0,"Voetballen",[0,9,3,0],[1,8,0,0],["Drinkbus"], (220,100,100,60),Sym_voetbal])
StandaardActiviteiten.append([2,"Zwemmen",[1,0,3,0],[1,4,0,0],["Zwembril","Handdoek"],(220,100,100,60),Sym_zwemmen])
StandaardActiviteiten.append([2,"Muziek",[1,0,3,0],[1,4,0,0],["Klokkenspel"],(220,100,100,60),Sym_muziek])
StandaardActiviteiten.append([3,"Andere",[1,6,0,0],[1,8,0,0],[],(220,150,180,60),Sym_andere])




#Surfaces maken_______________________________________________________________________________________________________
bovenvlak = pygame.Surface((screen.get_width(),screen.get_height()))
ondervlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
sleepvlak = pygame.Surface((screen.get_width(),screen.get_height()))
planningvlak = pygame.Surface((screen.get_width(),screen.get_height()))
planRechthoeken = pygame.Surface((screen.get_width(),screen.get_height()))
nieuweActivlak = pygame.Surface((screen.get_width(),screen.get_height()))
deletevlak = pygame.Surface((screen.get_width(),screen.get_height()))
keyboardvlak = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
klokvlak =  pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)


for surface in (bovenvlak,ondervlak,sleepvlak,planningvlak,klokvlak,planRechthoeken,nieuweActivlak,deletevlak,keyboardvlak):
    surface.set_colorkey((10,10,10))



#Dagkollommen variabelen____________________________________________________________________________________________
DagRect_Width = 0.124*screen.get_width()
DagRect_Height = 350
DagRect_Gap = 0.01*screen.get_width()
DagRects = []
Dagen= ["MA","DI","WOE","DO","VR","ZA","ZO"]
DagRect_collision = [False]*7
DagRect_Color = [(240,240,240,120),(200,200,255,120)]
Agenda_lst=[False,0]


#Activiteit variabelen________________________________________________________________________________________________

PlanActiviteit =[]
GeplandeActiviteiten = []
Dagen_Tellen = [0]*7


ActiRect_Width = 0.13*screen.get_width()
ActiRect_Height = 0.7*ActiRect_Width
ActiRect_Gap = 00.003*screen.get_width()
ActiRects =[]
ActiRect_Pos_x=[]
ActiRect_Pos_y =[]
ActiRect_Slepen =[]
ActiRect_Offset_x =[]
ActiRect_Offset_y =[]
Actis = ["Zwemmen","Lopen","Tekenacademie", "Schooltas"]
Titel = "0"
N_ActiH = len(StandaardActiviteiten)
N_ActiV =1

for j in range(N_ActiV):
    for i in range(N_ActiH):
        ActiRect_Pos_x.append(screen.get_width()/2-(N_ActiH/2*ActiRect_Width+(N_ActiH-1)/2*ActiRect_Gap)+i*(ActiRect_Width+ActiRect_Gap))
        ActiRect_Pos_y.append(40+ j*(ActiRect_Height + ActiRect_Gap))
        ActiRect_Slepen.append(False)
        ActiRect_Offset_x.append(0)
        ActiRect_Offset_y.append(0)
ActiRect_StartPos_x = ActiRect_Pos_x.copy()
ActiRect_StartPos_Y = ActiRect_Pos_y.copy()




#Planningsscherm variabele________________________________________________________________________________________________

PlanRect_Width = 0.7*screen.get_width()
PlanRect_Height = 0.85*screen.get_height()
PlanRect_Color = Achtergrond_kleur
PlanRect_TitelColor = (20,20,20)
PlanExt_knop = Button(Exit_img,planningvlak,(screen.get_width()/2+PlanRect_Width/2-Exit_img.get_width())-20,screen.get_height()-PlanRect_Height+20)
PlanExt_knop_b = False
PlanKop_Offset = 15

PlanRect = pygame.Rect(screen.get_width()/2-PlanRect_Width/2,screen.get_height()-PlanRect_Height,PlanRect_Width,PlanRect_Height)
Plan_Linkerrand = PlanRect.left+20 
PlanningLoop = False

#Hulp rechthoeken
PlanRect1 = pygame.Rect(Plan_Linkerrand,PlanRect.top,2*(PlanRect.centerx-Plan_Linkerrand),90)
#pygame.draw.rect(planningvlak,('black'),PlanRect1)
PlanRect2 = pygame.Rect(Plan_Linkerrand,PlanRect1.bottom+PlanKop_Offset,1*(PlanRect.centerx-Plan_Linkerrand),(height-(PlanRect1.bottom+PlanKop_Offset)))
#pygame.draw.rect(planningvlak,('red'),PlanRect2)
PlanRect2_1 = pygame.Rect(Plan_Linkerrand,PlanRect2.top,PlanRect2.width,PlanRect2.height/2)
#pygame.draw.rect(planningvlak,('green'),PlanRect2_1)
PlanRect2_2 = pygame.Rect(Plan_Linkerrand,PlanRect2.centery,PlanRect2.width,PlanRect2.height/2)
#pygame.draw.rect(planningvlak,('blue'),PlanRect2_2)

PlanRect3 = pygame.Rect(PlanRect.centerx+20,PlanRect2.top,(PlanRect.centerx-Plan_Linkerrand),280)
PlanRect3_1 = pygame.Rect(PlanRect3.left,PlanRect3.top+60,(PlanRect.centerx-Plan_Linkerrand),260)

PlanBevestig_Knop_width = 0.3*PlanRect.width
PlanBevestig_Knop = Button_Rechthoek(PlanBevestig_Knop_width,0.3*PlanBevestig_Knop_width,0, Bevestig_kleur,planningvlak,PlanRect3.centerx-PlanRect.width/8,
                                     PlanRect.bottom-0.35*PlanBevestig_Knop_width - 10,Font_KnopText,TekstKleur_licht,'Bevestigen')

PlanBox1 = PlanBox(planningvlak,PlanRect3_1,'black',1,(0.07*PlanRect.height)) #Initieren van planboxen, zal dan in de running het aantal bepalen

# Text input_______________________________________________________________________________________________________________________
Text_dict = {"PlanText_Active": False, "NieuweActiText_active": False, "User_IP":""}

#Nieuwe Activiteit naam ______________________________________

NieuweActi_Plannen =False #Bool die toestand van het plannen toont, Altijd laag, wanneer er op de nieuwe acti knop wordt geduuwd zal deze hoog worden. Hierbij komt het nieuwe Acti scherm tevoorschijn.

NieuweActiRect_width = 0.6*screen.get_width()
NieuweActiRect_height = 0.6*screen.get_height()
NieuweActiRect_Pos = (nieuweActivlak.get_width()/2-NieuweActiRect_width/2,nieuweActivlak.get_height()/2-NieuweActiRect_height/2)
NieuweActiRect = pygame.Rect(NieuweActiRect_Pos[0],NieuweActiRect_Pos[1],NieuweActiRect_width,NieuweActiRect_height)
NieuweActiRect_color = Achtergrond_kleur

#Knoppen
NieuweActiExt_knop = Button(Exit_img,nieuweActivlak, NieuweActiRect.right-Exit_img.get_width()-20, NieuweActiRect.top+20)


NieuweActiBevestig_knop = Button_Rechthoek(NieuweActiRect.width*0.3,0.09*NieuweActiRect_width,0,Bevestig_kleur,nieuweActivlak,
                                           NieuweActiRect.centerx-NieuweActiRect.width*0.15,NieuweActiRect.bottom-0.1*NieuweActiRect_width,Font_KnopText,TekstKleur_licht,'Bevestigen')


NieuweActiInput_Rect_Width = 0.6*NieuweActiRect_width
NieuweActiInput_Rect_Height = 55
NieuweActiInput_Rect = pygame.Rect(NieuweActiRect.centerx-NieuweActiInput_Rect_Width/2,NieuweActiRect.centery-NieuweActiInput_Rect_Height/2,NieuweActiInput_Rect_Width,NieuweActiInput_Rect_Height)
NieuweActiInput_Text = "Typ hier ..."

#Keyboard variabelen_______________________________________________________________________________________________________________
TextRect_width = width*0.4
TextRect_height = height*0.1
TextRect = pygame.Rect(width/2-TextRect_width/2, height*0.15, TextRect_width,TextRect_height)

Keyboard_Klaar = Button_Rechthoek(0.1*width,TextRect.height,0,Bevestig_kleur,keyboardvlak,TextRect.right,TextRect.top,Font_KnopText,TekstKleur_licht,"Klaar")
Keyboard_Annuleer = Button_Rechthoek(0.1*width,TextRect.height,0,Annuleer_kleur,keyboardvlak,TextRect.left-0.1*width,TextRect.top,Font_KnopText,TekstKleur_licht,"Annuleer")

#Klok Scroll____________________________________________________________________________________________________________________________
HighlightRect_width = PlanRect2.width*0.65
HighlightRect_height = PlanRect2_1.height*0.15


HighlightRect1 = pygame.Rect(1.1*PlanRect2_1.left, PlanRect2_1.centery-HighlightRect_height*0,
                             HighlightRect_width,HighlightRect_height)


Klok1_U = KlokScroll(planningvlak,0,HighlightRect1,50,20,20,Font_Klok)
Klok1_M = KlokScroll(planningvlak,1,HighlightRect1,50,20,20,Font_Klok)

HighlightRect2 = pygame.Rect(1.1*PlanRect2_2.left, PlanRect2_2.centery-HighlightRect_height*0,
                             HighlightRect_width,HighlightRect_height)


Klok2_U = KlokScroll(planningvlak,0,HighlightRect2,50,20,20,Font_Klok)
Klok2_M = KlokScroll(planningvlak,1,HighlightRect2,50,20,20,Font_Klok)

#Kleur kiezer_______________________________________________________________________________________________________________
Kleur_kiezerButton = pygame.Rect(PlanRect3.left, PlanExt_knop.rect.top,Exit_img.width,Exit_img.height)

KleurKiezerActive = False

KleurKiezerRect_width = 0.9*PlanRect3_1.width
KleurkiezerRect_height = 0.4 * PlanRect.height

KleurkiezerRect = pygame.Rect(
    PlanRect3_1.left,
    PlanRect3.top,
    KleurKiezerRect_width,
    KleurkiezerRect_height
)

# Grid instellingen
cols = 3
rows = 2

# Grootte van vierkanten (past zich aan zodat alles netjes blijft)
KleurRect_side = min(
    KleurkiezerRect.width / (cols + 1),
    KleurkiezerRect.height / (rows + 1)
)

# Automatische spacing
spacing_x = (KleurkiezerRect.width - cols * KleurRect_side) / (cols + 1)
spacing_y = (KleurkiezerRect.height - rows * KleurRect_side) / (rows + 1)

# Rects maken
KleurRects = []

for i in range(rows):
    for j in range(cols):
        x = KleurkiezerRect.left + spacing_x + j * (KleurRect_side + spacing_x)
        y = KleurkiezerRect.top + spacing_y + i * (KleurRect_side + spacing_y)

        rect = pygame.Rect(x, y, KleurRect_side, KleurRect_side)
        KleurRects.append(rect)

#Beveiligingsscherm-------------------------------------------------------------


preMouse = False

#___________________________________________________________________________________________________________________________
while running:



    for surface in ( sleepvlak, bovenvlak, ondervlak,planningvlak,klokvlak,planRechthoeken, nieuweActivlak,deletevlak, keyboardvlak):
        surface.fill((10,10,10))

    #Achtergrond vullen
    screen.blit(AchtergrondFoto,(0,0))

    #Muis positie, klik en net geklikked aanmaken
    Mouse_Pos = pygame.mouse.get_pos()
    Mouse = pygame.mouse.get_pressed()
    Time = pygame.time.get_ticks()

    if Mouse[0] and not preMouse:
        Mouse_JustPressed=True
        
    elif Mouse[0] and preMouse:
        Mouse_JustPressed=False
    elif not Mouse[0] and preMouse:
        Mouse_JustPressed=False 
    
    preMouse = Mouse[0]

    
    
    #Sleepbare rechthoeken maken
    if BovenRechthoeken(ActiRect_Pos_x,ActiRect_Pos_y,ActiRect_Width,ActiRect_Height,Mouse,Mouse_Pos,Mouse_JustPressed,ActiRect_Slepen,ActiRect_Offset_x,ActiRect_Offset_y,sleepvlak,bovenvlak,ActiRect_StartPos_x,ActiRect_StartPos_Y,Font_Acti,StandaardActiviteiten,Actieve_Status) and Actieve_Status=="Hoofdscherm":
        Actieve_Status = "NieuweActiviteit_Maken"


    #Nieuwe Activiteit maken
    if Actieve_Status == "NieuweActiviteit_Maken":
        NieuweActiviteit_maken(NieuweActiInput_Rect, Mouse_Pos, Mouse_JustPressed, Text_dict,overlay,nieuweActivlak,NieuweActiRect_color,NieuweActiRect,Font_PlanKop1,Font_KnopText, NieuweActiInput_Text,Time)
        if Text_dict["User_IP"]=="":
            NieuweActiBevestig_knop.color= Annuleer_kleur
        else:
            NieuweActiBevestig_knop.color = Bevestig_kleur

        if not Text_dict["NieuweActiText_active"]:
         
            #Exit voorwaarde maken
            if NieuweActiExt_knop.draw(1,Mouse,Mouse_Pos,Mouse_JustPressed):
                Actieve_Status = "Hoofdscherm"
                DagRect_collision = [False]*7
                overlay.set_alpha(0)
            
            #Bevestigknop 
            
            if NieuweActiBevestig_knop.draw(1,Mouse,Mouse_Pos):
                Actieve_Status = "Hoofdscherm"
                Actieve_Status = "Planning"
        






    #Dag rechthoeken maken
    OnderkantFunctie(screen, ondervlak,DagRect_Width,DagRect_Gap,DagRect_Height,Mouse_Pos,Font_Dagen,Dagen,DagRects,DagRect_Color,DagRect_collision)

    
    #Collision code ActiRect en DagRect
    if any(ActiRect_Slepen):
        for i, rect in enumerate(DagRects):
            DagRect_collision[i]= rect.collidepoint(Mouse_Pos)
    

    elif any(DagRect_collision):      #and PlanningTrigger==False: #Elif want de user moet losgelaten hebben

        if PlanActiviteit[1] == "Andere":   #Wanneer de andere geslepen werd.
            Actieve_Status = "NieuweActiviteit_Maken"      
        
        else: #Planning openen 
            Actieve_Status = "Planning"



        #Actieve Planactiviteit maken
    if (any(ActiRect_Slepen)):
        PlanActiviteit = StandaardActiviteiten[ActiRect_Slepen.index(True)].copy()

    #Planning window
    if Actieve_Status == "Planning" :
        if not PlanningLoop:
            PlanningLoop = True
            PlanBox1.Actief = [False]*len(PlanActiviteit[4])
        
        if PlanExt_knop_b and not KleurKiezerActive: 
            DagRect_collision = [False]*7 #HardCoded, er zullen altijd 7 dagen zijn vriendje :)
            overlay.set_alpha(0)
            PlanningLoop = False
            Actieve_Status = "Hoofdscherm"



        PlanExt_knop_b, KleurKiezerActive = Planningsscherm(overlay,planningvlak,PlanRect_Color,PlanRect,Font_PlanTitel,PlanRect_TitelColor,PlanRect1,Font_PlanKop1,Font_PlanKop2,PlanRect2_1,
                                                PlanRect2_2,PlanRect3,Mouse,Mouse_Pos,Mouse_JustPressed,PlanBox1,PlanActiviteit,
                                                Text_dict,Time,HighlightRect1,Klok1_U,Klok1_M,HighlightRect2,Klok2_U,Klok2_M,klokvlak, 
                                                KleurRects, KleurKiezerActive,KleurkiezerRect,PlanExt_knop,Kleur_kiezerButton)






        if not Text_dict["PlanText_Active"]:

            #Lijst van benodigdheden maken 
            ActieveBenodigdheden = list(zip(PlanActiviteit[4],PlanBox1.Actief))
            ActieveBenodigdheden = [s for s, a in ActieveBenodigdheden if a]

            #Bevestigingsknop maken en uitlezen. Ook nieuwe activiteit toevoegen aan geplande activiteiten lijst
            if PlanBevestig_Knop.draw(1,Mouse,Mouse_Pos):   
                GeplandeActiviteiten.append([len(GeplandeActiviteiten), PlanActiviteit[1],[800],[800],ActieveBenodigdheden,DagRect_collision.index(True),PlanActiviteit[5], PlanActiviteit[6]])
                print(GeplandeActiviteiten)
                
                DagRect_collision = [False]*7 #HardCoded, er zullen altijd 7 dagen zijn vriendje :)
                Actieve_Status = "Hoofdscherm"
                overlay.set_alpha(0)
                PlanningLoop = False
                Actieve_Status = "Hoofdscherm"


    if Actieve_Status == "DeleteMelding":
        Delete_lst = DeleteMelding(deletevlak,overlay,Font_PlanKop1, Font_KnopText,Mouse,Mouse_Pos,Mouse_JustPressed,Bevestig_kleur,Exit_img,Annuleer_kleur)

        if Delete_lst[0]:
            Actieve_Status ="Hoofdscherm"
            overlay.set_alpha(0)
            Agenda_lst[0]=False

        elif Delete_lst[1]:
            overlay.set_alpha(0)
            Actieve_Status ="Hoofdscherm"
            GeplandeActiviteiten.pop(Agenda_lst[1])
            Agenda_lst[0]=False





    #Agenda activiteiten opzetten
    if Actieve_Status =="BeveiligingScherm":
        Beveiliging_return = Beveiliging(deletevlak,overlay,Font_PlanKop1, Font_PlanKop2, Font_KnopText,Mouse,Mouse_Pos,Mouse_JustPressed,Bevestig_kleur,Exit_img)
        if Beveiliging_return == "Correct":
            Actieve_Status = "DeleteMelding"
        elif Beveiliging_return == "Exit":
            Actieve_Status = "Hoofdscherm"
            Agenda_lst[0]=False


        
    Agenda_lst = AgendaRechthoeken(GeplandeActiviteiten,DagRects,DagRect_Width,planRechthoeken,Font_GeplandeActi,Mouse_JustPressed,Mouse_Pos,Agenda_lst)


    if Agenda_lst[0] and Actieve_Status =="Hoofdscherm":
        Actieve_Status ="BeveiligingScherm"



        
   





#_______________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________________________

    #Alle surfaces op screen zetten, volgorde belangrijk. overlay boven alles behalve planningvlak
    for surface in (ondervlak,planRechthoeken, bovenvlak, sleepvlak,overlay,planningvlak,klokvlak,nieuweActivlak,deletevlak):
        screen.blit(surface,(0,0))



    clock.tick(60)  # limits FPS to 60

    #Text verzenden wanneer op de plus geduuwd wordt
    if Text_dict["PlanText_Active"]:
        TextInputscherm(keyboardvlak,Font_PlanKop1,Text_dict,TextRect,Time)
        Keyboard(keyboardvlak,Text_dict,Mouse_JustPressed,Mouse_Pos,Font_Keyboard,KeyboardColor)
        overlay.fill((255,255,255))
        overlay.set_alpha(30)
        planningvlak.set_alpha(20)
        bovenvlak.set_alpha(20)
        ondervlak.set_alpha(0)

        if Keyboard_Klaar.draw(1,Mouse,Mouse_Pos):
            if Text_dict["User_IP"].strip() != "":
                PlanActiviteit[4].append(Text_dict["User_IP"])
                PlanBox1.Actief.append(True)
            # Reset text parameters
            Text_dict["PlanText_Active"] = False
            Text_dict["User_IP"] = ""
 
        elif Keyboard_Annuleer.draw(1,Mouse,Mouse_Pos):
            Text_dict["PlanText_Active"] = False
            Text_dict["User_IP"]=""

        screen.blit(overlay,(0,0))
        screen.blit(keyboardvlak,(0,0))


    elif Text_dict["NieuweActiText_active"]:
        TextInputscherm(keyboardvlak,Font_PlanKop1,Text_dict,TextRect,Time)
        Keyboard(keyboardvlak,Text_dict,Mouse_JustPressed,Mouse_Pos,Font_Keyboard,KeyboardColor)
        overlay.fill((100,100,100))
        overlay.set_alpha(30)
        nieuweActivlak.set_alpha(20)
        bovenvlak.set_alpha(20)
        ondervlak.set_alpha(0)

        if Keyboard_Klaar.draw(1,Mouse,Mouse_Pos):

            # Reset text parameters
            Text_dict["NieuweActiText_active"] = False
         
        elif Keyboard_Annuleer.draw(1,Mouse,Mouse_Pos):
            Text_dict["NieuweActiText_active"] = False
            Text_dict["User_IP"]=""
            

        screen.blit(overlay,(0,0))
        screen.blit(keyboardvlak,(0,0))

        
    

    else:
        overlay.fill((0,0,0))
        overlay.set_alpha(0)
        planningvlak.set_alpha(255)
        nieuweActivlak.set_alpha(255)
        bovenvlak.set_alpha(255)
        ondervlak.set_alpha(255)
        klokvlak.set_alpha(255)

    if not Text_dict["NieuweActiText_active"]:  
        if Mouse_JustPressed and NieuweActiBevestig_knop.rect.collidepoint(Mouse_Pos):

            if Text_dict["User_IP"].strip() != "":
                PlanActiviteit[1] = (Text_dict["User_IP"])
                

            # Reset text parameters
            Text_dict["NieuweActiText_active"] = False
            Text_dict["User_IP"] = ""
            NieuweActiInput_Text="Typ hier..."


        elif Mouse_JustPressed and  NieuweActiExt_knop.rect.collidepoint(Mouse_Pos):
            Text_dict["NieuweActiText_active"] = False
            Text_dict["User_IP"] = ""
            NieuweActiInput_Text="Typ hier..."



    for event in pygame.event.get():
        #Pygame aflsuiten
        if event.type == pygame.QUIT:
            running = False

        
        elif event.type == pygame.FINGERDOWN:
            Touch_Down = True

        elif event.type == pygame.FINGERUP:
            Touch_Down = False                      #Laag plaatsten


        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # ALLES opnieuw maken
            bovenvlak = pygame.Surface((event.w, event.h))
            ondervlak = pygame.Surface((event.w, event.h), pygame.SRCALPHA)
            sleepvlak = pygame.Surface((event.w,event.h))
            planningvlak = pygame.Surface((event.w,event.h))
            planRechthoeken = pygame.Surface((event.w,event.h))
            nieuweActivlak = pygame.Surface((event.w,event.h))
            deletevlak = pygame.Surface((event.w,event.h))
            keyboardvlak = pygame.Surface((event.w,event.h))
            for surface in (bovenvlak,ondervlak,sleepvlak,planningvlak,planRechthoeken,nieuweActivlak,deletevlak,keyboardvlak):
                surface.set_colorkey((10,10,10))
            
            ActiRect_Pos_x.clear()
            ActiRect_Pos_y.clear()
            for j in range(N_ActiV):
                for i in range(N_ActiH):

                    ActiRect_Pos_x.append(screen.get_width()/2-(N_ActiH/2*ActiRect_Width+(N_ActiH-1)/2*ActiRect_Gap)+i*(ActiRect_Width+ActiRect_Gap))
                    ActiRect_Pos_y.append(40+ j*(ActiRect_Height + ActiRect_Gap))
            ActiRect_StartPos_x = ActiRect_Pos_x.copy()
            ActiRect_StartPos_Y = ActiRect_Pos_y.copy()




            Voetbalveld_img = pygame.transform.scale(Voetbalveld_img,(screen.get_width(), screen.get_height()))

        
        #Alles Text gebaseerd

        if (Text_dict["PlanText_Active"] or Text_dict["NieuweActiText_active"]) and event.type == pygame.KEYDOWN:
            pygame.key.start_text_input()

            if event.key == pygame.K_BACKSPACE:
                Text_dict["User_IP"] = Text_dict["User_IP"][:-1]

            elif event.key != pygame.K_RETURN:
                    Text_dict["User_IP"] += event.unicode

    # Rising edge detectie


    # Update vorige state
  

    pygame.display.flip()


pygame.quit()
