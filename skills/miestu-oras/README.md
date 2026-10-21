# miestu-oras

Penkių didžiausių Lietuvos miestų **dabartinių orų įvertinimas** iš oficialaus **Foreca Weather API**: Vilnius, Kaunas, Klaipėda, Šiauliai ir Panevėžys.

## Reikalavimai

- Python 3.9+ ir internetas; papildomų Python bibliotekų nereikia.
- **Foreca Weather API raktas**. Jį gaukite https://developer.foreca.com/ (gali reikėti registracijos, bandomojo laikotarpio ar mokamo plano).

## Paleidimas

Linux / macOS:

```bash
export FORECA_API_KEY="jusu_foreca_api_raktas"
python scripts/orai.py
```

Windows PowerShell:

```powershell
$env:FORECA_API_KEY="jusu_foreca_api_raktas"
python scripts/orai.py
```

**Niekada neįrašykite tikro API rakto į GitHub failus ar komandas, kurių istorija dalijatės.** Jei naudojate agentą, perduokite kintamąjį jo vykdymo aplinkai.

Skriptas grąžina JSON su temperatūra (°C), lietuvišku oro sąlygų aprašymu ir duomenų laiku Lietuvos laiku. Naudojamas Foreca `/api/v1/current/{longitude},{latitude}` endpointas ir `lang=lt`.

## Failai

- `SKILL.md` – agento instrukcijos.
- `scripts/orai.py` – Foreca API klientas.

**Pastaba:** Foreca `current` yra dabartinių orų įvertinimas, ne tiesioginis stoties matavimas. API užklausos gali būti apmokestinamos pagal jūsų planą. Duomenų šaltinis: https://developer.foreca.com/.
