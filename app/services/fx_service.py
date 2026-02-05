import json
import asyncio
import time
from pathlib import Path
from typing import Dict

import httpx

from app.models.response import SummaryResponse, DailyRate
from app.utils.math import percent_change

FRANKFURTER_RANGE = "https://api.frankfurter.app/{start}..{end}"
CACHE_TTL_SECONDS = 60

# simple in-memory cache
_cache: Dict[str, dict] = {}

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FALLBACK_FILE = BASE_DIR / "data" / "sample_fx.json"


async def fetch_rates(start: str, end: str) -> dict:
    cache_key = f"{start}:{end}"
    now = time.time()

    # cache hit
    if cache_key in _cache:
        entry = _cache[cache_key]
        if now - entry["ts"] < CACHE_TTL_SECONDS:
            return entry["data"]

    url = FRANKFURTER_RANGE.format(start=start, end=end)
    params = {"from": "EUR", "to": "USD"}

    backoff = 0.5

    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(url, params=params)
                res.raise_for_status()
                data = res.json()["rates"]

                _cache[cache_key] = {"ts": now, "data": data}
                return data

        except Exception:
            if attempt == 2:
                break
            await asyncio.sleep(backoff)
            backoff *= 2

    # fallback
    with FALLBACK_FILE.open() as f:
        return json.load(f)["rates"]


async def get_summary(start: str, end: str, breakdown: str) -> SummaryResponse:
    rates = await fetch_rates(start, end)

    days = sorted(rates.keys())
    values = [rates[d]["USD"] for d in days]

    start_rate = values[0]
    end_rate = values[-1]

    daily = []
    prev = None

    for d in days:
        rate = rates[d]["USD"]
        change = percent_change(prev, rate) if prev is not None else 0.0
        daily.append(DailyRate(date=d, rate=rate, percent_change=change))
        prev = rate

    response = SummaryResponse(
        start_rate=start_rate,
        end_rate=end_rate,
        total_percent_change=percent_change(start_rate, end_rate),
        mean_rate=sum(values) / len(values),
        daily=daily if breakdown == "day" else None
    )

    return response
