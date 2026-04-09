import pytest
from sistemrezervareavion import SistemRezervareAvion


@pytest.fixture
def sistem():
    return SistemRezervareAvion()

# pt metoda rezerva_loc(rand, litera_loc, varsta_pasager, are_bagaj_cala)

class TestRezerva_Loc:

    # 1. rand

    # clase de echivalenta

    # R_1
    def test_rand_valid_business(self, sistem):
        assert sistem.rezerva_loc(2, 'A', 25, False) == 150.0

    # R_2
    def test_rand_valid_economy(self, sistem):
        assert sistem.rezerva_loc(5, 'A', 25, False) == 100.0

    # R_3
    @pytest.mark.parametrize("rand", [0, 12, -1])
    def test_rand_invalid_value_raises_value_error(self, sistem, rand):
        with pytest.raises(ValueError):
            sistem.rezerva_loc(rand, 'A', 25, False)

    # R_4
    @pytest.mark.parametrize("rand", [3.5, "5", True])
    def test_rand_invalid_type_raises_type_error(self, sistem, rand):
        with pytest.raises(TypeError):
            sistem.rezerva_loc(rand, 'A', 25, False)

     # R_5
    def test_rand_bool_raises_type_error(self, sistem):
        with pytest.raises(TypeError):
            sistem.rezerva_loc(True, 'A', 25, False)


    # analiza de frontiera

    # R_1
    # limita inferiora: rand = 1
    def test_rand_minim_valid(self, sistem):
        assert sistem.rezerva_loc(1, 'A', 25, False) == 150.0

    # limita superioara: rand = 10
    def test_rand_maxim_valid(self, sistem):
        assert sistem.rezerva_loc(10, 'A', 25, False) == 100.0

    # R_2
    # rand = 0
    def test_rand_sub_minim_invalid(self, sistem):
        with pytest.raises(ValueError):
            sistem.rezerva_loc(0, 'A', 25, False)

    # rand = 11
    def test_rand_peste_maxim_invalid(self, sistem):
        with pytest.raises(ValueError):
            sistem.rezerva_loc(11, 'A', 25, False)

    
    # 2. litera_loc

    # clase de echivalenta

    # L_1
    def test_litera_mare_valid(self, sistem):
        assert sistem.rezerva_loc(1, 'B', 25, False) == 150.0
    
    # L_2
    def test_litera_mica_valid(self, sistem):
        assert sistem.rezerva_loc(1, 'c', 25, False) == 150.0

    # L_3
    @pytest.mark.parametrize("litera_loc", ['I', 'n', '1'])
    def test_litera_invalid_value_raises_value_error(self, sistem, litera_loc):
        with pytest.raises(ValueError):
            sistem.rezerva_loc(1, litera_loc, 25, False)

    # L_4
    @pytest.mark.parametrize("litera_loc", [1, True, 5.7])
    def test_litera_invalid_type_raises_value_error(self, sistem, litera_loc):
        with pytest.raises(ValueError):
            sistem.rezerva_loc(1, litera_loc, 25, False)

    # L_5
    @pytest.mark.parametrize("litera_loc", ["AB", "asd", ""])
    def test_litera_lungime_gresita_raises_value_error(self, sistem, litera_loc):
        with pytest.raises(ValueError):
            sistem.rezerva_loc(1, litera_loc, 25, False)

    # analiza de frontiera

    # L_1 si L_2
    @pytest.mark.parametrize("litera_loc", ['A', 'a'])
    def test_loc_minim_valid(self, sistem, litera_loc):
        assert sistem.rezerva_loc(1, litera_loc, 25, False) == 150.0
    
    @pytest.mark.parametrize("litera_loc", ['F', 'f'])
    def test_loc_maxim_valid(self, sistem, litera_loc):
        assert sistem.rezerva_loc(1, litera_loc, 25, False) == 150.0
    
    @pytest.mark.parametrize("litera_loc", ['G', 'g'])
    def test_loc_peste_maxim_invalid(self, sistem, litera_loc):
        with pytest.raises(ValueError):
            sistem.rezerva_loc(1, litera_loc, 25, False)


    # 3. varsta_pasager

    # clase de echivalenta

    # V_1
    @pytest.mark.parametrize("varsta_pasager", [1])
    def test_varsta_infant(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 15.0
    
    # V_2
    @pytest.mark.parametrize("varsta_pasager", [10])
    def test_varsta_copil(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 75.0

    # V_3
    @pytest.mark.parametrize("varsta_pasager", [20])
    def test_varsta_adult(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 150.0

    # V_4
    @pytest.mark.parametrize("varsta_pasager", [70])
    def test_varsta_senior(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 75.0
        
    # V_5
    @pytest.mark.parametrize("varsta_pasager", [-1, -5])
    def test_varsta_invalid_value_raises_value_error(self, sistem, varsta_pasager):
        with pytest.raises(ValueError):
            sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 150.0

    # V_6
    @pytest.mark.parametrize("varsta_pasager", ["abc", 3.5, 'a'])
    def test_varsta_invalid_type_raises_type_error(self, sistem, varsta_pasager):
        with pytest.raises(TypeError):
            sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 150.0
    
    # V_7
    @pytest.mark.parametrize("varsta_pasager", [True])
    def test_varsta_bool_raises_type_error(self, sistem, varsta_pasager):
        with pytest.raises(TypeError):
            sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 150.


    # analiza de frontiera

    # V_1
    @pytest.mark.parametrize("varsta_pasager", [0])
    def test_varsta_infant_minim_valid(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 15.0

    @pytest.mark.parametrize("varsta_pasager", [1])
    def test_varsta_infant_maxim_valid(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 15.0

    # V_2
    @pytest.mark.parametrize("varsta_pasager", [2])
    def test_varsta_copil_minim_valid(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 75.0

    @pytest.mark.parametrize("varsta_pasager", [12])
    def test_varsta_copil_maxim_valid(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 75.0

    # V_3
    @pytest.mark.parametrize("varsta_pasager", [13])
    def test_varsta_adult_minim_valid(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 150.0

    @pytest.mark.parametrize("varsta_pasager", [59])
    def test_varsta_adult_maxim_valid(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 150.0

    # V_4
    @pytest.mark.parametrize("varsta_pasager", [60])
    def test_varsta_senior_minim_valid(self, sistem, varsta_pasager):
        assert sistem.rezerva_loc(1, 'A', varsta_pasager, False) == 75.0

    # 4. are_bagaj_cala

    # clase de echivalenta

    # B_1
    @pytest.mark.parametrize("are_bagaj_cala", [True])
    def test_bagaj_cala_true(self, sistem, are_bagaj_cala):
        assert sistem.rezerva_loc(1, 'A', 20, are_bagaj_cala) == 170.0

    # B_2
    @pytest.mark.parametrize("are_bagaj_cala", [False])
    def test_bagaj_cala_false(self, sistem, are_bagaj_cala):
        assert sistem.rezerva_loc(1, 'A', 20, are_bagaj_cala) == 150.0

    # B_3
    @pytest.mark.parametrize("are_bagaj_cala", [True])
    def test_bagaj_cala_true_infant(self, sistem, are_bagaj_cala):
        assert sistem.rezerva_loc(1, 'A', 1, are_bagaj_cala) == 15.0

    # B_4
    @pytest.mark.parametrize("are_bagaj_cala", [1, "ab", 'a', 3.4])
    def test_bagaj_cala_invalid_type_raises_type_error(self, sistem, are_bagaj_cala):
        with pytest.raises(TypeError):
            sistem.rezerva_loc(1, 'A', 20, are_bagaj_cala)







