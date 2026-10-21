---
name: miestu-oras
description: Gauti penkių didžiausių Lietuvos miestų (Vilniaus, Kauno, Klaipėdos, Šiaulių ir Panevėžio) artimiausios prognozės oro temperatūrą ir sąlygas iš Yr.no (MET Norway API), o jei jis nepasiekiamas – iš Open-Meteo. Naudoti, kai prašoma šių miestų orų.
---

# Miestų oras

1. Paleisk `python scripts/orai.py` iš šio katalogo; reikalingas interneto ryšys.
2. Pateik lietuvišką lentelę: miestas, temperatūra (°C), oro sąlygos ir prognozės laikas Lietuvos laiku.
3. Paaiškink, kad Yr.no pateikia **artimiausią prognozę**, o Open-Meteo – **dabartinio laiko modelio duomenis**; tai nėra tiesioginiai meteorologijos stoties matavimai.
4. Kiekvienam miestui nurodyk faktiškai naudotą šaltinį: MET Norway / Yr.no (https://api.met.no/) arba Open-Meteo (https://open-meteo.com/).
5. Jei duomenys neprieinami, pateik „Duomenų nėra“ ir nespekuliuok.

Skriptas naudoja `GET https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=...&lon=...`. API rakto nereikia. Privalomas identifikuojantis `User-Agent` su kontaktine informacija. Nustatyk `YR_USER_AGENT` pagal savo programą (pvz. `miestu-oras/1.0 https://github.com/Martin-cool/testing-skills`); nekeisk jo į apsimestinį. Atsižvelk į API naudojimo ir talpyklos taisykles.

Jei Yr.no neveikia, skriptas automatiškai bando Open-Meteo be API rakto; jei abu šaltiniai nepasiekiami, rodo klaidą.
