# CFG + set minim teste structurale (S/B/C)

TODO: Diagrame

Pentru aceeași metodă, au fost construite seturi distincte de teste pentru statement coverage, branch coverage și condition coverage, astfel încât să se poată observa diferența dintre criterii și creșterea numărului minim de teste necesare. 
Testele suplimentare au fost separate de seturile minime, deoarece acestea nu sunt necesare pentru atingerea criteriului structural, ci pentru validarea mai clară a regulilor de business.

Legendă:
- S = acoperire la nivel de instrucțiune (statement)
- B = acoperire la nivel de ramură (branch)
- C = acoperire la nivel de condiție (condition)

Comenzi de rulare:
```bash
python -m pip install coverage

python -m coverage run -m unittest -v test_coverage.py
python -m coverage report -m

python -m coverage html
```

## 1) `__init__`

CFG:

```text
Start
 -> init locuri_ocupate
 -> init pret_baza
 -> init rezervari
Stop
```

Metoda `__init__` este liniară și nu conține decizii sau condiții compuse. Prin urmare, nu există ramuri alternative în fluxul de execuție.

Număr minim teoretic de teste:
- Statement coverage: 1
- Branch coverage: 1 (trivial, nu există ramuri)
- Condition coverage: 1 (trivial, nu există condiții)

Set minim de teste:
- I1: creare obiect și verificare stare inițială

## 2) `_litera_la_coloana`

CFG:

```text
Start
 -> litera_loc.upper()
 -> ord(...) - ord("A")
Stop
```

Număr minim teoretic de teste:
- Statement coverage: 1
- Branch coverage: 1
- Condition coverage: 1

Set minim de teste:
- L1: literă validă, de exemplu "A"

Teste suplimentare:
- L2: literă mică "f" pentru a verifica conversia upper() (nu este necesar structural)

## 3) `_calculeaza_pret`

CFG:

```text
Start
 -> pret = pret_baza
 -> D1: rand <= 2 ?
      True  -> pret += SUPLIMENT_BUSINESS
      False -> skip
 -> D2: varsta_pasager < 2 ?
      True  -> pret *= 0.1
      False -> D3
 -> D3: varsta_pasager <= 12 or varsta_pasager >= 60 ?
      True  -> pret *= 0.5
      False -> skip
 -> D4: are_bagaj_cala and varsta_pasager >= 2 ?
      True  -> pret += SUPLIMENT_BAGAJ
      False -> skip
 -> return round(float(pret), 2)
Stop
```

Metoda conține patru decizii:
- D1: rand <= 2
- D2: varsta_pasager < 2
- D3: varsta_pasager <= 12 or varsta_pasager >= 60
- D4: are_bagaj_cala and varsta_pasager >= 2

Dintre acestea:
- D1 și D2 sunt decizii simple;
- D3 și D4 sunt decizii compuse.

Analiză:

Metoda conține patru decizii: două simple și două compuse. În consecință, numărul minim de teste diferă în funcție de criteriul de acoperire.

Număr minim teoretic de teste:
- Statement coverage: 2
- Branch coverage: 3
- Condition coverage: 4

Set minim:
#### Statement coverage
- P1: (1, 1, False) → business + infant
- P2: (5, 10, True) → copil + bagaj

#### Branch coverage
- P1: (1, 1, False)
- P2: (5, 10, True)
- P3: (5, 30, False)

#### Condition coverage
- P1: (1, 1, False)
- P2: (5, 10, True)
- P3: (5, 30, False)
- P4: (5, 65, False)

#### Teste suplimentare
- P5: (5, 1, True) → infant cu bagaj; util pentru validarea explicită a regulii de business. Nu este necesar pentru minimul structural.

## 4) `_calculeaza_echilibru`

CFG:

```text
Start
 -> stanga = sum(... ocupat and col_idx < 3)
 -> dreapta = sum(... ocupat and col_idx >= 3)
 -> return (stanga, dreapta)
Stop
```

Set minim:

#### Statement coverage
- E1: avion gol

#### Branch coverage
- E1: avion gol
- E2: (1, "A"), (1, "D")

#### Pentru condition coverage
- E1: avion gol
- E2: (1, "A"), (1, "D")


## 5) `_verifica_echilibru`

CFG:

