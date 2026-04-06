import pygame


def BovenRechthoeken(rect_pos_x, rect_pos_y, ActiRect_Width,ActiRect_Height, Mouse,Mouse_pos,Mouse_JustPressed,slepen
                     ,rect_offset_x,rect_offset_y,sleepvlak,bovenvlak,rect_startpos_x, rect_startpos_y,font_acti,StandaardActiviteiten,planning):


    for i in range(len(StandaardActiviteiten)):
        rect = pygame.Rect(rect_pos_x[i],rect_pos_y[i],ActiRect_Width,ActiRect_Height)   
        acti_text =font_acti.render(StandaardActiviteiten[i][1],1,("white"))



        if Mouse[0] and rect.collidepoint(Mouse_pos) and sum(slepen)<1 and planning ==False: #Detecteren of rechthoek is aangeklikt, er mag nog geen andere sleep bezig zijn
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
    achtergrond_color = pygame.Color(255,255,255,130)
    OnderRect = pygame.Rect(0,screen.get_height()/2,screen.get_width(),screen.get_height()/2)
    pygame.draw.rect(ondervlak,(achtergrond_color),OnderRect,0,0,80,80,0,0)

    for i in range(7):
        DagRect = pygame.Rect(screen.get_width()/2-(3.5*DagRect_Width+3*DagRect_Gap)+i*(DagRect_Width+DagRect_Gap),OnderRect.top+50,DagRect_Width,OnderRect.height)
        
        if dagrect_collision[i]:
            color = dagrect_color[1]
          
        else:
            color = dagrect_color[0]

        pygame.draw.rect(ondervlak,color,DagRect,0,0,30,30,0,0)

        if dagrect_collision[i]:
            pygame.draw.rect(ondervlak,((150,205,150)),DagRect,3,30)
               
       
        Dagen_Text =Font_Dagen.render(Dagen[i],1,(dagrect_color[0]))
        ondervlak.blit(Dagen_Text,(DagRect.centerx-Dagen_Text.get_width()/2,DagRect.top-Dagen_Text.get_height()-4))
        DagRects.append(DagRect)

# Button logica
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

  def draw(self,zichtbaar,mouse,mouse_pos):
    action = False
    self.zichtbaar = zichtbaar
    pos = pygame.mouse.get_pos()
    if self.rect.collidepoint(pos) and mouse[0] and self.pressed ==0:
      self.pressed=1
    elif self.pressed ==1 and mouse[0]== False:
      self.pressed=0
      action = True

    if self.zichtbaar:
      self.surface.blit(self.image,(self.rect.x,self.rect.y))     
    return action


# Button logica
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
      pygame.draw.rect(self.surface,self.color,self.rect,self.dikte,0,10,10,0,0) 
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
        self.TextRect_Height = Trect_Height
        self.ScrollOffset = ScrollOffset
        self.Font = Font
        

        self.Scroll_Index = 5 
        self.Start_Index = 0
        self.Start_Y = 0
        self.Scroll_dist = 0
        self.Scroll_active=False
        self.alpha=[80,120,255,120,80]
        self.scale = [(1,0.7),(1,0.9),(1,1),(1,0.9),(1,0.7)]
        self.Yoffset = [0,-0.2,-0.6,0.6,0.2] 

        self.TextRects =[]
        if u_m:
            self.Txt = [f"{i:02d}" for i in range(60)]
            self.X = HighlightRect.right - Trect_Width-10

        else:
            self.Txt = [f"{i:02d}" for i in range(24)]
            self.X = HighlightRect.left+10

        for i in range(-2,3):
            text_rect = pygame.Rect(self.X, HighlightRect.top+i*(self.TextRect_Height+10)+ self.Yoffset[i]*self.TextRect_Height, self.TextRect_Width,self.TextRect_Height)
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
            
            uur_txt = self.Font.render(self.Txt[(self.Scroll_Index + i) % len(self.Txt)], True, (10,10,10))
            uur_rect = uur_txt.get_rect(center=rect.center)

            uur_txt.set_alpha(self.alpha[i])
            uur_txt = pygame.transform.scale_by(uur_txt,self.scale[i])
            
            self.surface.blit(uur_txt, uur_rect)

        return self.Txt[(self.Scroll_Index + 2) % len(self.Txt)]






