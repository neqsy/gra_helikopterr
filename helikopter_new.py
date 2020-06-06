import os
import math
import random
import pygame


SZER = 600
WYS = 600


def napisz(tekst, x, y, rozmiar, screen):
    """Funkcja służy do umieszczania napisów w grze."""

    czcionka = pygame.font.SysFont("Arial", rozmiar)
    rend = czcionka.render(tekst, 1, (255, 100, 100))
    screen.blit(rend, (x, y))


class Przeszkoda:
    """Klasa zawierająca właściwości i metody przeszkód."""
    def __init__(self, wspolrzedna_x, szerokosc):
        self.wspolrzedna_x = wspolrzedna_x
        self.szerokosc = szerokosc
        self.wspolrzedna_y_gora = 0
        self.wys_gora = random.randint(110, 210)
        self.odstep = 210
        self.wspolrzedna_y_dol = self.wys_gora + self.odstep
        self.wys_dol = WYS - self.wspolrzedna_y_dol
        self.kolor = (173, 140, 190)
        self.ksztalt_gora = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y_gora),
                                        int(self.szerokosc), int(self.wys_gora))
        self.ksztalt_dol = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y_dol),
                                       int(self.szerokosc), int(self.wys_dol))

    def rysuj(self, screen):
        pygame.draw.rect(screen, self.kolor, self.ksztalt_gora, 0)
        pygame.draw.rect(screen, self.kolor, self.ksztalt_dol, 0)

    def ruch(self, predkosc):
        self.wspolrzedna_x = self.wspolrzedna_x - predkosc
        self.ksztalt_gora = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y_gora),
                                        int(self.szerokosc), int(self.wys_gora))
        self.ksztalt_dol = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y_dol),
                                       int(self.szerokosc), int(self.wys_dol))

    def kolizja(self, player):
        if self.ksztalt_gora.colliderect(player) or self.ksztalt_dol.colliderect(player):
            return True
        else:
            return False


class Helikopter:
    """Klasa zawierająca właściwości i metody helikoptera."""
    def __init__(self, wspolrzedna_x, wspolrzedna_y):
        self.wspolrzedna_x = wspolrzedna_x
        self.wspolrzedna_y = wspolrzedna_y
        self.wysokosc = 30
        self.szerokosc = 50
        self.ksztalt = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y),
                                   int(self.szerokosc), int(self.wysokosc))
        self.grafika = pygame.image.load(os.path.join("helikopter.png"))
        self.grafika_z_tarcza = pygame.image.load(os.path.join("helikopter_tarcza.png"))

    def rysuj(self, screen):
        screen.blit(self.grafika, (int(self.wspolrzedna_x), int(self.wspolrzedna_y)))

    def rysuj_z_tarcza(self, screen):
        screen.blit(self.grafika_z_tarcza, (int(self.wspolrzedna_x), int(self.wspolrzedna_y)))

    def ruch(self, predkosc):
        self.wspolrzedna_y = self.wspolrzedna_y + predkosc
        self.ksztalt.y = int(self.wspolrzedna_y)


class Bomba:
    """Klasa zawierająca właściwości i metody bomby."""
    def __init__(self, wspolrzedna_x):
        self.wspolrzedna_x = wspolrzedna_x
        self.wspolrzedna_y = random.randint(220, 275)
        self.wysokosc = 13
        self.szerokosc = 17
        self.ksztalt = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y),
                                   int(self.szerokosc), int(self.wysokosc))
        self.grafika = pygame.image.load(os.path.join("bomba.png"))

    def rysuj(self, screen):
        screen.blit(self.grafika, (int(self.wspolrzedna_x), int(self.wspolrzedna_y)))

    def ruch(self, predkosc):
        self.wspolrzedna_x = self.wspolrzedna_x - predkosc
        self.ksztalt = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y),
                                   int(self.szerokosc), int(self.wysokosc))

    def kolizja(self, player):
        if self.ksztalt.colliderect(player):
            return True
        else:
            return False