```text
Start
 -> (stanga, dreapta) = _calculeaza_echilibru()
 -> D1: coloana < 3 ?
      True  -> D2: (stanga + 1 - dreapta) <= MAX_DEZECHILIBRU ?
                  True  -> return True
                  False -> return False
      False -> D3: (dreapta + 1 - stanga) <= MAX_DEZECHILIBRU ?
                  True  -> return True
                  False -> return False
Stop
```

**Notă:** În cadrul acestui proiect, noțiunea de decizie este utilizată conform definiției din cursul 2 – Structural Testing (pagina 8), unde deciziile sunt asociate exclusiv structurilor de control ale fluxului de execuție, precum if, while și for. În consecință, evaluarea directă a unei expresii booleene (de exemplu într-o instrucțiune return expr) nu este clasificată ca decizie și nu introduce ramuri suplimentare în graful de control (CFG).

Număr minim teoretic de teste:
- Statement coverage: 2
- Branch coverage: 3
- Condition coverage: 3

Set minim:
#### Statement coverage
- V1: coloană pe stânga, permis
- V2: coloană pe dreapta, permis

#### Branch coverage
- V1: coloană pe stânga, permis
- V2: coloană pe dreapta, permis
- V3: coloană pe stânga, refuzat după 3 locuri pe stânga

#### Condition coverage
- V1: coloană pe stânga, permis
- V2: coloană pe dreapta, permis
- V3: coloană pe stânga, refuzat după 3 locuri pe stânga

Teste suplimentare:
- V4: coloană pe dreapta, refuzat după 3 locuri pe dreapta; util pentru verificarea simetriei, dar nenecesar pentru minimul structural.

## 6) `rezerva_loc`

CFG: TODO: Diagrama draw.io

```text
Start
 -> D1: not isinstance(rand, int) or isinstance(rand, bool) ?
      True  -> raise TypeError
      False -> D2
 -> D2: not (1 <= rand <= NR_RANDURI) ?
      True  -> raise ValueError
      False -> D3
 -> D3: not isinstance(litera_loc, str) or len(litera_loc) != 1 ?
      True  -> raise ValueError
      False -> litera_upper = litera_loc.upper()
 -> D4: litera_upper not in LITERE_VALIDE ?
      True  -> raise ValueError
      False -> D5
 -> D5: not isinstance(varsta_pasager, int) or isinstance(varsta_pasager, bool) ?
      True  -> raise TypeError
      False -> D6
 -> D6: varsta_pasager < 0 ?
      True  -> raise ValueError
      False -> D7
 -> D7: not isinstance(are_bagaj_cala, bool) ?
      True  -> raise TypeError
      False -> coloana = _litera_la_coloana(...)
 -> D8: locul este ocupat ?
      True  -> return "Ocupat"
      False -> D9
 -> D9: not _verifica_echilibru(coloana) ?
      True  -> return "Dezechilibru"
      False -> calculeaza pret
 -> locuri_ocupate[rand - 1][coloana] = True
 -> append in rezervari
 -> return pret_final
Stop
```

![CFG06](images/CFG06.drawio.png)

Număr minim teoretic de teste:
- Statement coverage: 10
- Branch coverage: 10
- Condition coverage: 14
- MC/DC coverage: 14

Set minim:
#### Statement coverage
- R1: tip invalid la rand
- R2: valoare invalidă la rand
- R3: format invalid la literă
- R4: literă invalidă
- R5: tip invalid la vârstă
- R6: vârstă negativă
- R7: tip invalid la bagaj
- R8: rezervare validă
- R9: loc ocupat
- R10: dezechilibru

#### Branch coverage
- R1: tip invalid la rand
- R2: valoare invalidă la rand
- R3: format invalid la literă
- R4: literă invalidă
- R5: tip invalid la vârstă
- R6: vârstă negativă
- R7: tip invalid la bagaj
- R8: rezervare validă
- R9: loc ocupat
- R10: dezechilibru

#### Condition coverage
- R1: rand="1"
- R2: rand=True
- R3: rand=0
- R4: rand=11
- R5: litera_loc=5
- R6: litera_loc="AB"
- R7: litera_loc="Z"
- R8: varsta_pasager="30"
- R9: varsta_pasager=True
- R10: varsta_pasager=-1
- R11: are_bagaj_cala="da"
- R12: rezervare validă
- R13: loc ocupat
- R14: dezechilibru

