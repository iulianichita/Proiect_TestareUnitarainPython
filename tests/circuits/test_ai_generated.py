# teste generate cu ajutorul CHatGPT pentru interpretarea diferentelor 
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sistemrezervareavion import SistemRezervareAvion


@pytest.fixture
def sistem():
    return SistemRezervareAvion()


# =========================================================
# CIRCUIT 1
# rand nu este int
# =========================================================
def test_rand_tip_invalid(sistem):
    with pytest.raises(TypeError):
        sistem.rezerva_loc("3", "A", 25, True)


# =========================================================
# CIRCUIT 2
# rand in afara limitelor
# =========================================================
def test_rand_in_afara_intervalului(sistem):
    with pytest.raises(ValueError):
        sistem.rezerva_loc(0, "A", 25, True)


# =========================================================
# CIRCUIT 3
# litera loc invalida ca format
# =========================================================
def test_litera_format_invalid(sistem):
    with pytest.raises(ValueError):
        sistem.rezerva_loc(3, "AB", 25, True)


# =========================================================
# CIRCUIT 4
# litera loc invalida ca valoare
# =========================================================
def test_litera_valoare_invalida(sistem):
    with pytest.raises(ValueError):
        sistem.rezerva_loc(3, "Z", 25, True)


# =========================================================
# CIRCUIT 5
# varsta tip invalid
# =========================================================
def test_varsta_tip_invalid(sistem):
    with pytest.raises(TypeError):
        sistem.rezerva_loc(3, "A", "20", True)


# =========================================================
# CIRCUIT 6
# varsta negativa
# =========================================================
def test_varsta_negativa(sistem):
    with pytest.raises(ValueError):
        sistem.rezerva_loc(3, "A", -5, True)


# =========================================================
# CIRCUIT 7
# bagaj invalid
# =========================================================
def test_bagaj_tip_invalid(sistem):
    with pytest.raises(TypeError):
        sistem.rezerva_loc(3, "A", 25, "DA")


# =========================================================
# CIRCUIT 8
# loc deja ocupat
# =========================================================
def test_loc_ocupat(sistem):
    sistem.rezerva_loc(3, "A", 25, True)

    rezultat = sistem.rezerva_loc(3, "A", 30, False)

    assert rezultat == "Ocupat"


# =========================================================
# CIRCUIT 9
# dezechilibru avion
# =========================================================
def test_dezechilibru(sistem, monkeypatch):
    def mock_verifica_echilibru(coloana):
        return False

    monkeypatch.setattr(
        sistem,
        "_verifica_echilibru",
        mock_verifica_echilibru
    )

    rezultat = sistem.rezerva_loc(3, "A", 25, True)

    assert rezultat == "Dezechilibru"


# =========================================================
# CIRCUIT 10
# rezervare cu succes
# =========================================================
def test_rezervare_succes(sistem):
    rezultat = sistem.rezerva_loc(3, "A", 25, True)

    assert isinstance(rezultat, float)

    assert sistem.locuri_ocupate[2][0] is True

    assert len(sistem.rezervari) == 1

    rezervare = sistem.rezervari[0]

    assert rezervare["rand"] == 3
    assert rezervare["loc"] == "A"
    assert rezervare["varsta"] == 25
    assert rezervare["bagaj_cala"] is True