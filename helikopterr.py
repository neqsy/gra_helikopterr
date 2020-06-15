""" Moduł zawiera grę helikopterr"""

import math
import random
import pygame


SZEROKOSC = 600
WYSOKOSC = 600

BOMBA = "bomba.png"
TARCZA = "tarcza.png"

MENU = 0
ROZGRYWKA = 1
KONIEC = 2
WYSOKOSC_TEKSTU = 20


def napisz(tekst, x, y, rozmiar, screen):
    """Funkcja służy do umieszczania napisów w grze."""

    czcionka = pygame.font.SysFont("Arial", rozmiar)
    rysuj = czcionka.render(tekst, 1, Colors.CZERWONY)
    screen.blit(rysuj, (x, y))


def wyswietl_menu(screen):
    """Funkcja służy do wyświetlania menu w grze."""

    napisz("Naciśnij spację, aby zacząć", 90, 350, WYSOKOSC_TEKSTU, screen)
    napisz("STEROWANIE: strzałka do góry albo w dół", 90, 390, WYSOKOSC_TEKSTU, screen)
    grafika = pygame.image.load("logo.png")
    screen.blit(grafika, (90, 150))


def tworzenie_obiektow():
    """Funkcja służy do tworzenia obiektów(przeszkody, bomby, helikopter, tarcze) w grze."""
    
    gracz = Helikopter(270, 275)
    przeszkody = []
    bomby = []
    tarcze = []

    for i in range(21):
        przeszkody.append(Przeszkoda(i * SZEROKOSC / 20, SZEROKOSC / 20))
    for i in range(1):
        bomby.append(Sprite(BOMBA, i * SZEROKOSC))
    for i in range(1):
        tarcze.append(Sprite(TARCZA, i * SZEROKOSC))

    ruch_y = 0
    punkty = 0
    return ruch_y, punkty, gracz, przeszkody, bomby, tarcze


def wyswietl_rozgrywka(ruch_y, punkty, gracz, przeszkody, bomby, tarcze, screen):
    """Funkcja służy do wyświetlania rozgrywki w grze."""

    for p in przeszkody:  # rysowanie przeszkód
        p.ruch(0.5)
        p.rysuj(screen)
        if p.kolizja(gracz.ksztalt):
            stan_gry = KONIEC
            return stan_gry

    for p in przeszkody:  # sprawdzam czy przeszkoda miesci sie poza ekranem
        if p.wspolrzedna_x <= -p.szerokosc:
            przeszkody.remove(p)
            przeszkody.append((Przeszkoda(SZEROKOSC, SZEROKOSC / 20)))

    for b in bomby:
        b.ruch(0.9)
        b.rysuj(screen)
        if b.kolizja(gracz.ksztalt):
            if not gracz.tarcza:
                stan_gry = KONIEC
                return stan_gry
            else:
                gracz.tarcza = False
                bomby.remove(b)
                bomby.append((Sprite(BOMBA, SZEROKOSC)))

    for b in bomby:  # sprawdzam czy bomba miesci sie poza ekranem
        if b.wspolrzedna_x <= -b.szerokosc:
            bomby.remove(b)
            bomby.append((Sprite(BOMBA, SZEROKOSC)))

    for t in tarcze:  # rysowanie tarcz
        t.ruch(0.5)
        t.rysuj(screen)
        if t.kolizja(gracz.ksztalt):
            gracz.tarcza = True
            tarcze.remove(t)
            tarcze.append((Sprite(TARCZA, SZEROKOSC * 3)))

    for t in tarcze:  # sprawdzam czy tarcza miesci sie poza ekranem
        if t.wspolrzedna_x <= -t.szerokosc:
            tarcze.remove(t)
            tarcze.append((Sprite(TARCZA, SZEROKOSC * 3)))

    gracz.rysuj(screen)
    gracz.ruch(ruch_y)  # ruch gracza (góra, dół)

    napisz(f"PUNKTY: {round(punkty, 2)}", 50, 50, WYSOKOSC_TEKSTU, screen)
    stan_gry = ROZGRYWKA
    return stan_gry


