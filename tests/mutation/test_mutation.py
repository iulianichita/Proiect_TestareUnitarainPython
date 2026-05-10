import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import pytest
from sistemrezervareavion import SistemRezervareAvion

def test_rezervare_simpla():
    s = SistemRezervareAvion()
    pret = s.rezerva_loc(3, 'A', 30, False)
    assert pret == 100.0

def test_business_class():
    s = SistemRezervareAvion()
    pret = s.rezerva_loc(2, 'A', 30, False)
    assert pret == 150.0

def test_reducere_copil():
    s = SistemRezervareAvion()
    pret = s.rezerva_loc(3, 'A', 10, False)
    assert pret == 50.0

def test_reducere_senior():
    s = SistemRezervareAvion()
    pret = s.rezerva_loc(3, 'A', 65, False)
    assert pret == 50.0

def test_infant():
    s = SistemRezervareAvion()
    pret = s.rezerva_loc(3, 'A', 1, False)
    assert pret == 10.0

def test_bagaj():
    s = SistemRezervareAvion()
    pret = s.rezerva_loc(3, 'A', 30, True)
    assert pret == 120.0

def test_infant_fara_bagaj():
    s = SistemRezervareAvion()
    pret = s.rezerva_loc(3, 'A', 1, True)
    assert pret == 10.0

def test_loc_ocupat():
    s = SistemRezervareAvion()
    s.rezerva_loc(3, 'A', 30, False)
    rezultat = s.rezerva_loc(3, 'A', 30, False)
    assert rezultat == "Ocupat"

def test_anulare_rezervare():
    s = SistemRezervareAvion()
    s.rezerva_loc(3, 'A', 30, False)
    assert s.anuleaza_rezervare(3, 'A') is True
    assert s.este_loc_disponibil(3, 'A') is True

def test_anulare_loc_liber():
    s = SistemRezervareAvion()
    assert s.anuleaza_rezervare(3, 'A') is False

def test_locuri_disponibile_initial():
    s = SistemRezervareAvion()
    assert s.nr_locuri_disponibile() == 60

def test_avion_plin():
    s = SistemRezervareAvion()

    for r in range (1, 11):
        for c in "ABCDEF":
            s.rezerva_loc(r, c, 30, False)

    assert s.avion_plin() is True

def test_echilibru_blocare():
    s = SistemRezervareAvion()

    s.rezerva_loc(3, 'A', 30, False)
    s.rezerva_loc(3, 'B', 30, False)
    s.rezerva_loc(3, 'C', 30, False)
    s.rezerva_loc(4, 'A', 30, False)

    rezultat = s.rezerva_loc(4, 'B', 30, False)

    assert rezultat == "Dezechilibru"

def test_echilibru_limita():
    s = SistemRezervareAvion()

    s.rezerva_loc(3, 'A', 30, False)
    s.rezerva_loc(3, 'B', 30, False)
    s.rezerva_loc(3, 'C', 30, False)

    rezultat = s.rezerva_loc(3, 'D', 30, False)

    assert rezultat != "Dezechilibru"

def test_input_invalid_rand():
    s = SistemRezervareAvion()
    with pytest.raises(ValueError):
        s.rezerva_loc(0, 'A', 30, False)

def test_input_invalid_loc():
    s = SistemRezervareAvion()
    with pytest.raises(ValueError):
        s.rezerva_loc(3, 'Z', 30, False)

def test_input_invalid_loc2():
    s = SistemRezervareAvion()
    with pytest.raises(ValueError):
        s.rezerva_loc(3, "AB", 30, False)

def test_reset():
    s = SistemRezervareAvion()
    s.rezerva_loc(3, 'A', 30, False)
    s.reseteaza()
    assert s.nr_locuri_ocupate() == 0

# teste aditionale

def test_business_exact_boundary():
    s = SistemRezervareAvion()
    pret = s.rezerva_loc(2, 'F', 30, False)
    assert pret == 150.0

def test_copil_spre_adult():
    s = SistemRezervareAvion()

    pret_copil = s.rezerva_loc(3, 'A', 12, False)
    pret_adult = s.rezerva_loc(3, 'B', 13, False)

    assert pret_copil == 50.0
    assert pret_adult == 100.0


