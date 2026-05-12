import pytest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sistemrezervareavion import SistemRezervareAvion

@pytest.fixture
def sistem():
    return SistemRezervareAvion()


# ============================================================
# rezerva_loc - clase de echivalenta + valori de frontiera
# ============================================================

@pytest.mark.parametrize(
    "rand, litera, varsta, bagaj, pret_asteptat",
    [
        # randuri business: frontiera 1-2
        (1, "A", 30, False, 150.0),
        (2, "D", 30, False, 150.0),

        # rand economy: frontiera imediat dupa business
        (3, "A", 30, False, 100.0),

        # litere valide, inclusiv lowercase
        (10, "f", 30, False, 100.0),

        # varsta infant: < 2
        (3, "B", 0, False, 10.0),
        (3, "C", 1, True, 10.0),  # bagajul nu se aplica infantilor

        # frontiera copil: 2-12
        (4, "A", 2, True, 70.0),
        (4, "B", 12, False, 50.0),

        # frontiera adult: 13-59
        (4, "C", 13, True, 120.0),
        (5, "A", 59, False, 100.0),

        # frontiera senior: >= 60
        (5, "B", 60, True, 70.0),
    ],
)
def test_rezerva_loc_valid_preturi_frontiera(
    sistem, rand, litera, varsta, bagaj, pret_asteptat
):
    assert sistem.rezerva_loc(rand, litera, varsta, bagaj) == pret_asteptat


@pytest.mark.parametrize("rand_invalid", [0, 11, -1])
def test_rezerva_loc_rand_invalid_valoare(sistem, rand_invalid):
    with pytest.raises(ValueError):
        sistem.rezerva_loc(rand_invalid, "A", 30, False)


@pytest.mark.parametrize("rand_invalid", [1.5, "1", None, True])
def test_rezerva_loc_rand_invalid_tip(sistem, rand_invalid):
    with pytest.raises(TypeError):
        sistem.rezerva_loc(rand_invalid, "A", 30, False)


@pytest.mark.parametrize("litera_invalida", ["G", "Z", "", "AA", 1, None])
def test_rezerva_loc_litera_invalida(sistem, litera_invalida):
    with pytest.raises(ValueError):
        sistem.rezerva_loc(1, litera_invalida, 30, False)


@pytest.mark.parametrize("varsta_invalida", [-1])
def test_rezerva_loc_varsta_negativa(sistem, varsta_invalida):
    with pytest.raises(ValueError):
        sistem.rezerva_loc(1, "A", varsta_invalida, False)


@pytest.mark.parametrize("varsta_invalida", [1.5, "30", None, True])
def test_rezerva_loc_varsta_tip_invalid(sistem, varsta_invalida):
    with pytest.raises(TypeError):
        sistem.rezerva_loc(1, "A", varsta_invalida, False)


@pytest.mark.parametrize("bagaj_invalid", [1, 0, "True", None])
def test_rezerva_loc_bagaj_tip_invalid(sistem, bagaj_invalid):
    with pytest.raises(TypeError):
        sistem.rezerva_loc(1, "A", 30, bagaj_invalid)


def test_rezerva_loc_ocupat(sistem):
    assert sistem.rezerva_loc(1, "A", 30, False) == 150.0
    assert sistem.rezerva_loc(1, "A", 30, False) == "Ocupat"


def test_rezerva_loc_refuzat_dezechilibru_stanga(sistem):
    assert sistem.rezerva_loc(1, "A", 30, False) == 150.0
    assert sistem.rezerva_loc(2, "A", 30, False) == 150.0
    assert sistem.rezerva_loc(3, "A", 30, False) == 100.0

    # A patra rezervare pe stanga ar duce diferenta la 4 > MAX_DEZECHILIBRU
    assert sistem.rezerva_loc(4, "A", 30, False) == "Dezechilibru"


def test_rezerva_loc_refuzat_dezechilibru_dreapta(sistem):
    assert sistem.rezerva_loc(1, "D", 30, False) == 150.0
    assert sistem.rezerva_loc(2, "D", 30, False) == 150.0
    assert sistem.rezerva_loc(3, "D", 30, False) == 100.0

    # A patra rezervare pe dreapta ar duce diferenta la 4 > MAX_DEZECHILIBRU
    assert sistem.rezerva_loc(4, "D", 30, False) == "Dezechilibru"


# ============================================================
# anuleaza_rezervare
# ============================================================

def test_anuleaza_rezervare_loc_ocupat(sistem):
    sistem.rezerva_loc(1, "A", 30, False)

    assert sistem.anuleaza_rezervare(1, "A") is True
    assert sistem.este_loc_disponibil(1, "A") is True
    assert sistem.rezervari == []


def test_anuleaza_rezervare_loc_liber(sistem):
    assert sistem.anuleaza_rezervare(1, "A") is False


@pytest.mark.parametrize("rand_invalid", [0, 11, -1])
def test_anuleaza_rezervare_rand_invalid_valoare(sistem, rand_invalid):
    with pytest.raises(ValueError):
        sistem.anuleaza_rezervare(rand_invalid, "A")


@pytest.mark.parametrize("rand_invalid", [1.5, "1", None, True])
def test_anuleaza_rezervare_rand_invalid_tip(sistem, rand_invalid):
    with pytest.raises(TypeError):
        sistem.anuleaza_rezervare(rand_invalid, "A")


@pytest.mark.parametrize("litera_invalida", ["G", "", "AA", 1, None])
def test_anuleaza_rezervare_litera_invalida(sistem, litera_invalida):
    with pytest.raises(ValueError):
        sistem.anuleaza_rezervare(1, litera_invalida)


def test_anuleaza_rezervare_accepta_litera_lowercase(sistem):
    sistem.rezerva_loc(1, "a", 30, False)

    assert sistem.anuleaza_rezervare(1, "a") is True


# ============================================================
# este_loc_disponibil
# ============================================================

def test_este_loc_disponibil_initial_true(sistem):
    assert sistem.este_loc_disponibil(1, "A") is True


def test_este_loc_disponibil_dupa_rezervare_false(sistem):
    sistem.rezerva_loc(1, "A", 30, False)

    assert sistem.este_loc_disponibil(1, "A") is False


def test_este_loc_disponibil_dupa_anulare_true(sistem):
    sistem.rezerva_loc(1, "A", 30, False)
    sistem.anuleaza_rezervare(1, "A")

    assert sistem.este_loc_disponibil(1, "A") is True


@pytest.mark.parametrize("rand_valid", [1, 10])
def test_este_loc_disponibil_frontiere_rand_valide(sistem, rand_valid):
    assert sistem.este_loc_disponibil(rand_valid, "A") is True


@pytest.mark.parametrize("rand_invalid", [0, 11, -1])
def test_este_loc_disponibil_rand_invalid(sistem, rand_invalid):
    with pytest.raises(ValueError):
        sistem.este_loc_disponibil(rand_invalid, "A")


@pytest.mark.parametrize("litera_valida", ["A", "F", "a", "f"])
def test_este_loc_disponibil_litere_valide(sistem, litera_valida):
    assert sistem.este_loc_disponibil(1, litera_valida) is True


@pytest.mark.parametrize("litera_invalida", ["G", "Z", "AA"])
def test_este_loc_disponibil_litera_invalida(sistem, litera_invalida):
    with pytest.raises(ValueError):
        sistem.este_loc_disponibil(1, litera_invalida)