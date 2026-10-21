---
name: miestu-oras
description: Gauti penkių didžiausių Lietuvos miestų (Vilniaus, Kauno, Klaipėdos, Šiaulių, Panevėžio) oro temperatūrą ir oro sąlygas iš oficialios Meteo.lt tarnybos. Naudoti, kai prašoma dabartinių orų, temperatūrų ar orų palyginimo šiuose miestuose.
---

# Miestų oras

Kai vartotojas prašo penkių didžiausių Lietuvos miestų orų:

1. Paleisk `python scripts/orai.py` iš šio skill katalogo. Reikalingas interneto ryšys.
2. Pateik rezultatus lietuviškai lentelėje: miestas, temperatūra (°C), oro sąlygos, prognozės laikas Lietuvos laiku.
3. Aiškiai įvardyk, kad tai **artimiausio prognozės laiko orai**, o ne faktiniai meteorologinės stoties matavimai. Nurodyk šaltinį: Lietuvos hidrometeorologijos tarnyba (Meteo.lt), https://api.meteo.lt/.
4. Jei miesto duomenys neprieinami, nerašyk spėjimų: pateik „Duomenų nėra“ ir trumpai nurodyk klaidą. Jei visos užklausos nesėkmingos, pranešk apie nepasiekiamą šaltinį.
5. Jei vartotojas nurodo kitą laiką ar prašo faktinių matavimų, šis scenarijus netinka be atitinkamo pritaikymo; nepateik prognozės kaip matavimo.

Duomenų gavimas vykdomas per oficialų `GET /v1/places/{place-code}/forecasts/long-term` endpointą. Nekopijuok ankstesnių rezultatų kaip naujų.