#### MC/DC coverage

MC/DC reprezintă o formă mai puternică de condition/decision coverage. Pe lângă faptul că fiecare condiție individuală trebuie să ia valorile True și False, trebuie demonstrat și că fiecare condiție poate influența independent rezultatul deciziei din care face parte.

## Decizii analizate

```text
D1: not isinstance(rand, int) or isinstance(rand, bool)
D2: not (1 <= rand <= NR_RANDURI)
D3: not isinstance(litera_loc, str) or len(litera_loc) != 1
D4: litera_upper not in LITERE_VALIDE
D5: not isinstance(varsta_pasager, int) or isinstance(varsta_pasager, bool)
D6: varsta_pasager < 0
D7: not isinstance(are_bagaj_cala, bool)
D8: self.locuri_ocupate[rand - 1][coloana]
D9: not self._verifica_echilibru(coloana)
```

Pentru deciziile compuse, condițiile individuale sunt:

```text
D1:
  C1 = not isinstance(rand, int)
  C2 = isinstance(rand, bool)

D2:
  C3 = rand < 1
  C4 = rand > NR_RANDURI

D3:
  C5 = not isinstance(litera_loc, str)
  C6 = len(litera_loc) != 1

D5:
  C7 = not isinstance(varsta_pasager, int)
  C8 = isinstance(varsta_pasager, bool)
```

Celelalte decizii sunt decizii simple. Pentru acestea este suficient ca decizia să fie evaluată o dată pe `True` și o dată pe `False`.

---

## Număr minim de teste

Numărul minim de teste necesare pentru MC/DC este:

```text
1 test valid de bază
+ 2 teste pentru D1
+ 2 teste pentru D2
+ 2 teste pentru D3
+ 1 test pentru D4
+ 2 teste pentru D5
+ 1 test pentru D6
+ 1 test pentru D7
+ 1 test pentru D8
+ 1 test pentru D9
= 14 teste
```

Observație: față de setul pentru condition coverage, nu este necesar un test suplimentar dacă testul `litera_loc=5` este înlocuit cu `litera_loc=["A"]`. Această modificare permite demonstrarea influenței independente a condiției `not isinstance(litera_loc, str)` în decizia D3. Astfel, condiția `len(litera_loc) != 1` este conceptual `False`, iar influența independentă a condiției `not isinstance(litera_loc, str)` poate fi demonstrată corect.


## Demonstrație MC/DC pentru deciziile compuse

### D1: `not isinstance(rand, int) or isinstance(rand, bool)`

| Test | C1: `not isinstance(rand, int)` | C2: `isinstance(rand, bool)` | D1 |
|---|---:|---:|---:|
| R1: `rand="1"` | True | False | True |
| R2: `rand=True` | False | True | True |
| R12: `rand=1` | False | False | False |

Perechi MC/DC:

- C1 este demonstrată prin R1 și R12: C2 rămâne `False`, iar D1 se schimbă din `True` în `False`.
- C2 este demonstrată prin R2 și R12: C1 rămâne `False`, iar D1 se schimbă din `True` în `False`.

---

### D2: `not (1 <= rand <= NR_RANDURI)`

Această decizie poate fi tratată echivalent ca:

```text
rand < 1 or rand > NR_RANDURI
```

| Test | C3: `rand < 1` | C4: `rand > NR_RANDURI` | D2 |
|---|---:|---:|---:|
| R3: `rand=0` | True | False | True |
| R4: `rand=11` | False | True | True |
| R12: `rand=1` | False | False | False |

Perechi MC/DC:

- C3 este demonstrată prin R3 și R12: C4 rămâne `False`, iar D2 se schimbă din `True` în `False`.
- C4 este demonstrată prin R4 și R12: C3 rămâne `False`, iar D2 se schimbă din `True` în `False`.

---

### D3: `not isinstance(litera_loc, str) or len(litera_loc) != 1`

| Test | C5: `not isinstance(litera_loc, str)` | C6: `len(litera_loc) != 1` | D3 |
|---|---:|---:|---:|
| R5: `litera_loc=["A"]` | True | False | True |
| R6: `litera_loc="AB"` | False | True | True |
| R12: `litera_loc="A"` | False | False | False |

Perechi MC/DC:

