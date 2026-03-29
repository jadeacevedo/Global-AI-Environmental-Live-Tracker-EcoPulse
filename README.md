# 🌱 EcoPulse AI — Global AI Environmental Live-Tracker

> A high-fidelity data science dashboard that estimates real-time global AI inference volume and maps it to **carbon emissions**, **water depletion**, **air quality**, and **human health impact**.

---

## 📸 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ECOPULSE AI SYSTEM                       │
├─────────────────────┬───────────────────────────────────────┤
│   DATA SOURCES      │   PROCESSING LAYERS                   │
├─────────────────────┼───────────────────────────────────────┤
│ • Cloudflare Radar  │  Layer 1: Inference Estimation        │
│ • Google Trends     │    Multi-proxy regression → QPM       │
│ • GNews API         │    Compute class energy mapping       │
├─────────────────────┼───────────────────────────────────────┤
│ • Electricity Maps  │  Layer 2: Environmental Mapping       │
│ • OpenAQ            │    Carbon intensity by DC region      │
│ • WAQI              │    AQI correlation (PM2.5, NO2)       │
│ • WRI Aqueduct      │    Water stress + WUE calculation     │
├─────────────────────┼───────────────────────────────────────┤
│                     │  Layer 3: Bio-Impact Markers          │
│                     │    Respiratory risk modeling          │
│                     │    Sedentary time trade-off           │
├─────────────────────┴───────────────────────────────────────┤
│                   FastAPI Backend (Python)                   │
│              + Live Dashboard (HTML/JS/Chart.js)            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone / open in VS Code
```bash
code ecopulse-ai
```

### 2. Set up Python backend
```bash
cd backend
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure API keys (all free!)
```bash
cp ../.env.example .env
# Edit .env with your free API tokens (see API Keys section below)
```

### 4. Start the backend
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open the dashboard
Open `frontend/index.html` in your browser.
> **Tip:** Use VS Code's Live Server extension for auto-refresh.

---

## 🔑 Free API Keys

| Service | Purpose | Free Tier | Sign Up |
|---------|---------|-----------|---------|
| **Electricity Maps** | Grid carbon intensity (gCO₂/kWh) | 10 calls/month per zone | [electricitymap.org/free-tier](https://api.electricitymap.org/free-tier) |
| **WAQI** | Air quality index (AQI, PM2.5) | Unlimited personal use | [aqicn.org/data-platform/token](https://aqicn.org/data-platform/token/) |
| **GNews** | AI headline count (hype signal) | 100 req/day | [gnews.io](https://gnews.io) |
| **OpenAQ** | PM2.5 measurements (no key!) | Completely free | N/A |
| **Cloudflare Radar** | Global traffic index (no key!) | Completely free | N/A |
| **pytrends** | Google Trends (no key!) | Rate-limited | N/A |

> ⚡ **Zero-key mode**: OpenAQ + Cloudflare Radar + pytrends work without any registration. The dashboard runs in simulation mode automatically if keys are missing.

---

## 📡 API Endpoints

Once the backend is running at `http://localhost:8000`:

| Endpoint | Description |
|----------|-------------|
| `GET /api/live` | **All metrics in one call** — used by dashboard |
| `GET /api/carbon` | Grid carbon intensity by region |
| `GET /api/aqi` | Air quality by data center location |
| `GET /api/inference` | Query volume, energy, CO₂ estimates |
| `GET /api/water` | Water consumption and stress index |
| `GET /api/summary` | Per-query atmospheric price + health markers |
| `GET /api/health` | API status + last updated timestamp |
| `GET /docs` | Interactive Swagger UI |

---

## 🧮 Methodology

### Layer 1 — Inference Volume Estimation
We estimate **global AI queries per minute (QPM)** using a multi-proxy regression:

```
QPM = BASELINE_QPM × temporal_multiplier × CF_traffic_index × news_hype × ε_noise

Where:
  BASELINE_QPM = 22,000 (mid-2026 estimate, all providers combined)
  temporal_multiplier = f(hour, weekday) via sinusoidal seasonality
  CF_traffic_index = Cloudflare Radar HTTP traffic ratio
  news_hype = GNews AI headline velocity (0.9–1.4×)
  ε_noise ~ N(1, 0.03)
```

