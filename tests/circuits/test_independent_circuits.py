import unittest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sistemrezervareavion import SistemRezervareAvion

# functie rezerva_loc

class TestRezervareLoc(unittest.TestCase):
    def test_tip_rand_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc("1", "F", 20, False)

    def test_rand_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(20, "F", 20, False)

    def test_tip_litera_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(2, 1, 20, False)

    def test_litera_invalida(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(2, "G", 20, False)

    def test_tip_varsta_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc(2, "A", "10", False)

    def test_varsta_invalida(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(2, "A", -2, False)

    def test_bagaj_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc(2, "A", 20, "False")

    def test_loc_ocupat(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(3,"A", 20, False)
        rez = sistem.rezerva_loc(3,"A", 20, False)
        self.assertEqual(rez, "Ocupat")

    def test_dezechilibru(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(3, "A", 20, False)
        sistem.rezerva_loc(4, "A", 25, True)
        sistem.rezerva_loc(1, "B", 50, True)
        rez = sistem.rezerva_loc(6, "A", 20, False)
        self.assertEqual(rez, "Dezechilibru")
        

    def test_rezervare_valida(self):
        sistem = SistemRezervareAvion()
        pret = sistem.rezerva_loc(3,"A", 20, False)
        self.assertTrue(isinstance(pret, float))

    
# functie anuleaza_rezervare
class TestAnulareRezervare(unittest.TestCase):
    def test_tip_rand_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.anuleaza_rezervare(True, "A")

    def test_rand_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(25, "A")

    def test_tip_litera_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(2, 1)

    def test_litera_invalida(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(2, "G")

    def test_loc_liber(self):
        sistem = SistemRezervareAvion()
        self.assertFalse(sistem.anuleaza_rezervare(1, "A"))

    # intra o singura data in bucla
    def test_elibereaza_primul_loc(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A",20,False)
        self.assertTrue(sistem.anuleaza_rezervare(1, "A"))

    # trece prin bucla de mai multe ori
    def test_elibereaza_ultimul_loc(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1,"A",20,False)
        sistem.rezerva_loc(2,"D",20,False)
        sistem.rezerva_loc(10,"F",20,False)
        self.assertTrue(sistem.anuleaza_rezervare(10,"F"))

    

# functie locuri_disponibile
class TestLocuriDisponibile(unittest.TestCase):
    def test_toate_libere(self):
        sistem = SistemRezervareAvion()
        locuri = sistem.locuri_disponibile()
        self.assertEqual(len(locuri), 60)

    # exista locuri ocupate in avion 
    def test_locuri_ocupate(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 20, False)
        locuri = sistem.locuri_disponibile()
        self.assertEqual(len(locuri), 59)
        self.assertNotIn((1,"A"), locuri)
        self.assertIn((2,"A"), locuri)