- C5 este demonstrată prin R5 și R12: C6 rămâne `False`, iar D3 se schimbă din `True` în `False`.
- C6 este demonstrată prin R6 și R12: C5 rămâne `False`, iar D3 se schimbă din `True` în `False`.

---

### D5: `not isinstance(varsta_pasager, int) or isinstance(varsta_pasager, bool)`

| Test | C7: `not isinstance(varsta_pasager, int)` | C8: `isinstance(varsta_pasager, bool)` | D5 |
|---|---:|---:|---:|
| R8: `varsta_pasager="30"` | True | False | True |
| R9: `varsta_pasager=True` | False | True | True |
| R12: `varsta_pasager=30` | False | False | False |

Perechi MC/DC:

- C7 este demonstrată prin R8 și R12: C8 rămâne `False`, iar D5 se schimbă din `True` în `False`.
- C8 este demonstrată prin R9 și R12: C7 rămâne `False`, iar D5 se schimbă din `True` în `False`.

---

## Demonstrație pentru deciziile simple

Pentru deciziile simple este suficient ca decizia să fie evaluată o dată pe `True` și o dată pe `False`.

| Decizie | True | False |
|---|---|---|
| D4: `litera_upper not in LITERE_VALIDE` | R7 | R12 |
| D6: `varsta_pasager < 0` | R10 | R12 |
| D7: `not isinstance(are_bagaj_cala, bool)` | R11 | R12 |
| D8: `self.locuri_ocupate[rand - 1][coloana]` | R13 | R12 |
| D9: `not self._verifica_echilibru(coloana)` | R14 | R12 |

---


#### Set minim selectat
- R1: rand="1"
- R2: rand=True
- R3: rand=0
- R4: rand=11
- R5: litera_loc=["A"]
- R6: litera_loc="AB"
- R7: litera_loc="Z"
- R8: varsta_pasager="30"
- R9: varsta_pasager=True
- R10: varsta_pasager=-1
- R11: are_bagaj_cala="da"
- R12: rezervare validă
- R13: loc ocupat
- R14: dezechilibru

## 7) `anuleaza_rezervare`

CFG:

```text
Start
 -> D1: not isinstance(rand, int) or isinstance(rand, bool) ?
      True  -> raise TypeError
      False -> D2
 -> D2: not (1 <= rand <= NR_RANDURI) ?
      True  -> raise ValueError
      False -> D3
 -> D3: not isinstance(litera_loc, str) or len(litera_loc) != 1 ?
      True  -> raise ValueError
      False -> litera_upper = litera_loc.upper()
 -> D4: litera_upper not in LITERE_VALIDE ?
      True  -> raise ValueError
      False -> coloana = _litera_la_coloana(...)
 -> D5: not self.locuri_ocupate[rand - 1][coloana] ?
      True  -> return False
      False -> elibereaza locul
 -> for i = len(rezervari)-1 ... 0
      -> D6: rezervari[i]["rand"] == rand and rezervari[i]["loc"] == litera_upper ?
           True  -> pop(i), break
           False -> continua bucla
 -> return True
Stop
```

![CFG06](images/CFG07.drawio.png)

Număr minim teoretic de teste:
- Statement coverage: 6
- Branch coverage: 8
- Condition coverage: 11

Set minim

#### Statement coverage
- A1: tip invalid la rand
- A2: valoare invalidă la rand
- A3: format invalid la literă
- A4: literă invalidă
- A5: loc deja liber
- A6: anulare reușită

#### Branch coverage
- A1: tip invalid la rand
- A2: valoare invalidă la rand
- A3: format invalid la literă
- A4: literă invalidă
- A5: loc deja liber
- A6: anulare reușită
- A10: loc ocupat, dar prima rezervare verificată în istoric nu corespunde; bucla continuă și apoi găsește rezervarea corectă
- A11: loc marcat ca ocupat, dar fără rezervare în istoric; bucla se termină fără break, apoi funcția returnează True

#### Condition coverage
- A1: rand="1"
- A2: rand=True
- A3: rand=0
- A4: rand=11
- A5: litera_loc=5
- A6: litera_loc="AB"
- A7: litera_loc="Z"
- A8: loc valid, deja liber
- A9: loc valid și rezervat
`Acoperă ramura False pentru condiția not self.locuri_ocupate[rand - 1][coloana].`
- A10: rezervarea căutată nu este ultima din istoric
`Acoperă ramura False a condiției compuse din buclă: rezervari[i]["rand"] == rand and rezervari[i]["loc"] == litera_upper.`
- A11: loc ocupat fără rezervare în istoric
`Acoperă ieșirea din bucla for fără găsirea unei rezervări corespunzătoare.`

