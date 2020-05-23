"""Testy modułu helikopterr."""

import unittest

import helikopterr


class PrzeszkodaTest(unittest.TestCase):

    def setUp(self):
        self.Przeszkoda = helikopterr.Przeszkoda(x=349, szerokosc=32)

    def test_ruch(self):
        old_x = self.Przeszkoda.x
        self.Przeszkoda.ruch(5)
        self.assertEqual(old_x - 5, self.Przeszkoda.x)
        self.assertEqual(self.Przeszkoda.ksztalt_gora.x, 344)
        self.assertEqual(self.Przeszkoda.ksztalt_dol.x, 344)

    def test_kolizja(self):
        player = helikopterr.Helikopter(310, 0)
        gracz = player.ksztalt
        self.assertTrue(self.Przeszkoda.kolizja(gracz), "Nie ma kolizji")


class HelikopterTest(unittest.TestCase):

    def setUp(self):
        self.Helikopter = helikopterr.Helikopter(x=349, y=50)

    def test_ruch(self):
        old_y = self.Helikopter.y
        self.Helikopter.ruch(5)
        self.assertEqual(old_y + 5, self.Helikopter.y)


if __name__ == '__main__':
    unittest.main()