#!/usr/bin/env python3
"""Artimiausia penkių Lietuvos miestų prognozė per Yr.no / MET Norway API."""
import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
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


def fetch(city, lat, lon, user_agent, now):
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


def main():
    user_agent = os.environ.get("YR_USER_AGENT", DEFAULT_USER_AGENT).strip()
    if not user_agent:
        print("YR_USER_AGENT negali būti tuščias.", file=sys.stderr)
        return 2
    now = datetime.now(timezone.utc)
    results = [fetch(city, lat, lon, user_agent, now) for city, lat, lon in CITIES]
    print(json.dumps({
        "saltinis": "MET Norway / Yr.no",
        "saltinio_url": "https://api.met.no/",
        "gauta_utc": now.isoformat(),
        "miestai": results,
    }, ensure_ascii=False, indent=2))
    return 1 if all(item["temperatura_c"] is None for item in results) else 0


if __name__ == "__main__":
    sys.exit(main())