def wyswietl_koniec(punkty):
    """Funkcja służy do wyświetlania tekstu po porażce w grze."""

    screen = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
    grafika = pygame.image.load("logo.png")
    screen.blit(grafika, (80, 30))
    napisz("Niestety przegrywasz", 50, 290, WYSOKOSC_TEKSTU, screen)
    napisz("Naciśnij spację, aby zagrać ponownie", 50, 350, WYSOKOSC_TEKSTU, screen)
    napisz(f'PUNKTY: {punkty:%.2f}', 50, 320, WYSOKOSC_TEKSTU, screen)


def wyswietlanie_gry():
    stan_gry = MENU
    screen = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
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
                    if stan_gry != ROZGRYWKA:
                        ruch_y, punkty, gracz, przeszkody, bomby, tarcze = tworzenie_obiektow()
                        stan_gry = ROZGRYWKA

        screen.fill((0, 0, 0))
        if stan_gry == MENU:
            wyswietl_menu(screen)
        elif stan_gry == ROZGRYWKA:
            punkty = punkty + math.fabs(ruch_y/10)
            if ruch_y == 0:
                punkty = 0
            stan_gry = wyswietl_rozgrywka(ruch_y, punkty, gracz, przeszkody, bomby, tarcze, screen)
        elif stan_gry == KONIEC:
            wyswietl_koniec(punkty)
        pygame.display.update()


class Colors:
    """Paleta barw."""

    # pylint: disable=too-few-public-methods
    CZERWONY = (255, 100, 100)
    FIOLETOWY = (203, 75, 22)


class Przeszkoda:
    """Klasa zawierająca właściwości i metody przeszkód."""
    
    def __init__(self, wspolrzedna_x, SZEROKOSC):
        self.wspolrzedna_x = wspolrzedna_x
        self.szerokosc = SZEROKOSC
        self.wspolrzedna_y_gora = 0
        self.wysokosc_gora = random.randint(110, 210)
        self.odstep = 210
        self.wspolrzedna_y_dol = self.wysokosc_gora + self.odstep
        self.wysokosc_dol = WYSOKOSC - self.wspolrzedna_y_dol
        self.kolor = Colors.FIOLETOWY
        self.ksztalt_gora = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y_gora),
                                        int(self.szerokosc), int(self.wysokosc_gora))
        self.ksztalt_dol = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y_dol),
                                       int(self.szerokosc), int(self.wysokosc_dol))

    def rysuj(self, screen):
        pygame.draw.rect(screen, self.kolor, self.ksztalt_gora, 0)
        pygame.draw.rect(screen, self.kolor, self.ksztalt_dol, 0)

    def ruch(self, predkosc):
        self.wspolrzedna_x = self.wspolrzedna_x - predkosc
        self.ksztalt_gora = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y_gora),
                                        int(self.szerokosc), int(self.wysokosc_gora))
        self.ksztalt_dol = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y_dol),
                                       int(self.szerokosc), int(self.wysokosc_dol))

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
        self.szerokosc = 50
        self.wysokosc = 30
        self.ksztalt = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y),
                                   int(self.szerokosc), int(self.wysokosc))
        self.grafika = pygame.image.load("helikopter.png")
        self.grafika_z_tarcza = pygame.image.load("helikopter_tarcza.png")
        self.tarcza = False

    def rysuj(self, screen):
        if self.tarcza:
            screen.blit(self.grafika_z_tarcza, (int(self.wspolrzedna_x), int(self.wspolrzedna_y)))
        else:
            screen.blit(self.grafika, (int(self.wspolrzedna_x), int(self.wspolrzedna_y)))

    def ruch(self, predkosc):
        self.wspolrzedna_y = self.wspolrzedna_y + predkosc
        self.ksztalt.y = int(self.wspolrzedna_y)


class Sprite:
    """Klasa zawierająca właściwości i metody bomby oraz tarczy."""
    
    def __init__(self, obrazek, wspolrzedna_x):
        self.wspolrzedna_x = wspolrzedna_x
        self.wspolrzedna_y = random.randint(220, 275)

        self.grafika = pygame.image.load(obrazek)
        self.szerokosc = self.grafika.get_width()
        self.wysokosc = self.grafika.get_height()

        self.ksztalt = pygame.Rect(int(self.wspolrzedna_x), int(self.wspolrzedna_y),
                                   int(self.szerokosc), int(self.wysokosc))

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


def main():
    pygame.init()
    pygame.display.set_caption("Helikopterr")
    wyswietlanie_gry()


if __name__ == '__main__':
    main()