## 8) `este_loc_disponibil`

CFG:

```text
Start
 -> D1: not (1 <= rand <= NR_RANDURI) ?
      True  -> raise ValueError
      False -> litera_upper = litera_loc.upper()
 -> D2: litera_upper not in LITERE_VALIDE ?
      True  -> raise ValueError
      False -> coloana = _litera_la_coloana(litera_upper)
 -> return not self.locuri_ocupate[rand - 1][coloana]
Stop
```

Număr minim teoretic de teste:
- Statement coverage: 3
- Branch coverage: 4
- Condition coverage: 4

Set minim:

#### Statement coverage
- E1: rand invalid
- E2: litera_loc invalidă
- E3: loc valid, liber

#### Branch coverage
- E1: rand invalid
- E2: litera_loc invalidă
- E3: loc valid, liber

#### Condition coverage
- E1: rand=0
- E2: litera_loc="Z"
- E3: loc liber

Teste suplimentare:
- E4: loc valid, ocupat
- E5: literă mică ("a"), utilă funcțional, dar nenecesară pentru minimul structural.

## 9) `locuri_disponibile`

CFG:

```text
Start
 -> libere = []
 -> for rand_idx in range(NR_RANDURI):
      -> for col_idx in range(NR_COLOANE):
           -> D1: not self.locuri_ocupate[rand_idx][col_idx] ?
                True  -> libere.append((rand_idx + 1, LITERE_VALIDE[col_idx]))
                False -> skip
 -> return libere
Stop
```

Număr minim teoretic de teste:
- Statement coverage: 1
- Branch coverage: 2
- Condition coverage: 2

Set minim:

#### Statement coverage
- LD1: avion gol → toate locurile sunt libere

#### Branch coverage
- LD1: avion gol → se execută ramura True
- LD2: există cel puțin un loc ocupat → se execută și ramura False

#### Condition coverage
- LD1: loc liber
- LD2: loc ocupat

Teste suplimentare:
- LD3: avion parțial ocupat și verificarea exactă a listei rezultate; util pentru validarea ordinii de parcurgere și a conținutului exact al rezultatului, dar nenecesar pentru minimul structural.
- LD4: avion complet ocupat; util pentru a verifica faptul că metoda returnează lista goală [], deși acest caz nu este cerut pentru minimul structural.

## 10) `nr_locuri_disponibile`

CFG:

```text
Start
 -> return sum(1 for rand in self.locuri_ocupate
                 for ocupat in rand
                 if not ocupat)
Stop
```

Număr minim teoretic de teste:

- Statement coverage: 1
- Branch coverage: 2
- Condition coverage: 2

#### Statement coverage
- NLD1: avion gol → toate locurile sunt libere

#### Branch coverage
- NLD1: avion gol → condiția not ocupat este evaluată pe True
- NLD2: există cel puțin un loc ocupat → condiția este evaluată și pe False

#### Condition coverage
- NLD1: loc liber
- NLD2: loc ocupat

Teste suplimentare:

- NLD3: avion parțial ocupat și verificarea numărului exact de locuri rămase;


## 11) `nr_locuri_ocupate`

CFG:

```text
Start
 -> total_locuri = NR_RANDURI * NR_COLOANE
 -> locuri_libere = nr_locuri_disponibile()
 -> return total_locuri - locuri_libere
Stop
```

Număr minim teoretic de teste:

- Statement coverage: 1
- Branch coverage: 1
- Condition coverage: 1

#### Statement coverage
- NLO1: avion gol → numărul de locuri ocupate este 0

#### Branch coverage
- NLO1: avion gol

#### Condition coverage
- NLO1: avion gol

Teste suplimentare:

- NLO2: avion parțial ocupat și verificarea numărului exact de locuri ocupate;
- NLO3: avion complet ocupat și verificarea rezultatului 60.

## 12) `avion_plin`

CFG:

```text
Start
Start
 -> return nr_locuri_disponibile() == 0
Stop
```

Număr minim teoretic de teste:

