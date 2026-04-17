class SistemRezervareAvion:
    """
    Sistem de rezervare locuri avion:

    Avion cu 10 randuri x 6 locuri (A, B, C, D, E, F)
    Randurile 1-2 sunt Business Class (+50 RON)

    Reduceri varsta:
        - infant (< 2 ani):     90% reducere
        - copil (2-12 ani):     50% reducere
        - senior (>= 60 ani):   50% reducere
        - adult (13-59 ani):    fara reducere

    Bagaj de cala: +20 RON (nu se aplica copiilor sub 2 ani)

    Echilibru lateral:
        - rezervarea este refuzata daca diferenta dintre locurile ocupate pe o parte si cealalta depaseste pragul MAX_DEZECHILIBRU
    """

    LITERE_VALIDE = list("ABCDEF")
    NR_RANDURI = 10
    NR_COLOANE = 6
    PRET_BAZA = 100.0
    SUPLIMENT_BUSINESS = 50.0
    SUPLIMENT_BAGAJ = 20.0
    MAX_DEZECHILIBRU = 3  # diferenta maxima admisa stanga vs dreapta

    def __init__(self):
        # False = liber, True = ocupat
        self.locuri_ocupate = [[False] * self.NR_COLOANE for _ in range(self.NR_RANDURI)]
        self.pret_baza = self.PRET_BAZA
        # istoric rezervari: lista de dict-uri cu detalii
        self.rezervari = []

    # helpers
    def _litera_la_coloana(self, litera_loc: str) -> int:
        """Converteste litera locului (A-F) la index coloana (0-5)."""
        return ord(litera_loc.upper()) - ord('A')

    def _calculeaza_pret(self, rand: int, varsta_pasager: int,
                         are_bagaj_cala: bool) -> float:

        pret = self.pret_baza

        # Supliment Business Class
        if rand <= 2:
            pret += self.SUPLIMENT_BUSINESS

        # Reducere varsta
        if varsta_pasager < 2:
            pret *= 0.1  # infant: 90% reducere
        elif varsta_pasager <= 12 or varsta_pasager >= 60:
            pret *= 0.5  # copil/senior: 50%

        # Bagaj de cala (nu se aplica infantilor)
        if are_bagaj_cala and varsta_pasager >= 2:
            pret += self.SUPLIMENT_BAGAJ

        return round(float(pret), 2)

    def _calculeaza_echilibru(self) -> tuple[int, int]:
        """
        Numara locurile ocupate pe fiecare parte a avionului

        Returneaza:
            tuple[int, int] - (nr_ocupate_stanga, nr_ocupate_dreapta)
        """
        stanga = sum(
            1
            for rand in self.locuri_ocupate
            for col_idx, ocupat in enumerate(rand)
            if ocupat and col_idx < 3
        )
        dreapta = sum(
            1
            for rand in self.locuri_ocupate
            for col_idx, ocupat in enumerate(rand)
            if ocupat and col_idx >= 3
        )
        return stanga, dreapta

    def _verifica_echilibru(self, coloana: int) -> bool:
        """
        Verifica daca adaugarea unui loc pe coloana data ar depasi
        pragul de dezechilibru MAX_DEZECHILIBRU

        Returneaza:
            True  - rezervarea este permisa
            False - rezervarea ar depasi pragul de dezechilibru
        """
        stanga, dreapta = self._calculeaza_echilibru()

        if coloana < 3:
            # se adauga pe stanga
            return (stanga + 1 - dreapta) <= self.MAX_DEZECHILIBRU
        else:
            # se adauga pe dreapta
            return (dreapta + 1 - stanga) <= self.MAX_DEZECHILIBRU

    # system functionalities
    def rezerva_loc(self, rand: int, litera_loc: str,
                    varsta_pasager: int, are_bagaj_cala: bool):
        """
        Incearca sa rezerve locul (rand, litera_loc)

        Returneaza:
            float  - pretul final daca rezervarea a reusit
            "Ocupat" - daca locul era deja rezervat
            "Dezechilibru" - daca rezervarea ar dezechilibra avionul peste pragul MAX_DEZECHILIBRU

        Raises:
            ValueError - daca randul sau litera nu sunt valide
            TypeError  - daca varsta nu e int sau bool-ul nu e bool
        """
        # validare rand
        if not isinstance(rand, int) or isinstance(rand, bool):
            raise TypeError("Randul trebuie sa fie un numar intreg")
        if not (1 <= rand <= self.NR_RANDURI):
            raise ValueError(f"Rand invalid: {rand}. Trebuie sa fie intre 1 si {self.NR_RANDURI}")

        # validare litera loc
        if not isinstance(litera_loc, str) or len(litera_loc) != 1:
            raise ValueError("Litera locului trebuie sa fie un singur caracter (A-F)")
        litera_upper = litera_loc.upper()
        if litera_upper not in self.LITERE_VALIDE:
            raise ValueError(f"Loc invalid: '{litera_loc}'. Trebuie sa fie una din A-F")

        # validare varsta
        if not isinstance(varsta_pasager, int) or isinstance(varsta_pasager, bool):
            raise TypeError("Varsta trebuie sa fie un numar intreg")
        if varsta_pasager < 0:
            raise ValueError("Varsta nu poate fi negativa")

        # validare bagaj
        if not isinstance(are_bagaj_cala, bool):
            raise TypeError("are_bagaj_cala trebuie sa fie True sau False")

        coloana = self._litera_la_coloana(litera_upper)

        # verificare disponibilitate
        if self.locuri_ocupate[rand - 1][coloana]:
            return "Ocupat"

        # verificare echilibru lateral
        if not self._verifica_echilibru(coloana):
            return "Dezechilibru"

        # calculare pret si efectuare rezervare
        pret_final = self._calculeaza_pret(rand, varsta_pasager, are_bagaj_cala)
        self.locuri_ocupate[rand - 1][coloana] = True

        self.rezervari.append({
            "rand": rand,
            "loc": litera_upper,
            "varsta": varsta_pasager,
            "bagaj_cala": are_bagaj_cala,
            "pret": pret_final,
        })

        return pret_final

    def anuleaza_rezervare(self, rand: int, litera_loc: str) -> bool:
        """
        Anuleaza rezervarea unui loc

        Returneaza:
            True  - daca locul era rezervat si a fost eliberat
            False - daca locul era deja liber

        Raises:
            ValueError - daca randul sau litera nu sunt valide
        """
        if not isinstance(rand, int) or isinstance(rand, bool):
            raise TypeError("Randul trebuie sa fie un numar intreg")
        if not (1 <= rand <= self.NR_RANDURI):
            raise ValueError(f"Rand invalid: {rand}.")

        if not isinstance(litera_loc, str) or len(litera_loc) != 1:
            raise ValueError("Litera locului trebuie sa fie un singur caracter (A-F)")
        litera_upper = litera_loc.upper()
        if litera_upper not in self.LITERE_VALIDE:
            raise ValueError(f"Loc invalid: '{litera_loc}'.")

        coloana = self._litera_la_coloana(litera_upper)

        if not self.locuri_ocupate[rand - 1][coloana]:
            return False  # deja liber

        self.locuri_ocupate[rand - 1][coloana] = False
        # eliminam ultima rezervare care corespunde acestui loc
        for i in range(len(self.rezervari) - 1, -1, -1):
            if self.rezervari[i]["rand"] == rand and self.rezervari[i]["loc"] == litera_upper:
                self.rezervari.pop(i)
                break

        return True

    def este_loc_disponibil(self, rand: int, litera_loc: str) -> bool:
        """
        Verifica daca un loc este disponibil (nerezervat).

        Returns:
            True  - loc liber
            False - loc ocupat

        Raises:
            ValueError - daca randul sau litera nu sunt valide
        """
        if not (1 <= rand <= self.NR_RANDURI):
            raise ValueError(f"Rand invalid: {rand}.")
        litera_upper = litera_loc.upper()
        if litera_upper not in self.LITERE_VALIDE:
            raise ValueError(f"Loc invalid: '{litera_loc}'.")

        coloana = self._litera_la_coloana(litera_upper)
        return not self.locuri_ocupate[rand - 1][coloana]

    def locuri_disponibile(self) -> list[tuple[int, str]]:
        """
        Returneaza lista tuturor locurilor libere ca tupluri (rand, litera)

        Returneaza:
            list[tuple[int, str]] - ex. [(1, 'A'), (1, 'B'), ...]
        """
        libere = []
        for rand_idx in range(self.NR_RANDURI):
            for col_idx in range(self.NR_COLOANE):
                if not self.locuri_ocupate[rand_idx][col_idx]:
                    libere.append((rand_idx + 1, self.LITERE_VALIDE[col_idx]))
        return libere

    def nr_locuri_disponibile(self) -> int:
        """Returneaza numarul total de locuri libere."""
        return sum(
            1
            for rand in self.locuri_ocupate
            for ocupat in rand
            if not ocupat
        )

    def nr_locuri_ocupate(self) -> int:
        """Returneaza numarul total de locuri ocupate."""
        return self.NR_RANDURI * self.NR_COLOANE - self.nr_locuri_disponibile()

    def avion_plin(self) -> bool:
        """Returneaza True daca toate locurile sunt rezervate."""
        return self.nr_locuri_disponibile() == 0

    def reseteaza(self):
        """Elibereaza toate locurile si sterge istoricul rezervarilor."""
        self.locuri_ocupate = [[False] * self.NR_COLOANE for _ in range(self.NR_RANDURI)]
        self.rezervari.clear()

    def vizualizeaza_avion(self):
        """
        Vizualizeaza imaginea locurilor avionului
            1 - loc ocupat
            _ - loc neocupat
        """
        for rand_idx in range(self.NR_RANDURI):
            for col_idx in range(self.NR_COLOANE):
                if col_idx == 3:
                    print(' ', end='')
                if self.locuri_ocupate[rand_idx][col_idx]:
                    print(1, end='')
                else:
                    print('_', end='')
            print()