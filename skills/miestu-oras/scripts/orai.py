#!/usr/bin/env python3
"""Dabartiniai penkių Lietuvos miestų orai per Foreca Weather API."""
import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

# Foreca API priima koordinates formatu longitude,latitude.
CITIES = [
    ("Vilnius", 25.2797, 54.6872),
    ("Kaunas", 23.9036, 54.8985),
    ("Klaipėda", 21.1175, 55.7033),
    ("Šiauliai", 23.3137, 55.9349),
    ("Panevėžys", 24.3595, 55.7348),
]


def fetch(city, longitude, latitude, api_key):
    url = (
        f"https://weatherapi.foreca.net/api/v1/current/{longitude},{latitude}"
        "?lang=lt&tempunit=C&tz=Europe%2FVilnius"
    )
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": "miestu-oras/2.0",
        },
    )
    try:
        with urlopen(request, timeout=15) as response:
            data = json.load(response)
        current = data["current"]
        temperature = current.get("temperature")
        if temperature is None:
            raise ValueError("Temperatūros duomenų nėra")
        raw_time = current["time"]
        timestamp = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            # API užklausoje aiškiai prašoma Europe/Vilnius laiko.
            timestamp = timestamp.replace(tzinfo=ZoneInfo("Europe/Vilnius"))
        local_time = timestamp.astimezone(ZoneInfo("Europe/Vilnius"))
        return {
            "miestas": city,
            "temperatura_c": temperature,
            "salygos": current.get("symbolPhrase") or "Nenustatyta",
            "laikas_lietuvoje": local_time.strftime("%Y-%m-%d %H:%M"),
            "tipas": "dabartinių orų įvertinimas",
        }
    except HTTPError as exc:
        reason = "Neteisingas arba neaktyvus Foreca API raktas" if exc.code in (401, 403) else f"HTTP {exc.code}"
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
    api_key = os.environ.get("FORECA_API_KEY", "").strip()
    if not api_key:
        print("Trūksta FORECA_API_KEY aplinkos kintamojo.", file=sys.stderr)
        return 2
    now = datetime.now(timezone.utc)
    results = [fetch(city, lon, lat, api_key) for city, lon, lat in CITIES]
    print(json.dumps({
        "saltinis": "Foreca Weather API",
        "saltinio_url": "https://developer.foreca.com/",
        "gauta_utc": now.isoformat(),
        "miestai": results,
    }, ensure_ascii=False, indent=2))
    return 1 if all(item["temperatura_c"] is None for item in results) else 0


if __name__ == "__main__":
    sys.exit(main())