- Statement coverage: 1
- Branch coverage: 0 (nu există decizii)
- Condition coverage: 0 (nu există condiții în sensul cursului)

Set minim:

#### Statement coverage
- AP1: avion plin → rezultatul este True

#### Branch coverage
- AP1: avion plin → condiția este evaluată pe True

#### Condition coverage
- AP1: avion plin → condiția este evaluată pe True

Teste suplimentare:
- AP2: avion neplin → condiția este evaluată pe False

## 13) `reseteaza`

CFG:

```text
Start
 -> self.locuri_ocupate = [[False] * NR_COLOANE for _ in range(NR_RANDURI)]
 -> self.rezervari.clear()
Stop
```

Număr minim teoretic de teste:

- Statement coverage: 1
- Branch coverage: 1
- Condition coverage: 1

#### Statement coverage
- RST1: avion cu locuri ocupate și rezervări existente, apoi apel `reseteaza`

#### Branch coverage
- RST1: avion cu stare modificată, apoi apel reseteaza

#### Condition coverage
- RST1: avion cu stare modificată, apoi apel reseteaza

## 14) `vizualizeaza_avion`

CFG :

```text
Start
 -> for rand_idx in range(NR_RANDURI):
      -> for col_idx in range(NR_COLOANE):
           -> D1: col_idx == 3 ?
                True  -> print(" ", end="")
                False -> skip
           -> D2: self.locuri_ocupate[rand_idx][col_idx] ?
                True  -> print(1, end="")
                False -> print("_", end="")
      -> print()
Stop
```

Număr minim teoretic de teste:

- Statement coverage: 1
- Branch coverage: 1
- Condition coverage: 1

#### Statement coverage
- VIZ1: există cel puțin un loc ocupat și cel puțin un loc liber

#### Branch coverage
- VIZ1: există cel puțin un loc ocupat și cel puțin un loc liber

#### Condition coverage
- VIZ1: self.locuri_ocupate[rand_idx][col_idx] evaluată pe True și False

## Concluzie despre suficiență

Pentru acest proiect:
- setul marcat S/B/C este suficient pentru acoperire structurală 100% pe codul sursă;
- acoperirea structurală nu garantează absența defectelor de specificație;



Raport AI:

Prompt:

```text
Vreau să generezi o suită de teste unitare pentru metoda `rezerva_loc` de mai jos. 
Scopul este să obții acoperire pentru:

1. Statement coverage
2. Branch coverage
3. Condition coverage

Metoda analizată este:

def rezerva_loc(
        self, rand: int, litera_loc: str, varsta_pasager: int, are_bagaj_cala: bool
    ):
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
            raise ValueError(
                f"Rand invalid: {rand}. Trebuie sa fie intre 1 si {self.NR_RANDURI}"
            )

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

        self.rezervari.append(
            {
                "rand": rand,
                "loc": litera_upper,
                "varsta": varsta_pasager,
                "bagaj_cala": are_bagaj_cala,
                "pret": pret_final,
            }
        )

        return pret_final

Clasa din care face parte metoda este `SistemRezervareAvion`

    LITERE_VALIDE = list("ABCDEF")
    NR_RANDURI = 10
    NR_COLOANE = 6
    PRET_BAZA = 100.0
    SUPLIMENT_BUSINESS = 50.0
    SUPLIMENT_BAGAJ = 20.0
    MAX_DEZECHILIBRU = 3  # diferenta maxima admisa stanga vs dreapta

    def __init__(self):
        # False = liber, True = ocupat
        self.locuri_ocupate = [
            [False] * self.NR_COLOANE for _ in range(self.NR_RANDURI)
        ]
        self.pret_baza = self.PRET_BAZA
        # istoric rezervari: lista de dict-uri cu detalii
        self.rezervari = []

Cerințe pentru răspuns:

1. Analizează metoda `rezerva_loc` și identifică toate deciziile `if`.
2. Pentru fiecare decizie, identifică:
   - condiția completă;
   - subcondițiile atomice, acolo unde există expresii compuse cu `or` sau `and`;
   - ramura True;
   - ramura False;
   - efectul executării ramurii.
3. Generează o suită minimă, dar suficientă, de teste pentru:
   - statement coverage;
   - branch coverage;
   - condition coverage.
4. Testele trebuie redactate în Python, folosind `unittest`.
```


Rezultate:

![RaportAI](images/RaportAI.png)