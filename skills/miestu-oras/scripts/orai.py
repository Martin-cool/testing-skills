#!/usr/bin/env python3
"""Artimiausia penkių Lietuvos miestų prognozė per Yr.no / MET Norway API."""
import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

CITIES = [
    ("Vilnius", 54.6872, 25.2797),
    ("Kaunas", 54.8985, 23.9036),
    ("Klaipėda", 55.7033, 21.1175),
    ("Šiauliai", 55.9349, 23.3137),
    ("Panevėžys", 55.7348, 24.3595),
]
DEFAULT_USER_AGENT = "miestu-oras/1.0 https://github.com/Martin-cool/testing-skills"
CONDITIONS = {
    "clearsky": "Giedra",
    "fair": "Mažai debesuota",
    "partlycloudy": "Debesuota su pragiedruliais",
    "cloudy": "Debesuota",
    "fog": "Rūkas",
    "lightrain": "Nedidelis lietus",
    "rain": "Lietus",
    "heavyrain": "Smarkus lietus",
    "lightsnow": "Nedidelis sniegas",
    "snow": "Sniegas",
    "heavysnow": "Smarkus sniegas",
    "lightsleet": "Nedidelė šlapdriba",
    "sleet": "Šlapdriba",
    "heavysleet": "Smarki šlapdriba",
    "rainshowers": "Lietaus šuorai",
    "lightrainshowers": "Nedideli lietaus šuorai",
    "heavyrainshowers": "Smarkūs lietaus šuorai",
    "snowshowers": "Sniego šuorai",
    "sleetshowers": "Šlapdribos šuorai",
    "rainandthunder": "Lietus su perkūnija",
    "snowandthunder": "Sniegas su perkūnija",
    "sleetandthunder": "Šlapdriba su perkūnija",
}


def describe(code):
    if not code:
        return "Nenustatyta"
    base = code.removesuffix("_day").removesuffix("_night").removesuffix("_polartwilight")
    if base in CONDITIONS:
        return CONDITIONS[base]
    if "thunder" in base:
        return "Krituliai su perkūnija"
    if "snow" in base:
        return "Sniegas"
    if "sleet" in base:
        return "Šlapdriba"
    if "rain" in base:
        return "Lietus"
    return code


def fetch_yr(city, lat, lon, user_agent, now):
    url = (
        "https://api.met.no/weatherapi/locationforecast/2.0/compact"
        f"?lat={lat:.4f}&lon={lon:.4f}"
    )
    try:
        request = Request(url, headers={
            "User-Agent": user_agent,
            "Accept": "application/json",
        })
        with urlopen(request, timeout=15) as response:
            data = json.load(response)
        timeseries = data["properties"]["timeseries"]
        forecasts = []
        for entry in timeseries:
            timestamp = datetime.fromisoformat(entry["time"].replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            forecasts.append((timestamp.astimezone(timezone.utc), entry))
        upcoming = [(t, entry) for t, entry in forecasts if t >= now]
        if not upcoming:
            raise ValueError("Nėra būsimos prognozės")
        timestamp, entry = min(upcoming, key=lambda item: item[0])
        details = entry["data"]["instant"]["details"]
        temperature = details["air_temperature"]
        next_data = entry["data"]
        symbol = None
        for period in ("next_1_hours", "next_6_hours", "next_12_hours"):
            symbol = next_data.get(period, {}).get("summary", {}).get("symbol_code")
            if symbol:
                break
        return {
            "miestas": city,
            "temperatura_c": temperature,
            "salygos": describe(symbol),
            "laikas_lietuvoje": timestamp.astimezone(
                ZoneInfo("Europe/Vilnius")
            ).strftime("%Y-%m-%d %H:%M"),
            "tipas": "prognozė",
            "saltinis": "MET Norway / Yr.no",
        }
    except HTTPError as exc:
        reason = f"HTTP {exc.code}"
    except (URLError, TimeoutError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        reason = str(exc)
    return {
        "miestas": city,
        "temperatura_c": None,
        "salygos": "Duomenų nėra",
        "laikas_lietuvoje": None,
        "klaida": reason,
    }


OPEN_METEO_CODES = {
    0: "Giedra", 1: "Mažai debesuota", 2: "Debesuota su pragiedruliais",
    3: "Debesuota", 45: "Rūkas", 48: "Šerkšnotas rūkas",
    51: "Silpna dulksna", 53: "Dulksna", 55: "Stipri dulksna",
    56: "Šąlanti dulksna", 57: "Stipri šąlanti dulksna",
    61: "Nedidelis lietus", 63: "Lietus", 65: "Smarkus lietus",
    66: "Šąlantis lietus", 67: "Smarkus šąlantis lietus",
    71: "Nedidelis sniegas", 73: "Sniegas", 75: "Smarkus sniegas",
    77: "Sniego kruopos", 80: "Nedideli lietaus šuorai",
    81: "Lietaus šuorai", 82: "Smarkūs lietaus šuorai",
    85: "Nedideli sniego šuorai", 86: "Smarkūs sniego šuorai",
    95: "Perkūnija", 96: "Perkūnija su kruša", 99: "Smarki perkūnija su kruša",
}


def fetch_open_meteo(city, lat, lon):
    params = urlencode({
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,weather_code",
        "timezone": "Europe/Vilnius",
    })
    request = Request(
        "https://api.open-meteo.com/v1/forecast?" + params,
        headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "application/json"},
    )
    with urlopen(request, timeout=15) as response:
        data = json.load(response)
    current = data["current"]
    return {
        "miestas": city,
        "temperatura_c": current["temperature_2m"],
        "salygos": OPEN_METEO_CODES.get(current["weather_code"], "Nenustatyta"),
        "laikas_lietuvoje": current["time"].replace("T", " "),
        "tipas": "modelio duomenys",
        "saltinis": "Open-Meteo",
    }


def fetch(city, lat, lon, user_agent, now):
    result = fetch_yr(city, lat, lon, user_agent, now)
    if result["temperatura_c"] is not None:
        return result
    yr_error = result.get("klaida", "Nežinoma klaida")
    try:
        fallback = fetch_open_meteo(city, lat, lon)
        fallback["pastaba"] = "Yr.no nepasiekiamas: " + yr_error
        return fallback
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        result["klaida"] = "Yr.no: " + yr_error + "; Open-Meteo: " + str(exc)
        return result


def main():
    user_agent = os.environ.get("YR_USER_AGENT", DEFAULT_USER_AGENT).strip()
    if not user_agent:
        print("YR_USER_AGENT negali būti tuščias.", file=sys.stderr)
        return 2
    now = datetime.now(timezone.utc)
    results = [fetch(city, lat, lon, user_agent, now) for city, lat, lon in CITIES]
    print(json.dumps({
        "saltinis": "MET Norway / Yr.no (atsarginis: Open-Meteo)",
        "saltinio_url": "https://api.met.no/",
        "atsarginio_saltinio_url": "https://open-meteo.com/",
        "gauta_utc": now.isoformat(),
        "miestai": results,
    }, ensure_ascii=False, indent=2))
    return 1 if all(item["temperatura_c"] is None for item in results) else 0


if __name__ == "__main__":
    sys.exit(main())