class Klok_Input:
    def __init__(self, width, height, verhouding, Font, surface, TextKleur, X, Y):
        self.width = width
        self.height = height
        self.verhouding = verhouding
        self.Font = Font
        self.surface = surface
        self.TextKleur = TextKleur
        self.Klok_Vak = []
        self.Pijl_Vak = []
        self.Input_Tijd = [0, 0, 0, 0]  # [uur-tiental, uur-eenheid, min-tiental, min-eenheid]
        self.X = X-self.width/2
        self.Y = Y-self.height/2

        self.Klok_Rect = pygame.Rect(self.X, self.Y + 15, self.width, self.height)

        for i in range(5):
            rect = pygame.Rect(self.Klok_Rect.left + i * (self.width / 5), self.Klok_Rect.top, self.width / 5, self.height)
            self.Klok_Vak.append(rect)

            rect = pygame.Rect(self.Klok_Rect.left + i * (self.width / 5), self.Klok_Rect.top, self.width / 5, self.height * verhouding)
            self.Pijl_Vak.append(rect)

        for i in range(5):
            rect = pygame.Rect(self.Klok_Rect.left + i * (self.width / 5), self.Klok_Rect.bottom - self.height * verhouding, self.width / 5, self.height * verhouding)
            self.Pijl_Vak.append(rect)

    def _max_waarde(self, i):
        """Geeft de maximale waarde terug voor elke digit."""
        if i == 0: return 2
        if i == 1: return 3 if self.Input_Tijd[0] == 2 else 9
        if i == 2: return 5
        if i == 3: return 9

    def _verhoog(self, i):
        """Verhoog digit i. Geeft True terug als er een carry is (= overloop naar 0)."""
        if self.Input_Tijd[i] >= self._max_waarde(i):
            self.Input_Tijd[i] = 0
            return True   # carry!
        else:
            self.Input_Tijd[i] += 1
            return False

    def _verlaag(self, i):
        """Verlaag digit i. Geeft True terug als er een borrow is (= onderloop)."""
        if self.Input_Tijd[i] <= 0:
            self.Input_Tijd[i] = self._max_waarde(i)
            return True   # borrow!
        else:
            self.Input_Tijd[i] -= 1
            return False

    def _verhoog_met_carry(self, i):
        """Verhoog digit i en geef carry door naar hogere digits."""
        carry = self._verhoog(i)
        if carry and i > 0:
            self._verhoog_met_carry(i - 1)  # carry naar de digit links

    def _verlaag_met_borrow(self, i):
        """Verlaag digit i en geef borrow door naar hogere digits."""
        borrow = self._verlaag(i)
        if borrow and i > 0:
            self._verlaag_met_borrow(i - 1)  # borrow naar de digit links

    def draw(self, Mouse_pos, Mouse_JustPressed):

        # ── max waarde uur-eenheid aanpassen ──────────────────────────────────
        if self.Input_Tijd[0] == 2 and self.Input_Tijd[1] > 3:
            self.Input_Tijd[1] = 3

        # ── pijlen omhoog (indices 0,1,3,4 → digits 0,1,2,3) ─────────────────
        for pijl_i, digit_i in [(0, 0), (1, 1), (3, 2), (4, 3)]:
            pygame.draw.aaline(self.surface, 'black',
                               (self.Pijl_Vak[pijl_i].left + 3,  self.Pijl_Vak[pijl_i].bottom),
                               (self.Pijl_Vak[pijl_i].centerx,   self.Pijl_Vak[pijl_i].top))
            pygame.draw.aaline(self.surface, 'black',
                               (self.Pijl_Vak[pijl_i].right - 3, self.Pijl_Vak[pijl_i].bottom),
                               (self.Pijl_Vak[pijl_i].centerx,   self.Pijl_Vak[pijl_i].top))

            if Mouse_JustPressed and self.Pijl_Vak[pijl_i].collidepoint(Mouse_pos):
                self._verhoog_met_carry(digit_i)  # ← carry logica hier

        # ── pijlen omlaag (indices 5,6,8,9 → digits 0,1,2,3) ─────────────────
        for pijl_i, digit_i in [(5, 0), (6, 1), (8, 2), (9, 3)]:
            pygame.draw.aaline(self.surface, 'black',
                               (self.Pijl_Vak[pijl_i].left + 3,  self.Pijl_Vak[pijl_i].top),
                               (self.Pijl_Vak[pijl_i].centerx,   self.Pijl_Vak[pijl_i].bottom))
            pygame.draw.aaline(self.surface, 'black',
                               (self.Pijl_Vak[pijl_i].right - 3, self.Pijl_Vak[pijl_i].top),
                               (self.Pijl_Vak[pijl_i].centerx,   self.Pijl_Vak[pijl_i].bottom))

            if Mouse_JustPressed and self.Pijl_Vak[pijl_i].collidepoint(Mouse_pos):
                self._verlaag_met_borrow(digit_i)  # ← borrow logica hier

        # ── cijfers tekenen ───────────────────────────────────────────────────
        for i in range(4):  # was range(5), index 2 was de dubbele punt
            klok = self.Font.render(str(self.Input_Tijd[i]), 1, 'black')
            self.surface.blit(klok, (self.Klok_Vak[i if i < 2 else i + 1].centerx - 5,
                                     self.Klok_Vak[i if i < 2 else i + 1].centery - 10))
        dubbelpunt = self.Font.render(":",1,"black")
        self.surface.blit(dubbelpunt,(self.Klok_Vak[2].centerx-dubbelpunt.get_width()/2,self.Klok_Vak[2].centery-dubbelpunt.get_height()/2))


      

