"""Testy modułu helikopterr."""

import unittest

import helikopterr


class PrzeszkodaTest(unittest.TestCase):

    def setUp(self):
        self.przeszkoda = helikopterr.Przeszkoda(wspolrzedna_x=349, SZEROKOSC=600)

    def test_ruch(self):
        old_wspolrzedna_x = self.przeszkoda.wspolrzedna_x
        self.przeszkoda.ruch(5)
        self.assertEqual(old_wspolrzedna_x - 5, self.przeszkoda.wspolrzedna_x)
        self.assertEqual(self.przeszkoda.ksztalt_gora.x, 344)
        self.assertEqual(self.przeszkoda.ksztalt_dol.x, 344)

    def test_kolizja(self):
        player = helikopterr.Helikopter(349, 50)
        gracz = player.ksztalt
        self.assertTrue(self.przeszkoda.kolizja(gracz), "Nie ma kolizji")


class HelikopterTest(unittest.TestCase):

    def setUp(self):
        self.helikopter = helikopterr.Helikopter(wspolrzedna_x=349, wspolrzedna_y=50)

    def test_ruch(self):
        old_wspolrzedna_y = self.helikopter.wspolrzedna_y
        self.helikopter.ruch(5)
        self.assertEqual(old_wspolrzedna_y + 5, self.helikopter.wspolrzedna_y)


class SpriteTest(unittest.TestCase):

    def setUp(self):
        self.sprite = helikopterr.Sprite("bomba.png", 349)

    def test_ruch(self):
        old_wspolrzedna_x = self.sprite.wspolrzedna_x
        self.sprite.ruch(5)
        self.assertEqual(old_wspolrzedna_x - 5, self.sprite.wspolrzedna_x)
        self.assertEqual(self.sprite.ksztalt.x, 344)

    def test_kolizja(self):

        self.sprite.ksztalt.x = 100
        self.sprite.ksztalt.y = 270
        self.sprite.wspolrzedna_x = 100
        self.sprite.wspolrzedna_y = 270

        player = helikopterr.Helikopter(100, 270)

        self.assertTrue(self.sprite.kolizja(player.ksztalt), "Nie ma kolizji")

        self.sprite.ruch(self.sprite.szerokosc+1)
        self.assertFalse(self.sprite.kolizja(player.ksztalt), "Jest kolizja, a nie powinno być")


if __name__ == '__main__':
    unittest.main()
