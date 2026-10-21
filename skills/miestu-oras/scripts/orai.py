#!/usr/bin/env python3
"""Artimiausios Meteo.lt prognozės penkiems didžiausiems Lietuvos miestams."""
import json
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

CITIES = [('Vilnius', 'vilnius'), ('Kaunas', 'kaunas'), ('Klaipėda', 'klaipeda'), ('Šiauliai', 'siauliai'), ('Panevėžys', 'panevezys')]
CONDITIONS = {
    'clear': 'Giedra', 'partly-cloudy': 'Mažai debesuota',
    'cloudy-with-sunny-intervals': 'Debesuota su pragiedruliais',
    'cloudy': 'Debesuota', 'light-rain': 'Nedidelis lietus',
    'rain': 'Lietus', 'heavy-rain': 'Smarkus lietus',
    'thunder': 'Perkūnija', 'isolated-thunderstorms': 'Trumpas lietus su perkūnija',
    'thunderstorms': 'Lietus su perkūnija',
    'heavy-rain-with-thunderstorms': 'Smarkus lietus su perkūnija',
    'light-sleet': 'Nedidelė šlapdriba', 'sleet': 'Šlapdriba',
    'freezing-rain': 'Lijundra', 'hail': 'Kruša',
    'light-snow': 'Nedidelis sniegas', 'snow': 'Sniegas',
    'heavy-snow': 'Smarkus sniegas', 'fog': 'Rūkas',
}

def parse_utc(value):
    return datetime.fromisoformat(value.replace(' ', 'T').replace('Z', '+00:00')).replace(tzinfo=timezone.utc) if not any(x in value[10:] for x in ('+', 'Z')) else datetime.fromisoformat(value.replace(' ', 'T').replace('Z', '+00:00')).astimezone(timezone.utc)

def fetch(city, code, now):
    url = f'https://api.meteo.lt/v1/places/{code}/forecasts/long-term'
    try:
        with urlopen(Request(url, headers={'User-Agent': 'miestu-oras/1.0', 'Accept': 'application/json'}), timeout=12) as response:
            data = json.load(response)
        entries = [(parse_utc(e['forecastTimeUtc']), e) for e in data['forecastTimestamps']]
        upcoming = [(t, e) for t, e in entries if t >= now]
        if not upcoming:
            raise ValueError('Nėra būsimos prognozės')
        t, entry = min(upcoming, key=lambda item: item[0])
        temperature = entry.get('airTemperature')
        code_value = entry.get('conditionCode')
        return {'miestas': city, 'temperatura_c': temperature,
                'salygos': CONDITIONS.get(code_value, code_value or 'Nenustatyta'),
                'laikas_lietuvoje': t.astimezone(ZoneInfo('Europe/Vilnius')).strftime('%Y-%m-%d %H:%M'),
                'tipas': 'prognozė'}
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return {'miestas': city, 'temperatura_c': None, 'salygos': 'Duomenų nėra',
                'laikas_lietuvoje': None, 'klaida': str(exc)}

def main():
    now = datetime.now(timezone.utc)
    results = [fetch(city, code, now) for city, code in CITIES]
    print(json.dumps({'saltinis': 'Lietuvos hidrometeorologijos tarnyba (Meteo.lt)',
                      'saltinio_url': 'https://api.meteo.lt/',
                      'gauta_utc': now.isoformat(), 'miestai': results}, ensure_ascii=False, indent=2))
    return 1 if all(item['temperatura_c'] is None for item in results) else 0

if __name__ == '__main__':
    sys.exit(main())
