import pytest

from sistem_rezervare import SistemRezervareAvion


# ---------------------------
# INITIALIZARE
# ---------------------------

def test_avion_initial_gol():
    s = SistemRezervareAvion()

    assert s.nr_locuri_ocupate() == 0
    assert s.nr_locuri_disponibile() == 60
    assert s.avion_plin() is False


# ---------------------------
# PRETURI
# ---------------------------

def test_pret_adult_economy_fara_bagaj():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 30, False)

    assert pret == 100.0


def test_pret_business_adult():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(1, "A", 30, False)

    assert pret == 150.0


def test_pret_copil():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 10, False)

    assert pret == 50.0


def test_pret_senior():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 65, False)

    assert pret == 50.0


def test_pret_infant():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 1, False)

    assert pret == 10.0


def test_bagaj_adaugat():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 30, True)

    assert pret == 120.0


def test_infant_fara_taxa_bagaj():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 1, True)

    assert pret == 10.0


# ---------------------------
# BOUNDARY AGE TESTS
# ---------------------------

def test_varsta_fix_2_ani():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 2, False)

    assert pret == 50.0


def test_varsta_fix_12_ani():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 12, False)

    assert pret == 50.0


def test_varsta_fix_13_ani():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 13, False)

    assert pret == 100.0


def test_varsta_fix_59_ani():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 59, False)

    assert pret == 100.0


def test_varsta_fix_60_ani():
    s = SistemRezervareAvion()

    pret = s.rezerva_loc(5, "A", 60, False)

    assert pret == 50.0


# ---------------------------
# REZERVARE
# ---------------------------

def test_rezervare_ocupa_loc():
    s = SistemRezervareAvion()

    s.rezerva_loc(5, "A", 30, False)

    assert s.este_loc_disponibil(5, "A") is False


def test_rezervare_loc_ocupat():
    s = SistemRezervareAvion()

    s.rezerva_loc(5, "A", 30, False)

    rezultat = s.rezerva_loc(5, "A", 30, False)

    assert rezultat == "Ocupat"


# ---------------------------
# ANULARE
# ---------------------------

def test_anulare_rezervare():
    s = SistemRezervareAvion()

    s.rezerva_loc(5, "A", 30, False)

    rezultat = s.anuleaza_rezervare(5, "A")

    assert rezultat is True
    assert s.este_loc_disponibil(5, "A") is True


def test_anulare_loc_liber():
    s = SistemRezervareAvion()

    rezultat = s.anuleaza_rezervare(5, "A")

    assert rezultat is False


# ---------------------------
# VALIDARI
# ---------------------------

def test_rand_invalid_mic():
    s = SistemRezervareAvion()

    with pytest.raises(ValueError):
        s.rezerva_loc(0, "A", 30, False)


def test_rand_invalid_mare():
    s = SistemRezervareAvion()

    with pytest.raises(ValueError):
        s.rezerva_loc(11, "A", 30, False)


def test_litera_invalida():
    s = SistemRezervareAvion()

    with pytest.raises(ValueError):
        s.rezerva_loc(1, "Z", 30, False)


def test_varsta_negativa():
    s = SistemRezervareAvion()

    with pytest.raises(ValueError):
        s.rezerva_loc(1, "A", -1, False)


def test_varsta_non_int():
    s = SistemRezervareAvion()

    with pytest.raises(TypeError):
        s.rezerva_loc(1, "A", "30", False)


def test_bagaj_non_bool():
    s = SistemRezervareAvion()

    with pytest.raises(TypeError):
        s.rezerva_loc(1, "A", 30, "da")


# ---------------------------
# ECHILIBRU
# ---------------------------

def test_echilibru_acceptat():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, "A", 30, False)
    s.rezerva_loc(1, "B", 30, False)
    s.rezerva_loc(1, "C", 30, False)

    rezultat = s.rezerva_loc(1, "D", 30, False)

    assert rezultat != "Dezechilibru"


def test_echilibru_refuzat():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, "A", 30, False)
    s.rezerva_loc(1, "B", 30, False)
    s.rezerva_loc(1, "C", 30, False)

    rezultat = s.rezerva_loc(2, "A", 30, False)

    assert rezultat == "Dezechilibru"


# ---------------------------
# RESET
# ---------------------------

def test_reset():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, "A", 30, False)
    s.rezerva_loc(2, "B", 30, False)

    s.reseteaza()

    assert s.nr_locuri_ocupate() == 0
    assert s.nr_locuri_disponibile() == 60
    assert len(s.rezervari) == 0


# ---------------------------
# LOCURI DISPONIBILE
# ---------------------------

def test_lista_locuri_disponibile():
    s = SistemRezervareAvion()

    s.rezerva_loc(1, "A", 30, False)

    locuri = s.locuri_disponibile()

    assert (1, "A") not in locuri
    assert (1, "B") in locuri