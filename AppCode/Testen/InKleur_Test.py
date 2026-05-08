import pygame
import sys
import os
import numpy
basis = os.path.dirname(os.path.dirname(__file__))
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
GraphicsMap = os.path.join(basis,"Graphics")
BenodigdhedenMap = os.path.join(GraphicsMap,"Benodigdheden")

def laad_symbool(map,bestand):
    return pygame.image.load(os.path.join(map, bestand)).convert_alpha()

Handdoek_kleur = laad_symbool(BenodigdhedenMap,"Zwembroek_Kleur.svg")
Handdoek_leeg = laad_symbool(BenodigdhedenMap,"Zwembroek_Leeg.svg")

class inKleurButton:
    def __init__(self, Leegsymbool, Kleursymbool, ondervlak, tekenvlak):
        self.Kleursymbool = Kleursymbool
        self.ondervlak = ondervlak
        self.tekenvlak = tekenvlak
        self.leegsymbool = Leegsymbool
        self.klaar = False
        self.vorige_pos = None  # ← nieuw

        ButtonRect_width = 0.5*width
        ButtonRect_Height = 0.5*height
        self.ButtonRect = pygame.Rect(width/2-ButtonRect_width/2, height/2-ButtonRect_Height/2, ButtonRect_width, ButtonRect_Height)
        self.symbool_Rect = Kleursymbool.get_rect(center=self.ButtonRect.center)
        tekenvlak.blit(Leegsymbool, self.symbool_Rect)

        checkRect_width = 80
        self.check = [False]*3
        self.check_rect = [
            pygame.Rect(self.symbool_Rect.centerx-checkRect_width/2, self.symbool_Rect.top, checkRect_width, checkRect_width),
            pygame.Rect(self.symbool_Rect.centerx-checkRect_width/2, self.symbool_Rect.centery-checkRect_width/2, checkRect_width, checkRect_width),
            pygame.Rect(self.symbool_Rect.centerx-checkRect_width/2, self.symbool_Rect.bottom-checkRect_width, checkRect_width, checkRect_width),
        ]

    def teken_op(self, pos):
        """Teken een cirkel op pos, en een lijn vanaf de vorige positie."""
        tekenRadius = 50
        if self.ButtonRect.collidepoint(pos):
            if self.vorige_pos and self.ButtonRect.collidepoint(self.vorige_pos):
                pygame.draw.line(self.tekenvlak, 'green', self.vorige_pos, pos, tekenRadius * 2)
            pygame.draw.circle(self.tekenvlak, 'green', pos, tekenRadius)
            self.vorige_pos = pos

    def handle_event(self, event):
        """Verwerk muisevents voor vloeiend tekenen."""
        if self.klaar:
            return
        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            self.teken_op(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.vorige_pos = None  # ← reset bij loslaten

    def draw(self, mouse, mouse_pos):
        pygame.draw.rect(self.ondervlak, (200,200,200,10), self.ButtonRect, 0, 10)
        buttonVlak.blit(self.Kleursymbool, self.symbool_Rect)
        if self.klaar == False:
            # Cirkel op huidige pos (vangt klikken zonder bewegen op)
            if mouse[0] and self.ButtonRect.collidepoint(mouse_pos):
                pygame.draw.circle(self.tekenvlak, 'green', mouse_pos, 50)

            pygame.draw.rect(self.tekenvlak, 'blue', self.symbool_Rect, 2)
            for i, rect in enumerate(self.check_rect):
                pygame.draw.rect(self.tekenvlak, 'blue', rect, 1)
                if rect.collidepoint(mouse_pos) and mouse[0]:
                    self.check[i] = True

            if sum(self.check) == 3:
                print("Alles ingekleurd")
                self.klaar = True

            buttonVlak.blit(self.tekenvlak, (0,0))

Button1 = inKleurButton(Handdoek_leeg, Handdoek_kleur, buttonVlak, tekenVlak)

# GAMELOOP____________________________________________________________________________________
while running:
    mouse = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_justpressed = pygame.mouse.get_just_pressed()

    # ← events eerst verwerken, vóór draw
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        Button1.handle_event(event)  # ← muisbeweging vloeiend verwerken

    Button1.draw(mouse, mouse_pos)

    screen.fill((200,240,240))
    screen.blit(buttonVlak,(0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()