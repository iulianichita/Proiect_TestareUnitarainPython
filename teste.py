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