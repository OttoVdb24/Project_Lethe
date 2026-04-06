import pygame
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
                


    def draw(self, mouse_justpressed, mouse: tuple,mouse_pos: tuple ):
    
        if (mouse_justpressed[0] and self.ScrollRect.collidepoint(mouse_pos)) or self.Scroll_active:
            if mouse_justpressed[0]:
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
