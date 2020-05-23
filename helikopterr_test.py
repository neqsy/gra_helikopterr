"""Testy modułu helikopterr."""

import unittest

import helikopterr


class PrzeszkodaTest(unittest.TestCase):

    def setUp(self):
        self.Przeszkoda = helikopterr.Przeszkoda(wspolrzedna_x=349, szerokosc=32)

    def test_ruch(self):
        old_wspolrzedna_x = self.Przeszkoda.wspolrzedna_x
        self.Przeszkoda.ruch(5)
        self.assertEqual(old_wspolrzedna_x - 5, self.Przeszkoda.wspolrzedna_x)
        self.assertEqual(self.Przeszkoda.ksztalt_gora.x, 344)
        self.assertEqual(self.Przeszkoda.ksztalt_dol.x, 344)

    def test_kolizja(self):
        player = helikopterr.Helikopter(310, 0)
        gracz = player.ksztalt
        self.assertTrue(self.Przeszkoda.kolizja(gracz), "Nie ma kolizji")


class HelikopterTest(unittest.TestCase):

    def setUp(self):
        self.Helikopter = helikopterr.Helikopter(wspolrzedna_x=349, wspolrzedna_y=50)

    def test_ruch(self):
        old_wspolrzedna_y = self.Helikopter.wspolrzedna_y
        self.Helikopter.ruch(5)
        self.assertEqual(old_wspolrzedna_y + 5, self.Helikopter.wspolrzedna_y)


if __name__ == '__main__':
    unittest.main()
    