def Planningsscherm_maken(overlay,planningvlak,PlanRect_Color,PlanRect,Font_PlanTitel,PlanRect_TitelColor,PlanRect1,Font_PlanKop1,PlanRect2,Font_PlanKop2,PlanRect2_1,
                          PlanRect2_2,PlanRect3,PlanBevestig_Knop,Mouse,Mouse_Pos,Mouse_JustPressed,Plan_Klok1,Plan_Klok2,PlanBox1,PlanActiviteit,GeplandeActiviteiten,Text_dict, Time):
   

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

    """    Kleur_kiezerRect = pygame.Rect(PlanRect1.right-100, PlanRect1.centery-15,30,30)
        #pygame.draw.rect(planningvlak,PlanActiviteit[5],Kleur_kiezerRect,0,10)
        
        if (Mouse_JustPressed and Kleur_kiezerRect.collidepoint(Mouse_Pos)) :
            print("goed gedaan ventjes")
    """





    # Tijd instellen tekst
    PlanKop2 = Font_PlanKop1.render("Tas klaarzetten om:",1,(40,40,40))
    planningvlak.blit(PlanKop2,(PlanRect2_1.left,PlanRect2_1.top))
    Plan_Klok1.draw(Mouse_Pos,Mouse_JustPressed)

    
    PlanKop2 = Font_PlanKop1.render("Vertrekken om:",1,(40,40,40))        
    planningvlak.blit(PlanKop2,(PlanRect2_2.left,PlanRect2_2.top))
    Plan_Klok2.draw(Mouse_Pos,Mouse_JustPressed)

    Uur0 = Plan_Klok1.Input_Tijd[0]*600 + Plan_Klok1.Input_Tijd[1]*60 + Plan_Klok1.Input_Tijd[2]*10+ Plan_Klok1.Input_Tijd[3]
    Uur1 = Plan_Klok2.Input_Tijd[0]*600 + Plan_Klok2.Input_Tijd[1]*60 + Plan_Klok2.Input_Tijd[2]*10+ Plan_Klok2.Input_Tijd[3]

    if Uur1<Uur0:
    
        Volgendedag_text = Font_PlanKop2.render("Volgende dag vertrekken",1,(40,40,40))
        planningvlak.blit(Volgendedag_text,(PlanRect2_2.left,PlanRect2_2.bottom))


    PlanKop1 = Font_PlanKop1.render("Wat moet er in de zak?",1,(40,40,40))
    planningvlak.blit(PlanKop1,(PlanRect3.left,PlanRect3.top))

    PlanBox1.draw(Font_PlanKop2,1,PlanActiviteit[4],Mouse_JustPressed,Mouse_Pos,len(PlanActiviteit[4]),Text_dict,Time)



