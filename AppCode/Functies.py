import pygame



class Button:
  def __init__ (self,image,surface,X,Y):
    self.image = image
    self.surface = surface
    self.height = self.image.get_height()
    self.width  = self.image.get_width()
    self.rect = self.image.get_rect()
    self.X = X
    self.Y = Y
    self.rect.topleft = ((self.X,self.Y))
    self.pressed = 0

  def draw(self,zichtbaar,mouse,mouse_pos,mouse_justpressed):
    action = False
    self.zichtbaar = zichtbaar
    pos = pygame.mouse.get_pos()
    if self.rect.collidepoint(pos) and mouse_justpressed:
      action = True
    else:
        action = False

    if self.zichtbaar:
      self.surface.blit(self.image,(self.rect.x,self.rect.y))     
    return action


class Button_Rechthoek:
  def __init__ (self,width,height,dikte,color,surface,X,Y, TextFont, textcolor,text_str):
    self.width = width
    self.height = height
    self.dikte = dikte
    self.color = color
    self.surface = surface
    self.X = X
    self.Y = Y
    self.rect = pygame.Rect(self.X,self.Y,self.width,self.height)
    self.buttontext = TextFont.render(text_str,1,textcolor)
    self.pressed = 0

  def draw(self,zichtbaar,mouse,mouse_pos):
    self.action = False
    self.zichtbaar = zichtbaar
    if self.rect.collidepoint(mouse_pos) and mouse[0] and self.pressed ==0:
      self.pressed=1
    elif self.pressed == 1 and mouse[0]==False:
      self.pressed=0
      self.action = True

    if self.zichtbaar:
      pygame.draw.rect(self.surface,self.color,self.rect,self.dikte,10) 
      self.surface.blit(self.buttontext,(self.rect.centerx-self.buttontext.get_width()/2,self.rect.centery-self.buttontext.get_height()/2))    
    return self.action
  