def test_adult_spre_senior():
    s = SistemRezervareAvion()

    pret_adult = s.rezerva_loc(3, 'A', 59, False)
    pret_senior = s.rezerva_loc(3, 'B', 60, False)

    assert pret_adult == 100.0
    assert pret_senior == 50.0

def test_bagaj_la_varsta_2():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(3, 'A', 2, True)

    assert pret == 70.0

def test_echilibru_parte_dreapta():
    s = SistemRezervareAvion()

    s.rezerva_loc(3, 'D', 30, False)
    s.rezerva_loc(3, 'E', 30, False)
    s.rezerva_loc(3, 'F', 30, False)
    s.rezerva_loc(4, 'D', 30, False)

    rezultat = s.rezerva_loc(4, 'E', 30, False)

    assert rezultat == "Dezechilibru"

# teste 136 mutanti in viata

def test_locuri_disponibile_contin_randuri_corecte():
    s = SistemRezervareAvion()

    locuri = s.locuri_disponibile()

    assert (1, 'A') in locuri
    assert (10, 'F') in locuri

    assert (-1, 'A') not in locuri
    assert (0, 'A') not in locuri

def test_locuri_disponibile_dupa_rezervare():
    s = SistemRezervareAvion()

    s.rezerva_loc(3, 'A', 30, False)

    locuri = s.locuri_disponibile()

    assert (3, 'A') not in locuri
    assert len(locuri) == 59

def test_echilibru_exact_la_limita_permisa():
    s = SistemRezervareAvion()

    #diferenta = 2
    s.rezerva_loc(1, 'A', 30, False)
    s.rezerva_loc(1, 'B', 30, False)

    rezultat = s.rezerva_loc(1, 'C', 30, False)

    assert rezultat != "Dezechilibru"

def test_echilibru_depaseste_limita():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, 'A', 30, False)
    s.rezerva_loc(1, 'B', 30, False)
    s.rezerva_loc(1, 'C', 30, False)

    #diferenta = 4
    rezultat = s.rezerva_loc(2, 'A', 30, False)

    assert rezultat == "Dezechilibru"

def test_rand_bool_invalid():
    s = SistemRezervareAvion()

    with pytest.raises(TypeError):
        s.rezerva_loc(True, 'A', 30, False)

def test_varsta_bool_invalid():
    s = SistemRezervareAvion()

    with pytest.raises(TypeError):
        s.rezerva_loc(1, 'A', True, False)

def test_bagaj_non_bool():
    s = SistemRezervareAvion()

    with pytest.raises(TypeError):
        s.rezerva_loc(1, 'A', 30, "da")

def test_loc_lowercase():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(3, 'a', 30, False)

    assert pret == 100.0
    assert s.este_loc_disponibil(3, 'A') is False

def test_rezervare_adaugata_in_istoric():
    s = SistemRezervareAvion()

    s.rezerva_loc(3, 'A', 30, True)

    assert len(s.rezervari) == 1

    rezervare = s.rezervari[0]

    assert rezervare["rand"] == 3
    assert rezervare["loc"] == 'A'
    assert rezervare["varsta"] == 30
    assert rezervare["bagaj_cala"] is True
    assert rezervare["pret"] == 120.0

def test_anulare_sterge_din_istoric():
    s = SistemRezervareAvion()

    s.rezerva_loc(3, 'A', 30, False)

    s.anuleaza_rezervare(3, 'A')

    assert len(s.rezervari) == 0

def test_nr_locuri_ocupate_corect():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, 'A', 30, False)
    s.rezerva_loc(1, 'D', 30, False)

    assert s.nr_locuri_ocupate() == 2
    assert s.nr_locuri_disponibile() == 58

def test_reset_goleste_tot():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, 'A', 30, False)
    s.rezerva_loc(1, 'D', 30, False)

    s.reseteaza()

    assert s.nr_locuri_ocupate() == 0
    assert s.nr_locuri_disponibile() == 60
    assert len(s.rezervari) == 0

