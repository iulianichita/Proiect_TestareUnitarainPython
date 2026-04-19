import unittest
import io
from contextlib import redirect_stdout
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sistemrezervareavion import SistemRezervareAvion


class Test01Init(unittest.TestCase):
    # [S] Statement coverage
    def test_i1_stare_initiala(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(len(sistem.locuri_ocupate), 10)
        self.assertTrue(all(len(rand) == 6 for rand in sistem.locuri_ocupate))
        self.assertTrue(all(not loc for rand in sistem.locuri_ocupate for loc in rand))
        self.assertEqual(sistem.pret_baza, 100.0)
        self.assertEqual(sistem.rezervari, [])


class Test02LiteraLaColoana(unittest.TestCase):
    # [S]
    def test_l2_litera_mica(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(sistem._litera_la_coloana("f"), 5)


class Test03CalculeazaPret(unittest.TestCase):
    # [S]
    def test_p1_business_infant(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(sistem._calculeaza_pret(1, 1, False), 15.0)

    def test_p2_copil_cu_bagaj(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(sistem._calculeaza_pret(5, 10, True), 70.0)

    # [B]
    def test_p3_adult_fara_bagaj(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(sistem._calculeaza_pret(5, 30, False), 100.0)

    # [C]
    def test_p4_senior(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(sistem._calculeaza_pret(5, 65, False), 50.0)


class Test04CalculeazaEchilibru(unittest.TestCase):
    # [S]
    def test_e1_avion_gol(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(sistem._calculeaza_echilibru(), (0, 0))

    # [B] + [C]
    def test_e2_locuri_pe_ambele_parti(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)
        sistem.rezerva_loc(1, "D", 30, False)
        self.assertEqual(sistem._calculeaza_echilibru(), (1, 1))


class Test05VerificaEchilibru(unittest.TestCase):
    # [S]
    def test_v1_stanga_permisa(self):
        sistem = SistemRezervareAvion()
        self.assertTrue(sistem._verifica_echilibru(0))

    def test_v2_dreapta_permisa(self):
        sistem = SistemRezervareAvion()
        self.assertTrue(sistem._verifica_echilibru(4))

    # [B] + [C]
    def test_v3_stanga_refuzata(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)
        sistem.rezerva_loc(2, "B", 30, False)
        sistem.rezerva_loc(3, "C", 30, False)
        self.assertFalse(sistem._verifica_echilibru(0))


class Test06RezervaLoc(unittest.TestCase):
    # [S] + [B]
    def test_r1_rand_tip_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc("1", "A", 30, False)

    def test_r2_rand_interval_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(0, "A", 30, False)

    def test_r3_litera_format_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(1, "AB", 30, False)

    def test_r4_litera_domeniu_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(1, "Z", 30, False)

    def test_r5_varsta_tip_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc(1, "A", "30", False)

    def test_r6_varsta_negativa(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(1, "A", -1, False)

    def test_r7_bagaj_tip_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc(1, "A", 30, "da")

    def test_r8_rezervare_valida(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(sistem.rezerva_loc(1, "A", 30, True), 170.0)

    def test_r9_loc_ocupat(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)
        self.assertEqual(sistem.rezerva_loc(1, "A", 30, False), "Ocupat")

    def test_r10_dezechilibru(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)
        sistem.rezerva_loc(2, "B", 30, False)
        sistem.rezerva_loc(3, "C", 30, False)
        self.assertEqual(sistem.rezerva_loc(4, "A", 30, False), "Dezechilibru")

    # [C]
    def test_r1_rand_nu_este_int(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc("1", "A", 30, False)

    def test_r2_rand_este_bool(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc(True, "A", 30, False)

    def test_r3_rand_sub_limita(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(0, "A", 30, False)

    def test_r4_rand_peste_limita(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(11, "A", 30, False)

    def test_r5_litera_nu_este_string(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(1, 5, 30, False)

    def test_r6_litera_are_lungime_invalida(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(1, "AB", 30, False)

    def test_r7_litera_nu_este_in_domeniu(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(1, "Z", 30, False)

    def test_r8_varsta_nu_este_int(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc(1, "A", "30", False)

    def test_r9_varsta_este_bool(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc(1, "A", True, False)

    def test_r10_varsta_negativa(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.rezerva_loc(1, "A", -1, False)

    def test_r11_bagaj_nu_este_bool(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.rezerva_loc(1, "A", 30, "da")

    def test_r12_rezervare_valida(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(sistem.rezerva_loc(1, "A", 30, True), 170.0)

    def test_r13_loc_ocupat(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)
        self.assertEqual(sistem.rezerva_loc(1, "A", 40, True), "Ocupat")

    def test_r14_dezechilibru(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)
        sistem.rezerva_loc(2, "B", 30, False)
        sistem.rezerva_loc(3, "C", 30, False)
        self.assertEqual(sistem.rezerva_loc(4, "A", 30, False), "Dezechilibru")


class Test07AnuleazaRezervare(unittest.TestCase):
    # [S] + [B]
    def test_a1_rand_tip_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.anuleaza_rezervare(True, "A")

    def test_a2_rand_valoare_invalida(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(11, "A")

    def test_a3_litera_format_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(1, "AB")

    def test_a4_litera_domeniu_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(1, "Z")

    def test_a5_loc_deja_liber(self):
        sistem = SistemRezervareAvion()
        self.assertFalse(sistem.anuleaza_rezervare(1, "A"))

    def test_a6_anulare_reusita(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)
        self.assertTrue(sistem.anuleaza_rezervare(1, "A"))

    # [C]
    def test_a1_rand_nu_este_int(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.anuleaza_rezervare("1", "A")

    def test_a2_rand_este_bool(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(TypeError):
            sistem.anuleaza_rezervare(True, "A")

    def test_a3_rand_sub_limita(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(0, "A")

    def test_a4_rand_peste_limita(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(11, "A")

    def test_a5_litera_nu_este_string(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(1, 5)

    def test_a6_litera_are_lungime_invalida(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(1, "AB")

    def test_a7_litera_nu_este_in_domeniu(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.anuleaza_rezervare(1, "Z")

    def test_a8_loc_deja_liber(self):
        sistem = SistemRezervareAvion()
        self.assertFalse(sistem.anuleaza_rezervare(1, "A"))

    def test_a9_anulare_reusita(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)
        self.assertTrue(sistem.anuleaza_rezervare(1, "A"))


class Test08EsteLocDisponibil(unittest.TestCase):
    # [S] + [B] + [C]
    def test_e1_rand_invalid(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.este_loc_disponibil(0, "A")

    def test_e2_litera_invalida(self):
        sistem = SistemRezervareAvion()
        with self.assertRaises(ValueError):
            sistem.este_loc_disponibil(1, "Z")

    def test_e3_loc_liber(self):
        sistem = SistemRezervareAvion()
        self.assertTrue(sistem.este_loc_disponibil(1, "A"))


class Test09LocuriDisponibile(unittest.TestCase):
    # [S]
    def test_ld1_avion_gol(self):
        sistem = SistemRezervareAvion()
        locuri = sistem.locuri_disponibile()

        self.assertEqual(len(locuri), 60)
        self.assertEqual(locuri[0], (1, "A"))
        self.assertEqual(locuri[-1], (10, "F"))

    # [B] + [C]
    def test_ld2_exista_si_locuri_ocupate(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)

        locuri = sistem.locuri_disponibile()

        self.assertEqual(len(locuri), 59)
        self.assertNotIn((1, "A"), locuri)
        self.assertIn((1, "B"), locuri)


class Test10NrLocuriDisponibile(unittest.TestCase):
    # [S]
    def test_nld1_avion_gol(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(sistem.nr_locuri_disponibile(), 60)

    # [B] + [C]
    def test_nld2_exista_loc_ocupat(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)
        self.assertEqual(sistem.nr_locuri_disponibile(), 59)


class Test11NrLocuriOcupate(unittest.TestCase):
    # [S] + [B] + [C]
    def test_nlo1_avion_gol(self):
        sistem = SistemRezervareAvion()
        self.assertEqual(sistem.nr_locuri_ocupate(), 0)


class Test12AvionPlin(unittest.TestCase):
    # [S]
    def test_ap1_avion_plin(self):
        sistem = SistemRezervareAvion()

        for rand in range(sistem.NR_RANDURI):
            for col in range(sistem.NR_COLOANE):
                sistem.locuri_ocupate[rand][col] = True

        self.assertTrue(sistem.avion_plin())

    # [B] + [C]
    def test_ap2_avion_neplin(self):
        sistem = SistemRezervareAvion()
        self.assertFalse(sistem.avion_plin())


class Test13Reseteaza(unittest.TestCase):
    # [S] + [B] + [C]
    def test_rst1_reseteaza_dupa_rezervari(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)
        sistem.rezerva_loc(1, "D", 30, False)
        sistem.rezerva_loc(2, "B", 30, True)

        self.assertTrue(
            any(
                sistem.locuri_ocupate[rand][col]
                for rand in range(sistem.NR_RANDURI)
                for col in range(sistem.NR_COLOANE)
            )
        )
        self.assertGreater(len(sistem.rezervari), 0)

        sistem.reseteaza()

        self.assertTrue(
            all(
                not sistem.locuri_ocupate[rand][col]
                for rand in range(sistem.NR_RANDURI)
                for col in range(sistem.NR_COLOANE)
            )
        )
        self.assertEqual(sistem.rezervari, [])


class Test14VizualizeazaAvion(unittest.TestCase):
    # [S] + [B] + [C]
    def test_viz1_exista_loc_ocupat(self):
        sistem = SistemRezervareAvion()
        sistem.rezerva_loc(1, "A", 30, False)

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            sistem.vizualizeaza_avion()

        rezultat = buffer.getvalue()
        linii = rezultat.splitlines()

        self.assertEqual(linii[0], "1__ ___")
        self.assertTrue(all(linie == "___ ___" for linie in linii[1:]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