class Tarcza:
    """Klasa zawierająca właściwości i metody tarczy."""
    def __init__(self, wspolrzedna_x):
        self.wspolrzedna_x = wspolrzedna_x
        self.wspolrzedna_y = random.randint(220, 285)
        self.wysokosc = 17
        self.szerokosc = 17
        self.ksztalt = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y),
                                   int(self.szerokosc), int(self.wysokosc))
        self.grafika = pygame.image.load(os.path.join("tarcza.png"))
        self.brak_grafiki = pygame.image.load(os.path.join("brak_tarczy.png"))

    def rysuj(self, screen):
        screen.blit(self.grafika, (int(self.wspolrzedna_x), int(self.wspolrzedna_y)))

    def ruch(self, predkosc):
        self.wspolrzedna_x = self.wspolrzedna_x - predkosc
        self.ksztalt = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y),
                                   int(self.szerokosc), int(self.wysokosc))

    def kolizja(self, player):
        if self.ksztalt.colliderect(player):
            return True
        else:
            return False


def wyswietlanie_gry():
    copokazuje = "menu"
    screen = pygame.display.set_mode((SZER, WYS))
    ruch_y = 0  # określenie w którym kierunku porusza się helikopter (góra, dół)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ruch_y = -0.3
                if event.key == pygame.K_DOWN:
                    ruch_y = 0.3
                if event.key == pygame.K_SPACE:
                    if copokazuje != "rozgrywka":
                        gracz = Helikopter(270, 275)
                        przeszkody = []
                        bomby = []
                        tarcze = []
                        tarcza = False

                        for i in range(21):
                            przeszkody.append(Przeszkoda(i * SZER / 20, SZER / 20))
                        for i in range(1):
                            bomby.append(Bomba(i * SZER))
                        for i in range(1):
                            tarcze.append(Tarcza(i * SZER))

                        ruch_y = 0
                        copokazuje = "rozgrywka"
                        punkty = 0
        screen.fill((0, 0, 0))
        if copokazuje == "menu":
            napisz("Naciśnij spację, aby zacząć", 90, 350, 20, screen)
            napisz("STEROWANIE: strzałka do góry albo w dół", 90, 390, 20, screen)
            grafika = pygame.image.load(os.path.join("logo.png"))
            screen.blit(grafika, (90, 150))

        elif copokazuje == "rozgrywka":

            for p in przeszkody:  # rysowanie przeszkód
                p.ruch(0.5)
                p.rysuj(screen)
                if p.kolizja(gracz.ksztalt):
                    copokazuje = "koniec"

            for p in przeszkody:  # sprawdzam czy przeszkoda miesci sie poza ekranem
                if p.wspolrzedna_x <= -p.szerokosc:
                    przeszkody.remove(p)
                    przeszkody.append((Przeszkoda(SZER, SZER / 20)))
                    punkty = punkty + math.fabs(ruch_y)

            for b in bomby:
                b.ruch(0.73)
                b.rysuj(screen)
                if b.kolizja(gracz.ksztalt):
                    if not tarcza:
                        copokazuje = "koniec"
                    elif tarcza:
                        tarcza = False

            for b in bomby:  # sprawdzam czy bomba miesci sie poza ekranem
                if b.wspolrzedna_x <= -b.szerokosc:
                    bomby.remove(b)
                    bomby.append((Bomba(SZER)))
            for t in tarcze:  # rysowanie tarcz
                t.ruch(0.5)
                t.rysuj(screen)
                if t.kolizja(gracz.ksztalt):
                    tarcza = True
                    tarcze.remove(t)
                    tarcze.append((Tarcza(SZER*3)))

            for t in tarcze:  # sprawdzam czy tarcza miesci sie poza ekranem
                if t.wspolrzedna_x <= -t.szerokosc:
                    tarcze.remove(t)
                    tarcze.append((Tarcza(SZER*3)))
            if not tarcza:
                gracz.rysuj(screen)
            if tarcza:
                gracz.rysuj_z_tarcza(screen)

            gracz.ruch(ruch_y)  # ruch gracza (góra, dół)

            napisz("PUNKTY: " + str(round(punkty, 2)), 50, 50, 20, screen)
        elif copokazuje == "koniec":
            grafika = pygame.image.load(os.path.join("logo.png"))
            screen.blit(grafika, (80, 30))
            napisz("Niestety przegrywasz", 50, 290, 20, screen)
            napisz("Naciśnij spację, aby zagrać ponownie", 50, 350, 20, screen)
            napisz("Twój wynik to: " + str(round(punkty, 2)), 50, 320, 20, screen)
        pygame.display.update()


def main():
    pygame.init()
    wyswietlanie_gry()


if __name__ == '__main__':
    main()
