# miestu-oras

Penkių didžiausių Lietuvos miestų **artimiausio laiko orų prognozė** iš **Yr.no / MET Norway**: Vilnius, Kaunas, Klaipėda, Šiauliai ir Panevėžys.

## Naudojimas

Reikia Python 3.9+ ir interneto; papildomų Python paketų ir API rakto **nereikia**.

```bash
python skills/miestu-oras/scripts/orai.py
```

Skriptas pateikia JSON su kiekvieno miesto temperatūra (°C), lietuvišku oro sąlygų aprašymu ir prognozės laiku Lietuvos laiku.

## API identifikacija

MET Norway reikalauja **identifikuojančio User-Agent** su programos pavadinimu ir tikra kontaktine informacija (pvz., viešu projekto URL). Pagal numatytuosius nustatymus naudojamas šios repozitorijos URL. Jei projektą perkeliate, pakeiskite jį:

```bash
export YR_USER_AGENT="miestu-oras/1.0 https://github.com/Martin-cool/testing-skills"
```

Windows PowerShell:

```powershell
$env:YR_USER_AGENT="miestu-oras/1.0 https://github.com/Martin-cool/testing-skills"
```

Nenaudokite fiktyvios kontaktinės informacijos. Gerbkite API talpyklos ir užklausų dažnio taisykles.

## Failai

- `SKILL.md` – instrukcijos agentui.
- `scripts/orai.py` – oficialaus MET Norway `locationforecast/2.0/compact` API klientas.

**Svarbu:** tai prognozė, ne meteorologinės stoties matavimai. Šaltinis: [Yr.no](https://www.yr.no/) / [MET Norway](https://api.met.no/weatherapi/locationforecast/2.0/documentation). Duomenų naudojimui taikomos šaltinio licencijos ir priskyrimo sąlygos.
