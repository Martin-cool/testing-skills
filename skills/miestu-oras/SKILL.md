---
name: miestu-oras
description: Pateikti dabartinę penkių didžiausių Lietuvos miestų (Vilniaus, Kauno, Klaipėdos, Šiaulių ir Panevėžio) oro temperatūrą bei sąlygas iš Foreca Weather API. Naudoti, kai vartotojas prašo šių miestų orų arba temperatūrų palyginimo.
---

# Miestų oras

1. Įsitikink, kad aplinkos kintamajame `FORECA_API_KEY` yra naudotojo Foreca Weather API raktas. Niekada nerodyk jo atsakyme, žurnaluose ar repozitorijoje. Jei rakto nėra, paaiškink, kaip jį nustatyti, ir neišgalvok duomenų.
2. Paleisk `python scripts/orai.py` iš šio skill katalogo (reikia interneto).
3. Pateik lietuvišką lentelę su penkiais miestais, temperatūra (°C), oro sąlygomis ir Foreca duomenų laiku Lietuvos laiku.
4. Nurodyk, kad tai Foreca **dabartinių orų įvertinimas** (ne meteorologinės stoties matavimas). Šaltinis: Foreca Weather API, https://developer.foreca.com/.
5. Jei kuriam nors miestui užklausa nepavyko, parodyk „Duomenų nėra“, nekurk spėjimų. Jei visos užklausos nesėkmingos, paaiškink priežastį.
6. Jei vartotojas prašo prognozės kitai dienai ar faktinių stoties matavimų, šis dabartinių orų skriptas tam netinka.

Naudojamas oficialus `GET https://weatherapi.foreca.net/api/v1/current/{longitude},{latitude}` su `Authorization: Bearer` ir `lang=lt`. API raktas privalomas.
