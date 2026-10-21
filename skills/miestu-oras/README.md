# miestu-oras

Skill'as penkių didžiausių Lietuvos miestų artimiausio laiko orų prognozei gauti iš Meteo.lt.

## Turinys
- `SKILL.md` – aktyvavimo sąlygos ir agento instrukcijos.
- `scripts/orai.py` – standartine Python biblioteka paremtas Meteo.lt API klientas.

## Naudojimas

Reikia Python 3.9+ ir interneto prieigos.

```bash
python scripts/orai.py
```

Skriptas grąžina JSON: Vilniaus, Kauno, Klaipėdos, Šiaulių ir Panevėžio temperatūrą, oro sąlygas bei prognozės laiką Lietuvos laiku. Nereikia API rakto ar papildomų Python paketų.

Skill'ą įdiekite nukopijavę `miestu-oras` katalogą į savo agento skills katalogą. Vartotojo pavyzdys: „Parodyk penkių didžiausių Lietuvos miestų orus“.

**Svarbu:** rodoma artimiausia prieinama **prognozė**, ne realaus laiko stoties matavimas. Duomenų šaltinis: Lietuvos hidrometeorologijos tarnyba, https://api.meteo.lt/. Naudojant duomenis laikykitės tarnybos licencijos ir priskyrimo sąlygų.