def AgendaRechthoeken(GeplandeActiviteiten,DagRects,DagRect_Width,planRechthoeken,Font_GeplandeActi, Mouse_JustPressed, Mouse_Pos,AgendaRechthoeken_lst):
    Dagen_Tellen = [0]*7
    DagenRects =[]
    #Rechthoeken maken in de dagen
    for i in range(len(GeplandeActiviteiten)):
        

        dag = GeplandeActiviteiten[i][5]
        j = Dagen_Tellen[dag]
           
        GeplandRect = pygame.Rect(DagRects[GeplandeActiviteiten[i][5]].left,DagRects[0].top+30+j*35 ,DagRect_Width,50)
        pygame.draw.rect(planRechthoeken,GeplandeActiviteiten[i][6],GeplandRect,0,5)
        Activiteit_Text= Font_GeplandeActi.render(GeplandeActiviteiten[i][1],1,'white')
        planRechthoeken.blit(Activiteit_Text,(GeplandRect.centerx-Activiteit_Text.get_width()/2,GeplandRect.centery-Activiteit_Text.get_height()/2))

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




def DeleteMelding(surface,overlay,Font, Knop_Font,Mouse,Mouse_pos,Mouse_JustPressed,Bevestig_kleur,Annuleer_kleur):

        return_list=[False]*2
        overlay.set_alpha(120)
        VlakRect_width = 0.5*surface.get_width()
        VlakRect_height = 0.3*surface.get_height()
        VlakRect = pygame.Rect(surface.get_width()/2-VlakRect_width/2, surface.get_height()/2-VlakRect_height/2,VlakRect_width,VlakRect_height)

        pygame.draw.rect(surface,(220,220,220),VlakRect,0,20)
        DeleteMelding_Tekst = Font.render("Ben je zeker dat je dit wilt verwijderen?",1,(0,0,0))
        surface.blit(DeleteMelding_Tekst,(surface.get_width()/2-DeleteMelding_Tekst.get_width()/2,VlakRect.top+DeleteMelding_Tekst.get_height()+10))
        
        DeleteBevestig_knop = Button_Rechthoek(VlakRect_width/3,50,0,Bevestig_kleur,surface, VlakRect.centerx+VlakRect.width/12,VlakRect.bottom-30, Knop_Font,(255,255,255),"Bevestig")
        DeleteBevestig_knop.draw(1,Mouse,Mouse_pos)
        DeleteAnnuleer_knop = Button_Rechthoek(VlakRect_width/3,50,0,Annuleer_kleur,surface, VlakRect.left+VlakRect.width/12,VlakRect.bottom-30, Knop_Font,(255,255,255),"Annuleer")
        DeleteAnnuleer_knop.draw(1,Mouse,Mouse_pos)
        
        if  Mouse_JustPressed:
            if DeleteBevestig_knop.rect.collidepoint(Mouse_pos):
                return_list[1]=True
            elif DeleteAnnuleer_knop.rect.collidepoint(Mouse_pos):
                return_list[0]=True
        return return_list




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
            print(    Text_dict["User_IP"])
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
            print(    Text_dict["User_IP"])
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
            print(Text_dict["User_IP"])
            pygame.draw.rect(surface,keyboardColor[1],rect,0)
        else:
            pygame.draw.rect(surface,keyboardColor[0],rect,0)
        surface.blit(Letter,(rect.centerx-Letter.get_width()/2,rect.centery-Letter.get_height()/2))
    
    #Backspace
    BackspaceRect = pygame.Rect(StartRij3 + 6*(rect_width+rect_gap),StartRij1 + 2*(rect_height+rect_gap),2*rect_width + rect_gap,rect_height)
    if BackspaceRect.collidepoint(mouse_pos)and mouse_justpressed:
        Text_dict["User_IP"] = Text_dict["User_IP"][:-1]
        print(Text_dict["User_IP"])
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
        print(Text_dict["User_IP"])
        pygame.draw.rect(surface,keyboardColor[1],SpatieRect,0)
    else:
        pygame.draw.rect(surface,keyboardColor[0],SpatieRect,0)




def TextInputscherm(surface, font, Text_dict,TextRect,Time):



    pygame.draw.rect(surface,(220,220,220),TextRect,0,10)

    TextInput =font.render(Text_dict["User_IP"],1,(0,0,0))
    surface.blit(TextInput,(TextRect.left+20,TextRect.centery-TextInput.get_height()/2))
    if (Time // 500) % 2 == 0  and Text_dict["User_IP"] == "":
        pygame.draw.line(surface,(180,180,180),(TextRect.left+20,TextRect.top+15),(TextRect.left+20,TextRect.bottom-15))  
        