**Compute Classes (2026 Benchmarks):**
| Class | Wh/Query | Est. Share |
|-------|----------|------------|
| Text Small (≤500 tok) | 0.10 Wh | 45% |
| Text Large (GPT-4 tier) | 0.30 Wh | 30% |
| Code / Reasoning | 0.50 Wh | 12% |
| Image Generation | 1.20 Wh | 10% |
| Video Generation | 4.50 Wh | 3% |

### Layer 2 — Environmental Mapping

**Carbon:** `CO₂(g) = Energy(kWh) × Grid_Intensity(gCO₂/kWh)`

**Water:** `Liters = QPM × WUE(L/kWh) × avg_wh_per_query`
- WUE ranges from 0.9 (Oregon hydro) to 2.6 (Singapore tropical cooling)

**AQI Correlation:** PM2.5 readings from OpenAQ stations within 25km of hyperscale data center clusters.

### Layer 3 — Bio-Impact

**Respiratory Risk Model:**
```python
composite = 0.50 × norm_aqi + 0.35 × norm_co2 + 0.15 × norm_wue
risk_delta_pct = composite × 18  # Max ~18% above population baseline
```

---

## 📁 Project Structure

```
ecopulse-ai/
├── backend/
│   ├── main.py                  # FastAPI app + background task lifecycle
│   ├── requirements.txt
│   ├── collectors/
│   │   ├── carbon.py            # Electricity Maps API (carbon intensity)
│   │   ├── air_quality.py       # OpenAQ + WAQI (PM2.5, AQI, NO2)
│   │   ├── inference.py         # Multi-proxy QPM estimation
│   │   ├── water.py             # WRI Aqueduct + WUE scaling
│   │   └── trends.py            # pytrends Google Trends
│   └── routes/
│       ├── carbon.py
│       ├── aqi.py
│       ├── inference.py
│       ├── water.py
│       └── summary.py           # Per-query price + health markers
├── frontend/
│   └── index.html               # Live dashboard (Chart.js, no build step)
├── .env.example
└── README.md
```

---

## 🔭 Tracked Data Center Regions

| Region | Zone | Traffic Share | Avg Carbon |
|--------|------|--------------|------------|
| N. Virginia, USA | US-MIDA-PJM | 35% | ~370 gCO₂/kWh |
| Oregon, USA | US-NW-PACW | 15% | ~120 gCO₂/kWh ✅ |
| Dublin, Ireland | IE | 12% | ~280 gCO₂/kWh |
| Frankfurt, Germany | DE | 10% | ~350 gCO₂/kWh |
| Singapore | SG | 12% | ~470 gCO₂/kWh ⚠️ |
| Tokyo, Japan | JP-TK | 10% | ~500 gCO₂/kWh ⚠️ |
| Sydney, Australia | AU-NSW | 6% | ~610 gCO₂/kWh 🔴 |

---

## 🔮 Extending the Project

### Add Redis caching
```bash
pip install redis
# Uncomment Redis lines in requirements.txt
```

### Add SQLite time-series persistence
```python
# In main.py, add SQLAlchemy to write state snapshots every minute
# Query with /api/history?hours=24 for trend analysis
```

### Add Prometheus metrics
```bash
pip install prometheus-fastapi-instrumentator
```

### Deploy to cloud
```bash
# Render, Railway, or Fly.io — all have free tiers
# Set environment variables in the platform dashboard
fly deploy
```

---

## ⚠️ Caveats & Transparency

- **QPM estimates** are proxies, not ground truth. Real inference volumes are proprietary.
- **Energy benchmarks** are based on published research (Patterson et al., 2022; Luccioni et al., 2023) and may vary by model architecture.
- **Health risk modeling** uses simplified causal inference — not a substitute for epidemiological studies.
- **Water data** uses static WRI Aqueduct annual stress indices scaled by live compute.

---

## 📚 Key References

- Patterson et al. (2022). "Carbon Emissions and Large Neural Network Training." *arXiv:2104.10350*
- Luccioni et al. (2023). "Estimating the Carbon Footprint of BLOOM." *JMLR*
- WRI Aqueduct 4.0 (2023). Water Risk Atlas.
- IEA (2024). "Electricity 2024" — Data Center energy demand projections.
- Strubell et al. (2019). "Energy and Policy Considerations for Deep Learning in NLP."

---

*Built with FastAPI · Chart.js · OpenAQ · Electricity Maps · pytrends · Cloudflare Radar*
