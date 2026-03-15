# TradeScope — Python Backend

Technical signal analyzer for NSE/BSE stocks.
Generates BUY/CALL, PUT/SELL, and NEUTRAL signals from RSI, VWAP, and EMA indicators.

---

## Folder structure

```
tradescope-backend/
├── main.py                  ← Start the server from here
├── requirements.txt
├── data/
│   └── fetcher.py           ← Downloads OHLCV data from Yahoo Finance
├── indicators/
│   └── calculator.py        ← Calculates RSI, VWAP, EMA 9/21/50/200
├── signals/
│   └── engine.py            ← Scoring engine → produces BUY/CALL/PUT
└── routes/
    ├── analyze.py            ← GET /api/analyze  (main endpoint)
    └── watchlist.py          ← GET/POST/DELETE /api/watchlist
```

---

## Setup (one time)

### Step 1 — Install Python 3.11+
Download from https://python.org if you don't have it.

### Step 2 — Create a virtual environment
```bash
# Go into the project folder
cd tradescope-backend

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running the server

```bash
uvicorn main:app --reload --port 8000
```

The server will start at: http://localhost:8000

---

## API endpoints

### Main analysis endpoint
```
GET http://localhost:8000/api/analyze?symbol=RELIANCE&timeframe=1d
```

Parameters:
- `symbol`    → Stock name: RELIANCE, TCS, INFY, NIFTY, HDFC, etc.
- `timeframe` → Candle size: 1m, 5m, 15m, 1h, 1d
- `candles`   → How many candles to return (default: 100)

Example response:
```json
{
  "symbol": "RELIANCE",
  "timeframe": "1d",
  "ticker": {
    "price": 2851.40,
    "change_pct": 1.24,
    "open": 2818.00,
    "high": 2863.50,
    "low": 2812.20,
    "volume": 4200000,
    "vwap": 2838.60
  },
  "indicators": {
    "price": 2851.40,
    "rsi": 28.4,
    "rsi_status": "OVERSOLD",
    "vwap": 2838.60,
    "vwap_position": "ABOVE",
    "ema_9": 2847.00,
    "ema_21": 2831.00,
    "ema_50": 2790.00,
    "ema_200": 2620.00,
    "ema_stack": "BULLISH"
  },
  "signal": {
    "label": "BUY / CALL",
    "direction": "bull",
    "arrow": "▲",
    "confidence": 78,
    "score": {
      "rsi": 2, "vwap": 1, "ema_stack": 2, "ema_200": 1,
      "total": 6, "max": 6
    },
    "reasons": [
      { "type": "bull", "text": "RSI at 28.4 — deeply oversold, bounce likely" },
      { "type": "bull", "text": "Price 0.45% above VWAP — bullish institutional bias" }
    ]
  },
  "candles": [ ... ]
}
```

### Live price quote (lightweight)
```
GET http://localhost:8000/api/quote?symbol=RELIANCE
```

### Watchlist
```
GET    http://localhost:8000/api/watchlist
POST   http://localhost:8000/api/watchlist/RELIANCE
DELETE http://localhost:8000/api/watchlist/RELIANCE
GET    http://localhost:8000/api/watchlist/signals
```

### Interactive API docs
After starting the server, open:
http://localhost:8000/docs

This gives you a full Swagger UI where you can test every endpoint.

---

## Connecting to the frontend (trade-signal-analyzer.html)

In the HTML file, replace the `analyze()` function's mock data section with:

```javascript
async function analyze() {
  const sym = document.getElementById('tickerInput').value.trim().toUpperCase();
  const tf = currentTF;

  document.getElementById('chartLoading').classList.add('active');

  const res = await fetch(`http://localhost:8000/api/analyze?symbol=${sym}&timeframe=${tf}`);
  const data = await res.json();

  // data.ticker      → price, change_pct, open, high, low, volume, vwap
  // data.indicators  → rsi, vwap, ema_9/21/50/200, ema_stack
  // data.signal      → label, direction, confidence, score, reasons
  // data.candles     → array of OHLCV + indicator values for charting

  applyApiData(data);  // wire up to your UI elements
  document.getElementById('chartLoading').classList.remove('active');
}
```

---

## Indian market symbols (Yahoo Finance format)

| You type   | Fetched as    |
|------------|---------------|
| RELIANCE   | RELIANCE.NS   |
| TCS        | TCS.NS        |
| INFY       | INFY.NS       |
| HDFC       | HDFCBANK.NS   |
| NIFTY      | ^NSEI         |
| NIFTY 50   | ^NSEI         |
| SENSEX     | ^BSESN        |
| BANKNIFTY  | ^NSEBANK      |

To add more custom mappings, edit `data/fetcher.py` → `SYMBOL_MAP`.

---

## Notes

- Yahoo Finance provides 15-minute delayed data on the free tier.
- For real-time data, use Zerodha Kite Connect or Upstox API v2 (requires account).
- This backend is for educational and paper-trading use only.
- Always test with daily timeframe first — 1m data is only available for the last 7 days.
