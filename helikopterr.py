import random
import pygame
import os
import math

pygame.init()

SZER = 600
WYS = 600
COPOKAZUJE = "menu"

screen = pygame.display.set_mode((SZER, WYS))


def napisz(tekst, x, y, rozmiar):
    """Funkcja służy do umieszczania napisów w grze"""

    cz = pygame.font.SysFont("Arial", rozmiar)
    rend = cz.render(tekst, 1, (255, 100, 100))
    screen.blit(rend, (x, y))


class Przeszkoda:

    def __init__(self, x, szerokosc):
        self.x = x
        self.szerokosc = szerokosc
        self.y_gora = 0
        self.wys_gora = random.randint(150, 250)
        self.odstep = 193
        self.y_dol = self.wys_gora + self.odstep
        self.wys_dol = WYS - self.y_dol
        self.kolor = (173, 140, 190)
        self.ksztalt_gora = pygame.Rect(int(self.x), int(self.y_gora), int(self.szerokosc), int(self.wys_gora))
        self.ksztalt_dol = pygame.Rect(int(self.x), int(self.y_dol), int(self.szerokosc), int(self.wys_dol))

    def rysuj(self):
        pygame.draw.rect(screen, self.kolor, self.ksztalt_gora, 0)
        pygame.draw.rect(screen, self.kolor, self.ksztalt_dol, 0)

    def ruch(self, v):
        self.x = self.x - v
        self.ksztalt_gora = pygame.Rect(int(self.x), int(self.y_gora), int(self.szerokosc), int(self.wys_gora))
        self.ksztalt_dol = pygame.Rect(int(self.x), int(self.y_dol), int(self.szerokosc), int(self.wys_dol))

    def kolizja(self, player):
        if self.ksztalt_gora.colliderect(player) or self.ksztalt_dol.colliderect(player):
            return True
        else:
            return False

class Helikopter:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wysokosc = 30
        self.szerokosc = 50
        self.ksztalt = pygame.Rect(int(self.x), int(self.y), int(self.szerokosc), int(self.wysokosc))
        self.grafika = pygame.image.load(os.path.join("helikopter.png"))

    def rysuj(self):
        screen.blit(self.grafika, (int(self.x), int(self.y)))

    def ruch(self, v):
        self.y = self.y + v


przeszkody = []
for i in range(21):
        przeszkody.append(Przeszkoda(i*SZER/20, SZER/20))

gracz = Helikopter(0, 0)
dy = 0 #określenie w którym kierunku porusza się helikopter
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -0.3
            if event.key == pygame.K_DOWN:
                dy = 0.3
            if event.key == pygame.K_SPACE:
                if COPOKAZUJE != "rozgrywka":
                    gracz = Helikopter(275, 275)
                    dy = 0
                    COPOKAZUJE = "rozgrywka"
                    punkty = 0

    screen.fill((0, 0, 0))
    if COPOKAZUJE == "menu":
        napisz("Naciśnij spację, aby zacząć", 90, 350, 20)
        grafika = pygame.image.load(os.path.join("logo.png"))
        screen.blit(grafika, (90, 150))

    elif COPOKAZUJE == "rozgrywka":
        for p in przeszkody:
            p.ruch(0.5)
            p.rysuj()
            if p.kolizja(gracz.ksztalt):
                COPOKAZUJE = "koniec"
        for p in przeszkody:
            if p.x <= -p.szerokosc:
                przeszkody.remove(p)
                przeszkody.append((Przeszkoda(SZER, SZER/20)))
                punkty = punkty + math.fabs(dy)
        gracz.rysuj()
        gracz.ruch(dy)

        napisz(str(punkty), 50, 50, 20)
    elif COPOKAZUJE == "koniec":
        grafika = pygame.image.load(os.path.join("logo.png"))
        screen.blit(grafika, (80, 30))
        napisz("Niestety przegrywasz", 50, 290, 20)
        napisz("Naciśnij spację, aby zagrać ponownie", 50, 350, 20)
        napisz("Twój wynik to: " + str(punkty), 50, 320, 20)
    pygame.display.update()
