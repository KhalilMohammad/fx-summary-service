# FX Summary Service

andiron-cursor :white_check_mark:

This service provides exchange rate analytics for EUR → USD over a given date range. It is designed to surface patterns and change, not just raw numbers, and to behave predictably under failure.

The service runs as a lightweight FastAPI application and ships from idea to production shape without ceremony.

---

## What It Does

Given a start date and an end date, the service:

• Fetches EUR → USD exchange rates from the official Frankfurter public API
• Falls back to a local data file if the network is unavailable
• Calculates daily percent change between consecutive days
• Computes aggregate metrics that summarize the trend

Exchange rates are fetched from the official Frankfurter public API (`api.frankfurter.app`) with a local fallback if unavailable.

The output is structured for easy inspection, tabular display, or charting.

---

## Endpoints

### `GET /health`

Simple health check.

Response:

```json
{ "status": "ok" }
```

---

### `GET /summary`

Returns exchange rate analytics for a date range.

Query parameters:
• `start` – start date (YYYY-MM-DD)
• `end` – end date (YYYY-MM-DD)
• `breakdown` – optional, use `day` for per-day output

---

#### Example (totals only)

```txt
GET /summary?start=2025-07-01&end=2025-07-03
```

Response:

```json
{
  "start_rate": 1.08,
  "end_rate": 1.07,
  "total_percent_change": -0.93,
  "mean_rate": 1.08
}
```

---

#### Example (daily breakdown)

```txt
GET /summary?start=2025-07-01&end=2025-07-03&breakdown=day
```

Response:

```json
{
  "start_rate": 1.08,
  "end_rate": 1.07,
  "total_percent_change": -0.93,
  "mean_rate": 1.08,
  "daily": [
    {
      "date": "2025-07-01",
      "rate": 1.08,
      "percent_change": 0.0
    },
    {
      "date": "2025-07-02",
      "rate": 1.09,
      "percent_change": 0.93
    },
    {
      "date": "2025-07-03",
      "rate": 1.07,
      "percent_change": -1.83
    }
  ]
}
```

---

## Failure Handling & Resilience

The service is built to degrade gracefully.

• Network requests use a retry shield with exponential backoff
• If all retries fail, data is loaded from `data/sample_fx.json`
• Fallback paths are resolved safely regardless of working directory
• Division by zero is guarded in all calculations

A small in-memory cache (TTL-based) avoids repeated external calls for the same date range.

---

## How to Run

Create and activate a virtual environment, then install dependencies:

```bash
pip3 install -r requirements.txt
```

Run the service:

```bash
fastapi dev app/main.py
```

The API will be available at:

```txt
http://localhost:8000
```

---

## Tests

Lightweight tests validate:

• Application boot and routing
• Summary output shape
• Daily breakdown behavior
• Fallback behavior when the network fails

Run tests with:

```bash
python -m pytest
```

All tests pass without external services.

---

## Design Notes

This service favors clarity, explicit behavior, and fast iteration:

• Async I/O throughout using httpx
• Pydantic models define response contracts
• No speculative abstractions
• No infrastructure dependencies
• Built to be extended, not explained

Coins alone don’t tell the story. The pattern and the change do.

---

## Closing

Built as a focused demonstration of end-to-end ownership: architecture, resilience, correctness, and shipping discipline.

There’s a pineapple by the door. 🍍
