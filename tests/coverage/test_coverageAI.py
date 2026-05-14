import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sistemrezervareavion import SistemRezervareAvion


class TestableSistemRezervareAvion(SistemRezervareAvion):
    """Clasa wrapper pentru a oferi implementari 'dummy' ale metodelor interne."""
    def __init__(self):
        super().__init__()
        self.echilibru_rezultat = True  # Controlam rezultatul pentru teste
        
    def _litera_la_coloana(self, litera):
        return self.LITERE_VALIDE.index(litera)
        
    def _verifica_echilibru(self, coloana):
        return self.echilibru_rezultat
        
    def _calculeaza_pret(self, rand, varsta_pasager, are_bagaj_cala):
        return 120.0


class TestRezervaLoc(unittest.TestCase):
    def setUp(self):
        self.sistem = TestableSistemRezervareAvion()

    # --- Decizia 1: Validare rand tip (Condition Coverage: C1 T/F, C2 T/F) ---
    def test_rand_tip_gresit_string(self):
        # C1 (not isinstance(int)) = True, C2 (isinstance(bool)) = False
        with self.assertRaisesRegex(TypeError, "Randul trebuie sa fie un numar intreg"):
            self.sistem.rezerva_loc("1", "A", 30, False)

    def test_rand_tip_gresit_bool(self):
        # C1 = False (in python isinstance(True, int) este True), C2 = True
        with self.assertRaisesRegex(TypeError, "Randul trebuie sa fie un numar intreg"):
            self.sistem.rezerva_loc(True, "A", 30, False)

    # --- Decizia 2: Validare rand valoare (Condition Coverage: rand < 1, rand > NR_RANDURI) ---
    def test_rand_valoare_prea_mica(self):
        # rand < 1 = True
        with self.assertRaisesRegex(ValueError, "Rand invalid"):
            self.sistem.rezerva_loc(0, "A", 30, False)

    def test_rand_valoare_prea_mare(self):
        # rand > 10 = True
        with self.assertRaisesRegex(ValueError, "Rand invalid"):
            self.sistem.rezerva_loc(11, "A", 30, False)

    # --- Decizia 3: Validare litera tip si lungime (Condition Coverage) ---
    def test_litera_tip_gresit(self):
        # C1 (not isinstance(str)) = True
        with self.assertRaisesRegex(ValueError, "Litera locului trebuie sa fie un singur caracter"):
            self.sistem.rezerva_loc(1, 123, 30, False)

    def test_litera_lungime_gresita(self):
        # C1 = False, C2 (len != 1) = True
        with self.assertRaisesRegex(ValueError, "Litera locului trebuie sa fie un singur caracter"):
            self.sistem.rezerva_loc(1, "AB", 30, False)

    # --- Decizia 4: Validare litera valoare ---
    def test_litera_invalida(self):
        with self.assertRaisesRegex(ValueError, "Loc invalid"):
            self.sistem.rezerva_loc(1, "Z", 30, False)

    # --- Decizia 5: Validare varsta tip (Condition Coverage) ---
    def test_varsta_tip_gresit_string(self):
        # C1 = True, C2 = False
        with self.assertRaisesRegex(TypeError, "Varsta trebuie sa fie un numar intreg"):
            self.sistem.rezerva_loc(1, "A", "30", False)

    def test_varsta_tip_gresit_bool(self):
        # C1 = False, C2 = True
        with self.assertRaisesRegex(TypeError, "Varsta trebuie sa fie un numar intreg"):
            self.sistem.rezerva_loc(1, "A", True, False)

    # --- Decizia 6: Validare varsta valoare ---
    def test_varsta_negativa(self):
        with self.assertRaisesRegex(ValueError, "Varsta nu poate fi negativa"):
            self.sistem.rezerva_loc(1, "A", -5, False)

    # --- Decizia 7: Validare bagaj cala tip ---
    def test_bagaj_tip_gresit(self):
        with self.assertRaisesRegex(TypeError, "are_bagaj_cala trebuie sa fie True sau False"):
            self.sistem.rezerva_loc(1, "A", 30, "Da")

    # --- Decizia 8: Verificare disponibilitate (Branch Coverage) ---
    def test_loc_ocupat(self):
        # Ocupam locul manual inainte
        self.sistem.locuri_ocupate[0][0] = True # Rand 1, Litera A
        rezultat = self.sistem.rezerva_loc(1, "A", 30, False)
        self.assertEqual(rezultat, "Ocupat")

    # --- Decizia 9: Verificare echilibru (Branch Coverage) ---
    def test_dezechilibru(self):
        # Setam mock-ul sa returneze False la echilibru
        self.sistem.echilibru_rezultat = False
        rezultat = self.sistem.rezerva_loc(1, "A", 30, False)
        self.assertEqual(rezultat, "Dezechilibru")

    # --- HAPPY PATH: Toate False, Statement Coverage si Branch Coverage complet ---
    def test_rezervare_reusita(self):
        rezultat = self.sistem.rezerva_loc(1, "A", 30, False)
        
        # Verificam ca rezervarea a reusit si s-a returnat pretul corect
        self.assertEqual(rezultat, 120.0)
        
        # Verificam ca starea interna s-a actualizat (Statement coverage pt ultimele linii)
        self.assertTrue(self.sistem.locuri_ocupate[0][0])
        self.assertEqual(len(self.sistem.rezervari), 1)
        self.assertEqual(self.sistem.rezervari[0]["pret"], 120.0)

if __name__ == "__main__":
    unittest.main()