class PlanBox:
    def __init__ (self, surface,planrect,color,lijn,height):
        self.width = planrect.width - 20
        self.surface = surface
        self.y =  planrect.top
        self.x = planrect.left
        self.lijn = [lijn,0]
        self.height = height
        self.Actief = [False]*8
        self.RectColor = [pygame.Color(40,40,40), pygame.Color(180,220,180,0)]
        self.VakColor = [pygame.Color(40,40,40), pygame.Color(225,225,225,255)]
        self.yoffset = self.height +10




    def draw(self,Font,text,benodigdheden,Mouse_JustPressed,mousepos,Aantal_Boxen,Text_dict,Time):
        for i in range(Aantal_Boxen):
            self.boxrect = pygame.Rect(self.x,self.y+i*self.yoffset,self.width,self.height)
            self.vinkvak = pygame.Rect(self.boxrect.left+20,self.boxrect.centery-10,20,20)


            if self.boxrect.collidepoint(mousepos) and Mouse_JustPressed and self.Actief[i] == False:
                self.Actief[i] = True

            elif self.boxrect.collidepoint(mousepos) and Mouse_JustPressed and self.Actief[i] == True:
                self.Actief[i] = False
            
            
                
            pygame.draw.rect(self.surface,self.RectColor[int(self.Actief[i])],self.boxrect,self.lijn[int(self.Actief[i])],10)    #Rechthoek
            pygame.draw.rect(self.surface,self.VakColor[int(self.Actief[i])],self.vinkvak,2,3)                            #Vakje

            if self.Actief[i]:
                pygame.draw.aaline(self.surface,"white",(self.vinkvak.left,self.vinkvak.centery),(self.vinkvak.centerx,self.vinkvak.bottom),6)
                pygame.draw.aaline(self.surface,"white",(self.vinkvak.topright),(self.vinkvak.centerx,self.vinkvak.bottom),6)
                
            if text:
                    Benodigdheden_Tekst = Font.render(benodigdheden[i],1,(40,40,40))
                    self.surface.blit(Benodigdheden_Tekst,(self.boxrect.centerx-Benodigdheden_Tekst.get_width()/2,self.boxrect.centery-Benodigdheden_Tekst.get_height()/2))
        

        #Alles voor de extra box om nieuwe benodigdheden toe te voegen.

        self.ToevoegBox = pygame.Rect(self.x,self.y + (Aantal_Boxen)*self.yoffset,self.width,self.height)
        pygame.draw.rect(self.surface,'black',self.ToevoegBox,1,10)    #Rechthoek


        self.PlusRect = pygame.Rect(self.ToevoegBox.right- 40,self.ToevoegBox.centery-10,20,20)
        pygame.draw.line(self.surface,'black',(self.PlusRect.left,self.PlusRect.centery),(self.PlusRect.right,self.PlusRect.centery),2)
        pygame.draw.line(self.surface,'black',(self.PlusRect.centerx,self.PlusRect.top),(self.PlusRect.centerx,self.PlusRect.bottom),2)

        if Mouse_JustPressed and self.ToevoegBox.collidepoint(mousepos):
            Text_dict["PlanText_Active"] = True

        if Text_dict["PlanText_Active"]:
            self.ToevoegText = Text_dict["User_IP"]

            if (Time // 500) % 2 == 0 and Text_dict["User_IP"] == "":
                pygame.draw.line(self.surface,"black",(self.ToevoegBox.left+20,self.ToevoegBox.top+10),(self.ToevoegBox.left+20,self.ToevoegBox.bottom-10))
        
        
        
        else:
            self.ToevoegText = "Extra toevoegen"

        Toevoeg_Tekst = Font.render(self.ToevoegText,1,(40,40,40))        
        self.surface.blit(Toevoeg_Tekst,(self.ToevoegBox.left+20,self.ToevoegBox.centery-Toevoeg_Tekst.get_height()/2))

        
class KlokScroll:
    def __init__(self,surface,u_m: bool,HighlightRect, Trect_Width:int, Trect_Height:int, ScrollOffset: int, Font):
        self.surface = surface
        self.HiglightRect = HighlightRect
        self.TextRect_Width = Trect_Width
        self.TextRect_Height = self.HiglightRect.height
        self.ScrollOffset = ScrollOffset
        self.Font = Font
        

        self.Scroll_Index = 5 
        self.Start_Index = 0
        self.Start_Y = 0
        self.Scroll_dist = 0
        self.Scroll_active=False
        self.alpha=[40,100,255,100,40]
        self.scale = [(1,0.7),(1,0.9),(1,1),(1,0.9),(1,0.7)]
        self.Yoffset = [0,-0.2,-0.6,0.6,0.2] 
        self.TextRects =[]
        if u_m:
            self.Txt = [f"{i:02d}" for i in range(60)]
            self.X = HighlightRect.right - Trect_Width-HighlightRect.width*0.20

        else:
            self.Txt = [f"{i:02d}" for i in range(24)]
            self.X = HighlightRect.left+HighlightRect.width*0.20


        for i in range(-2,3):
            text_rect = pygame.Rect(self.X, HighlightRect.top+i*(self.TextRect_Height+10)+ self.Yoffset[i]*self.TextRect_Height, self.TextRect_Width, self.TextRect_Height)
            self.TextRects.append(text_rect)
        self.ScrollRect = pygame.Rect(self.TextRects[0].left-ScrollOffset/2, self.TextRects[0].top-ScrollOffset/2, self.TextRect_Width+ScrollOffset, (self.TextRects[len(self.TextRects)-1].bottom +ScrollOffset/2) -(self.TextRects[0].top-ScrollOffset/2))
                


    def draw(self, mouse_justpressed: bool, mouse: tuple,mouse_pos: tuple ):
    
        if (mouse_justpressed and self.ScrollRect.collidepoint(mouse_pos)) or self.Scroll_active:
            if mouse_justpressed:
                self.Start_Y = mouse_pos[1]
                self.Start_Index = self.Scroll_Index
                self.Scroll_active =True

            
            self.Scroll_dist=mouse_pos[1]-self.Start_Y
            self.Scroll_Index = self.Start_Index- (self.Scroll_dist//40)

        if not mouse[0]:
            self.Scroll_active=False

        for i, rect in enumerate(self.TextRects):
            
            uur_txt = self.Font.render(self.Txt[(self.Scroll_Index + i) % len(self.Txt)], True, (20,20,20))
            uur_rect = uur_txt.get_rect(center=rect.center)

            uur_txt.set_alpha(self.alpha[i])
            uur_txt = pygame.transform.scale_by(uur_txt,self.scale[i])
            
            self.surface.blit(uur_txt, uur_rect)

        return self.Txt[(self.Scroll_Index + 2) % len(self.Txt)]






def BovenRechthoeken(rect_pos_x, rect_pos_y, ActiRect_Width,ActiRect_Height, Mouse,Mouse_pos,Mouse_JustPressed,slepen
                     ,rect_offset_x,rect_offset_y,sleepvlak,bovenvlak,rect_startpos_x, rect_startpos_y,font_acti,StandaardActiviteiten,Actieve_Status):


    for i in range(len(StandaardActiviteiten)):
        rect = pygame.Rect(rect_pos_x[i],rect_pos_y[i],ActiRect_Width,ActiRect_Height)   
        acti_text =font_acti.render(StandaardActiviteiten[i][1],1,("white"))



        if Mouse[0] and rect.collidepoint(Mouse_pos) and sum(slepen)<1 and Actieve_Status == "Hoofdscherm": #Detecteren of rechthoek is aangeklikt, er mag nog geen andere sleep bezig zijn
            slepen[i]=True
            rect_offset_x[i] = Mouse_pos[0]-rect_pos_x[i] # Offset berekenen tussen Topleft en muis
            rect_offset_y[i] = Mouse_pos[1]-rect_pos_y[i]
        

        if slepen[i]:   
            # Tijdens het slepen
            if Mouse[0]==False:
                rect_pos_x[i]=rect_startpos_x[i]
                rect_pos_y[i] = rect_startpos_y[i]
                slepen[i]=False                               # Controle is muis wel nog ingedrukt

            else:                                                  #Als muis nog geklikt is is positie de sleep positie
                rect_pos_x[i]= Mouse_pos[0]- rect_offset_x[i]
                rect_pos_y[i]= Mouse_pos[1]- rect_offset_y[i]

            pygame.draw.rect(sleepvlak,StandaardActiviteiten[i][5],rect,0,10) #Rechthoek tekenen op sleepvlak als die aan het slepen is, zodat die boven alles komt
            sleepvlak.blit(acti_text,(rect.centerx-acti_text.get_width()/2,rect.bottom-acti_text.get_height() - 5))
            sleepvlak.blit(StandaardActiviteiten[i][6],(rect.centerx-StandaardActiviteiten[i][6].get_width()/2,rect.top+5))

        else:
            pygame.draw.rect(bovenvlak,StandaardActiviteiten[i][5],rect,0,10) # Rechthoek tekenen als die niet aan het slepen is (Lagere laag).
            bovenvlak.blit(acti_text,(rect.centerx-acti_text.get_width()/2,rect.bottom-acti_text.get_height() - 5))
            bovenvlak.blit(StandaardActiviteiten[i][6],(rect.centerx-StandaardActiviteiten[i][6].get_width()/2,rect.top+5))


def OnderkantFunctie(screen, ondervlak,DagRect_Width,DagRect_Gap,DagRect_Height,Mouse_pos,Font_Dagen,Dagen,DagRects,dagrect_color,dagrect_collision):
    DagRects.clear()
    achtergrond_color = pygame.Color(255,255,255,200)
    OnderRect = pygame.Rect(0,screen.get_height()/2,screen.get_width(),screen.get_height()/2)
    pygame.draw.rect(ondervlak,(achtergrond_color),OnderRect,0,0,80,80,0,0)

    for i in range(7):
        DagRect = pygame.Rect(screen.get_width()/2-(3.5*DagRect_Width+3*DagRect_Gap)+i*(DagRect_Width+DagRect_Gap),OnderRect.top+50,DagRect_Width,OnderRect.height)

        
        if dagrect_collision[i]:
            color = dagrect_color[1]
          
        else:
            color = dagrect_color[0]
        """        
        for j in range(3):
            KleineDagRect = pygame.Rect(DagRect.left, DagRect.top + j*(0.5*DagRect.width+10),DagRect.width,0.5*DagRect.width)
            pygame.draw.rect(ondervlak,color,KleineDagRect,0,10)

        """
        pygame.draw.rect(ondervlak,color,DagRect,0,0,10,10,0,0)

        if dagrect_collision[i]:
            pygame.draw.rect(ondervlak,((150,205,150)),DagRect,2,10)
               
       
        Dagen_Text =Font_Dagen.render(Dagen[i],1,(140,80,80))
        ondervlak.blit(Dagen_Text,(DagRect.centerx-Dagen_Text.get_width()/2,DagRect.top-Dagen_Text.get_height()-4))
        DagRects.append(DagRect)
    

def Planningsscherm(overlay,planningvlak,PlanRect_Color,PlanRect,Font_PlanTitel,PlanRect_TitelColor,PlanRect1,Font_PlanKop1,Font_PlanKop2,PlanRect2_1,
                          PlanRect2_2,PlanRect3,Mouse,Mouse_Pos,Mouse_JustPressed,PlanBox1,PlanActiviteit,Text_dict, Time,HighLightRect,Klok1_U,Klok1_M ,
                          HighlightRect2,Klok2_U,Klok2_M,klokvlak,KleurRects, KleurKiezerActive,KleurkiezerRect, PlanExt_knop):
   
# Plannings window maken

    #Achtergrond vervagen
    overlay.set_alpha(120)  # 0 = volledig transparant, 255 = volledig ondoorzichtig
    #Planningsrechthoek 
    pygame.draw.rect(planningvlak,PlanRect_Color,PlanRect,0,0,40,40)


    


    #Window titel maken
    PlanTitel =Font_PlanTitel.render(PlanActiviteit[1],1,PlanRect_TitelColor)
    planningvlak.blit(PlanTitel,(PlanRect1.left,PlanRect1.centery-PlanTitel.get_height()/2))
    # Tussenlijn
    pygame.draw.line(planningvlak,(200,200,200),(PlanRect.left+1,PlanRect1.bottom),(PlanRect.right-1,PlanRect1.bottom),1)

    Kleur_kiezerRect = pygame.Rect(PlanRect3.left, PlanRect1.centery-30,60,60)
    pygame.draw.rect(planningvlak,PlanActiviteit[5],Kleur_kiezerRect,0,20)
    Kleurkies_Txt = Font_PlanKop2.render("Klik op het vierkantje voor een andere kleur",1,PlanRect_TitelColor)
    planningvlak.blit(Kleurkies_Txt,(Kleur_kiezerRect.right+10,PlanRect1.centery-Kleurkies_Txt.get_height()/2))
        
    if (Mouse_JustPressed and Kleur_kiezerRect.collidepoint(Mouse_Pos)):
        KleurKiezerActive= True
    elif Mouse_JustPressed and not KleurkiezerRect.collidepoint(Mouse_Pos):
        KleurKiezerActive = False
    






    # Tijd instellen tekst
    PlanKop2 = Font_PlanKop1.render("Vertrekken om:",1,(40,40,40))
    planningvlak.blit(PlanKop2,(PlanRect2_1.left,PlanRect2_1.top))
    HighLightRectColor = PlanActiviteit[5]
    pygame.draw.rect(klokvlak,HighLightRectColor,HighLightRect,0,20)
    Klok1_Uur = Klok1_U.draw(Mouse_JustPressed,Mouse,Mouse_Pos)
    Klok1_Min = Klok1_M.draw(Mouse_JustPressed,Mouse,Mouse_Pos)


    
    PlanKop2 = Font_PlanKop1.render("Tas klaarmaken om:",1,(40,40,40))        
    planningvlak.blit(PlanKop2,(PlanRect2_2.left,PlanRect2_2.top))
    pygame.draw.rect(klokvlak,HighLightRectColor,HighlightRect2,0,20)
    Klok2_Uur = Klok2_U.draw(Mouse_JustPressed,Mouse,Mouse_Pos)
    Klok2_Min = Klok2_M.draw(Mouse_JustPressed,Mouse,Mouse_Pos)


    PlanKop1 = Font_PlanKop1.render("Wat moet er in de zak?",1,(40,40,40))
    planningvlak.blit(PlanKop1,(PlanRect3.left,PlanRect3.top))


    
    if not KleurKiezerActive:
        PlanBox1.draw(Font_PlanKop2,1,PlanActiviteit[4],Mouse_JustPressed,Mouse_Pos,len(PlanActiviteit[4]),Text_dict,Time)

    if KleurKiezerActive:
        ColorPicker  = [(255,50,50,60),(50,255,50,60),(50,50,255,60),(255,255,50,60),(50,255,255,60),(255,50,255,60)]
        pygame.draw.rect(planningvlak,(230,230,230),KleurkiezerRect,0,10)
        for i, rect in enumerate(KleurRects):
            pygame.draw.rect(planningvlak,ColorPicker[i],rect,0,5)
            if Mouse_JustPressed and rect.collidepoint(Mouse_Pos):
                PlanActiviteit[5]=ColorPicker[i]
                print("Kleur")
        return False, KleurKiezerActive

    else:
    
        if PlanExt_knop.draw(1,Mouse,Mouse_Pos,Mouse_JustPressed):
                print("Tik")
                return True, False



    return False,KleurKiezerActive


def AgendaRechthoeken(GeplandeActiviteiten,DagRects,DagRect_Width,planRechthoeken,Font_GeplandeActi, Mouse_JustPressed, Mouse_Pos,AgendaRechthoeken_lst):
    Dagen_Tellen = [0]*7
    DagenRects =[]
    #Rechthoeken maken in de dagen
    for i in range(len(GeplandeActiviteiten)):
        
        symbool = GeplandeActiviteiten[i][7]
        dag = GeplandeActiviteiten[i][5]
        j = Dagen_Tellen[dag]
        GeplandRect = pygame.Rect(DagRects[GeplandeActiviteiten[i][5]].left, DagRects[0].top + j*(0.5*DagRect_Width + 5) ,DagRect_Width,DagRect_Width*0.5)
        pygame.draw.rect(planRechthoeken,GeplandeActiviteiten[i][6],GeplandRect,0,10)
        
        Activiteit_Text= Font_GeplandeActi.render(GeplandeActiviteiten[i][1],1,'white')
        planRechthoeken.blit(Activiteit_Text,(GeplandRect.centerx-Activiteit_Text.get_width()/2
                                              , GeplandRect.bottom-1.1*Activiteit_Text.get_height()))

        planRechthoeken.blit(symbool,(GeplandRect.centerx-symbool.get_width()/2
                                      ,GeplandRect.top ))

        Dagen_Tellen[dag]+=1

        if Mouse_JustPressed and GeplandRect.collidepoint(Mouse_Pos):
            AgendaRechthoeken_lst = [True,i]
        
    
    return AgendaRechthoeken_lst
        

def NieuweActiviteit_maken(NieuweActiInput_Rect, Mouse_Pos, Mouse_JustPressed, Text_dict,overlay,nieuweActivlak,NieuweActiRect_color,NieuweActiRect,Font_PlanKop1,Font_KnopText,NieuweActiInput_Text,Time):
        
        pygame.draw.rect(nieuweActivlak,NieuweActiRect_color,NieuweActiRect,0,30)
        NieuweActi_Titel = Font_PlanKop1.render("Geef je activiteit een naam:",1,(0,0,0))
        nieuweActivlak.blit(NieuweActi_Titel, (NieuweActiInput_Rect.centerx-NieuweActi_Titel.get_width()/2,NieuweActiInput_Rect.top-NieuweActi_Titel.get_height()-20))

        
        
        if NieuweActiInput_Rect.collidepoint(Mouse_Pos) and Mouse_JustPressed:
            Text_dict["NieuweActiText_active"]=True

        
        if Text_dict["NieuweActiText_active"] or Text_dict["User_IP"] != "":
            NieuweActiInput_Text = Text_dict["User_IP"]

      


        overlay.set_alpha(120)
        pygame.draw.rect(nieuweActivlak,(180,180,180),NieuweActiInput_Rect,1,10)
        NieuweActi_Textvak = Font_KnopText.render(NieuweActiInput_Text,1,(180,180,180))
        nieuweActivlak.blit(NieuweActi_Textvak, (NieuweActiInput_Rect.left+20, NieuweActiInput_Rect.centery-NieuweActi_Textvak.get_height()/2))


def DeleteMelding(surface,overlay,Font, Knop_Font,Mouse,Mouse_pos,Mouse_JustPressed,Bevestig_kleur,Exit_img,Annuleer_kleur):

        return_list=[False]*2
        overlay.set_alpha(120)
        VlakRect_width = 0.6*surface.get_width()
        VlakRect_height = 0.5*surface.get_height()
        VlakRect = pygame.Rect(surface.get_width()/2-VlakRect_width/2, surface.get_height()/2-VlakRect_height/2,VlakRect_width,VlakRect_height)

        pygame.draw.rect(surface,(220,220,220),VlakRect,0,20)
        DeleteMelding_Tekst = Font.render("Zeker dat je de activiteit wilt verwijderen?",1,(0,0,0))
        DeletMelding_Tekst_top = VlakRect.top+20
        surface.blit(DeleteMelding_Tekst,(surface.get_width()/2-DeleteMelding_Tekst.get_width()/2, DeletMelding_Tekst_top))
        
        DeleteBevestig_knop = Button_Rechthoek(VlakRect_width/3,80,0,Bevestig_kleur,surface, VlakRect.right- VlakRect_width*0.02 - VlakRect_width/3,VlakRect.bottom-80-10, Knop_Font,(255,255,255),"Bevestig")
        DeleteBevestig_knop.draw(1,Mouse,Mouse_pos)
        DeleteAnnuleer_knop = Button_Rechthoek(VlakRect_width/3,80,0,Annuleer_kleur,surface, VlakRect.left + VlakRect_width*0.02 ,VlakRect.bottom-80-10, Knop_Font,(255,255,255),"Annuleer")
        DeleteAnnuleer_knop.draw(1,Mouse,Mouse_pos)


        DeleteExt_knop = Button(Exit_img,surface,VlakRect.right-Exit_img.get_width()-20, 
                                DeletMelding_Tekst_top+DeleteMelding_Tekst.get_height()/2-Exit_img.get_height()/2)
        
        pygame.draw.line(surface,(200,200,200),(VlakRect.left+1,DeletMelding_Tekst_top+DeleteMelding_Tekst.get_height()+20)
                                            ,(VlakRect.right-1, DeletMelding_Tekst_top+DeleteMelding_Tekst.get_height()+20) )


        if DeleteExt_knop.draw(1,Mouse,Mouse_pos,Mouse_JustPressed):
            return_list[0] =True

        
        if  Mouse_JustPressed:
            if DeleteBevestig_knop.rect.collidepoint(Mouse_pos):
                return_list[1]=True
            elif DeleteAnnuleer_knop.rect.collidepoint(Mouse_pos):
                return_list[0]=True
        return return_list


def Beveiliging(surface,overlay,Titel_Font, Font_Kop2, Knop_Font,Mouse,Mouse_pos,Mouse_JustPressed,Bevestig_kleur, Exit_img):

        return_list=[False]*2
        overlay.set_alpha(120)

        #Achtergrond vlak maken
        VlakRect_width = 0.6*surface.get_width()
        VlakRect_height = 0.5*surface.get_height()
        VlakRect = pygame.Rect(surface.get_width()/2-VlakRect_width/2, surface.get_height()/2-VlakRect_height/2,VlakRect_width,VlakRect_height)
        pygame.draw.rect(surface,(220,220,220),VlakRect,0,20)


        #Titel Tekst
        Beveiliging_txt = Titel_Font.render("Los op om de activiteit te verwijderen.",1,(0,0,0))
        Beveiliging_txt_top = VlakRect.top+20
        surface.blit(Beveiliging_txt,(surface.get_width()/2-Beveiliging_txt.get_width()/2,Beveiliging_txt_top))
        
        BeveiligingExt_knop = Button(Exit_img,surface,VlakRect.right-Exit_img.get_width()-20, Beveiliging_txt_top+Beveiliging_txt.get_height()/2-Exit_img.get_height()/2)
        if BeveiligingExt_knop.draw(1,Mouse,Mouse_pos,Mouse_JustPressed):
            return "Exit"


        pygame.draw.line(surface,(200,200,200),(VlakRect.left+1,Beveiliging_txt_top+Beveiliging_txt.get_height()+20)
                                                ,(VlakRect.right-1, Beveiliging_txt_top+Beveiliging_txt.get_height()+20) )


        #Vraagstuk tekst
        Vraagstuk_txt = Font_Kop2.render("Hoeveel is 99/3 + 1?",1,(0,0,0))
        surface.blit(Vraagstuk_txt,(surface.get_width()/2-Vraagstuk_txt.get_width()/2,
                                    VlakRect.centery - Vraagstuk_txt.get_height()))
        

        Antwoorden = [21,34,60]
        AntwoordKnop_width = VlakRect_width*0.2
        AntwoordKnop_gap = VlakRect_width*0.01
        AntwoordKnop_StartX = VlakRect.centerx-(1.5*AntwoordKnop_width+AntwoordKnop_gap) 
        
        for i in range(len(Antwoorden)):
            AntwoordKnop = Button_Rechthoek(AntwoordKnop_width,0.4*AntwoordKnop_width,0,Bevestig_kleur,surface,
                                            AntwoordKnop_StartX + i*(AntwoordKnop_width+AntwoordKnop_gap), VlakRect.centery+0.4*AntwoordKnop_width, Titel_Font,"black",str(Antwoorden[i]))
            AntwoordKnop.draw(1,Mouse,Mouse_pos)

            if AntwoordKnop.rect.collidepoint(Mouse_pos)and Mouse_JustPressed and i==1:
                return "Correct"


def Keyboard(surface, Text_dict, mouse_justpressed, mouse_pos,font, keyboardColor):
    w= surface.get_width()
    h = surface.get_height()
    rect_gap = 0.0075*w
    rect_rand = 0.025*w
    rect_width = (w-2*rect_rand-9*rect_gap)/10
    rect_height = 0.5*rect_width
    StartRij1 = h- (4*rect_height + 4*rect_gap)

    StartRij3 = rect_rand+ 2*(rect_width + rect_gap)
    Spatie_width = 4*rect_width+3*rect_gap
    Spatie_Start = surface.get_width()/2-Spatie_width/2

    AchtergrondColor = pygame.Color(120,153,182,200)
    AchtergrondRect = pygame.Rect(0,surface.get_height()/2,w,h)
    pygame.draw.rect(surface,AchtergrondColor,AchtergrondRect,0,0,80,80)
   
    #Rij1
    Letters1 = ["A","Z","E","R","T","Y","U","I","O","P"]
    for i in range(len(Letters1)):
        rect = pygame.Rect(rect_rand + i*(rect_width+rect_gap),StartRij1,rect_width,rect_height)
        Letter = font.render(Letters1[i],1,("white"))
        if rect.collidepoint(mouse_pos)and mouse_justpressed:
            Text_dict["User_IP"]+= Letters1[i]
            pygame.draw.rect(surface,keyboardColor[1],rect,0)
        else:
            pygame.draw.rect(surface,keyboardColor[0],rect,0)
        surface.blit(Letter,(rect.centerx-Letter.get_width()/2,rect.centery-Letter.get_height()/2))



    #Rij2
    Letters2 = ["Q","S","D","F","G","H","J","K","L","M"]
    for i in range(len(Letters2)):
        rect = pygame.Rect(rect_rand + i*(rect_width+rect_gap),StartRij1 + rect_height+rect_gap,rect_width,rect_height)
        Letter = font.render(Letters2[i],1,("white"))
        if rect.collidepoint(mouse_pos)and mouse_justpressed:
            Text_dict["User_IP"]+= Letters2[i]
            pygame.draw.rect(surface,keyboardColor[1],rect,0)
        else:
            pygame.draw.rect(surface,keyboardColor[0],rect,0)
        surface.blit(Letter,(rect.centerx-Letter.get_width()/2,rect.centery-Letter.get_height()/2))

    #Rij3
    Letters3 = ["W","X","C","V","B","N"]
    for i in range(len(Letters3)):
        rect = pygame.Rect(StartRij3 + i*(rect_width+rect_gap),StartRij1 + 2*(rect_height+rect_gap),rect_width,rect_height)
        Letter = font.render(Letters3[i],1,("white"))
        if rect.collidepoint(mouse_pos)and mouse_justpressed:
            Text_dict["User_IP"]+= Letters3[i]
            pygame.draw.rect(surface,keyboardColor[1],rect,0)
        else:
            pygame.draw.rect(surface,keyboardColor[0],rect,0)
        surface.blit(Letter,(rect.centerx-Letter.get_width()/2,rect.centery-Letter.get_height()/2))
    
    #Backspace
    BackspaceRect = pygame.Rect(StartRij3 + 6*(rect_width+rect_gap),StartRij1 + 2*(rect_height+rect_gap),2*rect_width + rect_gap,rect_height)
    if BackspaceRect.collidepoint(mouse_pos)and mouse_justpressed:
        Text_dict["User_IP"] = Text_dict["User_IP"][:-1]
        pygame.draw.rect(surface,keyboardColor[1],BackspaceRect,0)
    else:
        pygame.draw.rect(surface,keyboardColor[0],BackspaceRect,0)
    BackspaceIcoonRect_width = BackspaceRect.width*0.5
    BackspaceIcoonRect_height = BackspaceRect.height*0.6
    BackspaceIcoonRect = pygame.Rect(BackspaceRect.centerx-BackspaceIcoonRect_width/2,BackspaceRect.centery-BackspaceIcoonRect_height/2,BackspaceIcoonRect_width,BackspaceIcoonRect_height)
    pygame.draw.aalines(surface,"white",2,[BackspaceIcoonRect.topright,BackspaceIcoonRect.bottomright,(BackspaceIcoonRect.left+BackspaceIcoonRect_width*0.25 , BackspaceIcoonRect.bottom), (BackspaceIcoonRect.left,BackspaceIcoonRect.centery),(BackspaceIcoonRect.left+BackspaceIcoonRect_width*0.25 , BackspaceIcoonRect.top)])

    #Spatie
    SpatieRect = pygame.Rect(Spatie_Start,StartRij1+3*(rect_height+rect_gap),4* rect_width+3*rect_gap,rect_height)
    if SpatieRect.collidepoint(mouse_pos)and mouse_justpressed:
        Text_dict["User_IP"] +=" "
        pygame.draw.rect(surface,keyboardColor[1],SpatieRect,0)
    else:
        pygame.draw.rect(surface,keyboardColor[0],SpatieRect,0)


def TextInputscherm(surface, font, Text_dict,TextRect,Time):



    pygame.draw.rect(surface,(220,220,220),TextRect,0,10)

    TextInput =font.render(Text_dict["User_IP"],1,(0,0,0))
    surface.blit(TextInput,(TextRect.left+20,TextRect.centery-TextInput.get_height()/2))
    if (Time // 500) % 2 == 0  and Text_dict["User_IP"] == "":
        pygame.draw.line(surface,(180,180,180),(TextRect.left+20,TextRect.top+15),(TextRect.left+20,TextRect.bottom-15))  
        