@pytest.mark.parametrize(
    "varsta, pret",
    [
        (1, 10.0),
        (2, 50.0),
        (12, 50.0),
        (13, 100.0),
        (59, 100.0),
        (60, 50.0),
    ],
)
def test_boundary_varste(varsta, pret):
    s = SistemRezervareAvion()

    rezultat = s.rezerva_loc(3, 'A', varsta, False)

    assert rezultat == pret

def test_avion_devine_plin_corect():
    s = SistemRezervareAvion()

    rezultate = []

    for r in range(1, 11):
        for c in "ABCDEF":
            rezultate.append(
                s.rezerva_loc(r, c, 30, False)
            )

    assert all(r != "Ocupat" for r in rezultate)
    assert all(r != "Dezechilibru" for r in rezultate)

    assert s.avion_plin() is True
    assert s.nr_locuri_disponibile() == 0

#79 mutanti

def test_echilibru_limita_si_depasire_pe_dreapta():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, 'D', 30, False)
    s.rezerva_loc(1, 'E', 30, False)

    rezultat_ok = s.rezerva_loc(1, 'F', 30, False)

    assert rezultat_ok != "Dezechilibru"

    rezultat_blocat = s.rezerva_loc(2, 'D', 30, False)

    assert rezultat_blocat == "Dezechilibru"

#68 mutanti

def test_litere_mapate_corect():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, 'A', 30, False)
    s.rezerva_loc(1, 'F', 30, False)

    assert s.este_loc_disponibil(1, 'A') is False
    assert s.este_loc_disponibil(1, 'F') is False

    assert s.este_loc_disponibil(1, 'B') is True
    assert s.este_loc_disponibil(1, 'E') is True

def test_anulare_rezervare_corecta_cu_mai_multe_rezervari():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, 'A', 30, False)
    s.rezerva_loc(1, 'B', 30, False)
    s.rezerva_loc(1, 'C', 30, False)

    s.anuleaza_rezervare(1, 'C')

    assert len(s.rezervari) == 2

    assert s.este_loc_disponibil(1, 'C') is True
    assert s.este_loc_disponibil(1, 'A') is False
    assert s.este_loc_disponibil(1, 'B') is False

def test_nr_locuri_ocupate_31():
    s = SistemRezervareAvion()

    count = 0

    for r in range(1, 11):
        for c in "ABCDEF":
            if count == 31:
                break
            s.rezerva_loc(r, c, 30, False)
            count += 1

    assert s.nr_locuri_ocupate() == 31

#57 mutanti

def test_litere_ocupa_locuri_diferite():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, 'A', 30, False)

    assert s.este_loc_disponibil(1, 'A') is False
    assert s.este_loc_disponibil(1, 'B') is True

    s.rezerva_loc(1, 'B', 30, False)

    assert s.nr_locuri_ocupate() == 2

def test_echilibru_mare_stanga_blocat():
    s = SistemRezervareAvion()

    # 3 pe dreapta
    s.rezerva_loc(1, 'D', 30, False)
    s.rezerva_loc(1, 'E', 30, False)
    s.rezerva_loc(1, 'F', 30, False)

    s.rezerva_loc(2, 'A', 30, False)
    s.rezerva_loc(2, 'B', 30, False)
    s.rezerva_loc(2, 'C', 30, False)

    rezultat = s.rezerva_loc(3, 'A', 30, False)

    assert rezultat != "Dezechilibru"

    rezultat2 = s.rezerva_loc(3, 'B', 30, False)

    assert rezultat2 == "Dezechilibru"

def test_este_loc_disponibil_rand_4():
    s = SistemRezervareAvion()

    s.rezerva_loc(4, 'A', 30, False)

    assert s.este_loc_disponibil(4, 'A') is False
    assert s.este_loc_disponibil(5, 'A') is True

def test_anulare_rezervare_rand_4():
    s = SistemRezervareAvion()

    s.rezerva_loc(4, 'A', 30, False)

    assert s.anuleaza_rezervare(4, 'A') is True
    assert s.este_loc_disponibil(4, 'A') is True

def test_vizualizare_format_corect(capsys):
    s = SistemRezervareAvion()

    s.vizualizeaza_avion()

    captured = capsys.readouterr()

    prima_linie = captured.out.splitlines()[0]

    assert prima_linie == "___ ___"

#0 mutanti