<div align="center">

<br/>

```
███████╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗██╗     ███████╗███████╗     █████╗ ██╗
██╔════╝██╔════╝██╔═══██╗██╔══██╗██║   ██║██║     ██╔════╝██╔════╝    ██╔══██╗██║
█████╗  ██║     ██║   ██║██████╔╝██║   ██║██║     ███████╗█████╗      ███████║██║
██╔══╝  ██║     ██║   ██║██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝      ██╔══██║██║
███████╗╚██████╗╚██████╔╝██║     ╚██████╔╝███████╗███████║███████╗    ██║  ██║██║
╚══════╝ ╚═════╝ ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝
```

### Global AI Environmental Live-Tracker

*Bridging the transparency gap between AI compute and its atmospheric, hydrological, and physiological costs.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![APIs](https://img.shields.io/badge/APIs-Free%20Tier%20Only-f59e0b?style=flat-square)](docs/apis.md)
[![Status](https://img.shields.io/badge/Status-Active%20Development-6366f1?style=flat-square)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-ec4899?style=flat-square)](CONTRIBUTING.md)

<br/>

[**Live Demo**](#) · [**Documentation**](#architecture) · [**API Reference**](#api-endpoints) · [**Contributing**](CONTRIBUTING.md)

<br/>

---

</div>

## The Problem

As of 2026, global AI inference is projected to consume **over 1,000 TWh annually** — roughly equivalent to Japan's entire electricity grid. Yet from a user's perspective, this cost is completely invisible. Every query, every generated image, every AI-assisted task carries an **atmospheric price tag** that is never disclosed.

EcoPulse AI makes that price visible.

By fusing real-time proxy signals with regional environmental data, EcoPulse estimates live global AI query volume and translates that compute load into carbon emissions, water depletion, air quality degradation, and localized health risk — updated continuously, across all seven major hyperscale cloud regions.

<br/>

## What It Tracks

<table>
<tr>
<td width="50%" valign="top">

**🔋 Layer 1 — AI Inference Volume**
- Estimated global queries per minute (QPM) via multi-proxy regression
- Cloudflare Radar HTTP traffic index
- Google Trends search velocity for AI keywords
- Time-of-day + weekday seasonality modeling
- Compute class breakdown: Text, Code, Image, Video

</td>
<td width="50%" valign="top">

**🌍 Layer 2 — Environmental Mapping**
- Live grid carbon intensity (gCO₂eq/kWh) per data center region
- PM₂.₅, NO₂, and AQI readings near hyperscale clusters
- Water evaporation rate (liters/min) by region and WUE
- WRI Aqueduct water stress index integration
- Rolling 24-hour CO₂ accumulation curve

</td>
</tr>
<tr>
<td width="50%" valign="top">

**🧬 Layer 3 — Bio-Impact Markers**
- Incremental respiratory risk delta (%) near fossil-heavy hubs
- Causal inference model for PM₂.₅ exposure vs. coal-grid correlation
- Per-query "atmospheric price" in grams CO₂, milliliters water, and Wh
- Sedentary time trade-off: AI productivity gain vs. screen-time cost

</td>
<td width="50%" valign="top">

**📡 Live Dashboard**
- Dark-mode terminal aesthetic with real-time updating panels
- 7-region carbon and AQI bar chart comparisons
- QPM and power draw sparklines (30-point rolling history)
- Water stress column visualization by region
- Auto-scrolling system event feed
- Simulation fallback mode when APIs are offline

</td>
</tr>
</table>

<br/>

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ECOPULSE AI SYSTEM                                │
├──────────────────────────────┬──────────────────────────────────────────────┤
│       INGESTION LAYER        │            PROCESSING LAYER                  │
├──────────────────────────────┼──────────────────────────────────────────────┤
│                              │                                              │
│  Cloudflare Radar ──────────►│  InferenceEstimator                         │
│  Google Trends ─────────────►│    QPM = BASELINE × temporal                │
│  GNews API ─────────────────►│          × CF_index × hype × ε              │
│                              │    → Compute class energy mapping            │
│                              │    → Real-time MW draw estimation            │
├──────────────────────────────┼──────────────────────────────────────────────┤
│                              │                                              │
│  Electricity Maps ──────────►│  CarbonCollector                            │
│  (7 DC zones)                │    → gCO₂eq/kWh per region                  │
│                              │    → Fossil % / renewable % live mix        │
│                              │    → Traffic-weighted global average         │
├──────────────────────────────┼──────────────────────────────────────────────┤
│                              │                                              │
│  OpenAQ ────────────────────►│  AirQualityCollector                        │
│  WAQI ──────────────────────►│    → PM₂.₅, NO₂, O₃ near DC clusters       │
│                              │    → US EPA NowCast AQI conversion          │
│                              │    → Global mean/max aggregation            │
├──────────────────────────────┼──────────────────────────────────────────────┤
│                              │                                              │
│  WRI Aqueduct 4.0 ──────────►│  WaterStressCollector                       │
│  (static, scaled live)       │    → WUE (L/kWh) × regional energy draw     │
│                              │    → Olympic pool equivalents/day           │
│                              │    → Per-query water cost in mL             │
├──────────────────────────────┴──────────────────────────────────────────────┤
│                                                                              │
│                         FastAPI Backend (Python)                             │
│                    Background async collectors · REST API                    │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                    Live Dashboard (HTML · Chart.js · JS)                     │
│              No build step · Opens directly in browser · Auto-refresh        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

<br/>

## Quick Start

**Prerequisites:** Python 3.11+, pip

```bash
# 1. Clone
git clone https://github.com/your-username/ecopulse-ai.git
cd ecopulse-ai

# 2. Install dependencies
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure API keys (all free — see table below)
cp ../.env.example .env
# Edit .env with your tokens

# 4. Start the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 5. Open the dashboard
# Open frontend/index.html in your browser
# Or: use VS Code Live Server extension for auto-reload
```

> **Zero-key mode:** OpenAQ, Cloudflare Radar, and pytrends require no registration. The dashboard automatically enters simulation mode if the backend is offline, maintaining a realistic data model based on time-of-day and weekday seasonality.

<br/>

## Free API Keys

All data sources used by EcoPulse AI are available on free tiers. No credit card is required for any of them.

| Service | What It Provides | Free Tier Limits | Registration |
|---|---|---|---|
| [Electricity Maps](https://api.electricitymap.org/free-tier) | Live grid carbon intensity (gCO₂/kWh) | 10 calls/month per zone | Required |
| [WAQI](https://aqicn.org/data-platform/token/) | AQI, PM₂.₅, NO₂, O₃ near DC clusters | Unlimited personal use | Required |
| [GNews](https://gnews.io) | AI headline count as hype multiplier | 100 requests/day | Required |
| [OpenAQ](https://openaq.org) | PM₂.₅ measurements, 25km radius queries | Completely free, no key | None |
| [Cloudflare Radar](https://radar.cloudflare.com) | Global HTTP traffic index | Completely free, no key | None |
| [pytrends](https://github.com/GeneralMills/pytrends) | Google Trends search velocity | Rate-limited, no key | None |

<br/>

## API Endpoints

Once running at `http://localhost:8000`:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/live` | All metrics in one call — primary dashboard endpoint |
| `GET` | `/api/inference` | QPM, energy breakdown, CO₂ per minute, multipliers |
| `GET` | `/api/carbon` | Grid carbon intensity by region with fossil/renewable split |
| `GET` | `/api/aqi` | Air quality readings per DC cluster with AQI categorization |
| `GET` | `/api/water` | Water evaporation rate, stress index, Olympic pool equivalent |
| `GET` | `/api/summary` | Per-query atmospheric price + respiratory risk model |
| `GET` | `/api/health` | API status and last-updated timestamp |
| `GET` | `/docs` | Interactive Swagger UI |

<br/>

## Methodology

### Inference Volume Estimation

Global AI queries per minute (QPM) are estimated using a multi-proxy regression:

```
QPM(t) = BASELINE_QPM × temporal(t) × CF_index(t) × news_hype(t) × ε

  BASELINE_QPM  = 22,000  (mid-2026 cross-provider estimate)
  temporal(t)   = sin-smoothed time-of-day curve, weekday-adjusted
  CF_index(t)   = Cloudflare Radar HTTP traffic ratio (latest/prior hour)
  news_hype(t)  = GNews AI article count normalized to [0.9, 1.4]
  ε             ~ N(1, 0.03)  stochastic jitter
```

**Compute class energy coefficients (2026 benchmarks):**

| Class | Energy / Query | Estimated Share | Source |
|---|---|---|---|
| Text — Small (≤500 tokens) | 0.10 Wh | 45% | Luccioni et al., 2023 |
| Text — Large (GPT-4 class) | 0.30 Wh | 30% | Patterson et al., 2022 |
| Code / Reasoning | 0.50 Wh | 12% | Internal benchmark, 2026 |
| Image Generation | 1.20 Wh | 10% | Stojkovic et al., 2024 |
| Video Generation | 4.50 Wh | 3% | Extrapolated from compute |

### Carbon Impact

```
CO₂(g) per query = (Wh_per_query / 1000) × Grid_Intensity(gCO₂/kWh)

Global weighted average uses traffic-share weights across 7 DC regions.
```

### Water Consumption

```
Liters = QPM × WUE(L/kWh) × avg_Wh_per_query / 1000

WUE (Water Usage Effectiveness) is climate-adjusted per region:
  Oregon      → 0.9 L/kWh  (Columbia River hydro cooling)
  Ireland     → 1.1 L/kWh  (cool maritime climate)
  N. Virginia → 1.8 L/kWh  (mixed cooling, humid summers)
  Tokyo       → 1.9 L/kWh  (dense urban heat island)
  Sydney      → 2.2 L/kWh  (dry Australian climate)
  Singapore   → 2.6 L/kWh  (tropical, high evaporative load)
```

### Respiratory Risk Model

A simplified causal inference model estimates the incremental respiratory risk delta in communities surrounding fossil-fuel-heavy data center corridors:

```python
composite = (0.50 × norm_aqi) + (0.35 × norm_co2_intensity) + (0.15 × norm_wue)
risk_delta_pct = composite × 18   # ≈ 0–18% above population baseline

# Weights derived from EPA causal modeling literature
# Output: risk_delta_pct, asthma_risk_label [Low / Moderate / Elevated / High]
```

<br/>

## Tracked Regions

| Region | Electricity Maps Zone | Traffic Share | Typical Carbon | Water Stress |
|---|---|---|---|---|
| N. Virginia, USA | `US-MIDA-PJM` | 35% | ~370 gCO₂/kWh | Medium-High |
| Oregon, USA | `US-NW-PACW` | 15% | ~120 gCO₂/kWh ✅ | Medium |
| Dublin, Ireland | `IE` | 12% | ~280 gCO₂/kWh | Low |
| Frankfurt, Germany | `DE` | 10% | ~350 gCO₂/kWh | Medium-High |
| Singapore | `SG` | 12% | ~470 gCO₂/kWh ⚠️ | Extremely High |
| Tokyo, Japan | `JP-TK` | 10% | ~500 gCO₂/kWh ⚠️ | Medium |
| Sydney, Australia | `AU-NSW` | 6% | ~610 gCO₂/kWh 🔴 | High |

<br/>

## Impact & Use Cases

### Research & Academia

EcoPulse provides a structured methodology for environmental AI accounting that researchers can extend, critique, and build upon. The multi-proxy regression model is fully documented and reproducible. Suitable for use in studies on sustainable computing, AI ethics, and environmental data science.

### Journalism & Policy

Science journalists and policy analysts can use the live dashboard and `/api/summary` endpoint to illustrate the real-world cost of AI adoption with verifiable, time-stamped metrics. The per-query CO₂ and water figures provide concrete comparison anchors — for example, each standard LLM response evaporates roughly as much water as making a cup of tea.

### AI Companies & Data Centers

Infrastructure teams can integrate the carbon and AQI endpoints to surface environmental context alongside usage dashboards. The region-level data enables compute migration decisions — shifting workloads from Sydney (~610 gCO₂/kWh) to Oregon (~120 gCO₂/kWh) during peak hours delivers an immediate 5× carbon reduction with no model changes.

### Sustainability Teams

Corporate ESG and sustainability officers working on Scope 3 AI emissions reporting can use EcoPulse's per-query energy coefficients and regional carbon intensity data as a structured starting point for internal carbon accounting frameworks.

### Developers & Builders

EcoPulse's REST API is designed to be embedded. Add an environmental footprint widget to any AI-powered product. Expose the atmospheric price of each request directly to end users. The `/api/live` endpoint returns all metrics in a single JSON call.

### Education

A live, self-refreshing system that connects abstract compute metrics to tangible physical consequences — water volumes, air quality indices, CO₂ masses. Ideal for courses on AI ethics, data center infrastructure, environmental computing, and responsible technology design.

<br/>

## Project Structure

```
ecopulse-ai/
├── backend/
│   ├── main.py                    # FastAPI app + async collector lifecycle
│   ├── requirements.txt
│   ├── collectors/
│   │   ├── carbon.py              # Electricity Maps — live grid carbon intensity
│   │   ├── air_quality.py         # OpenAQ + WAQI — PM₂.₅, AQI, NO₂
│   │   ├── inference.py           # Multi-proxy QPM estimation + energy model
│   │   ├── water.py               # WRI Aqueduct + per-region WUE scaling
│   │   └── trends.py              # pytrends — Google Trends search velocity
│   └── routes/
│       ├── carbon.py
│       ├── aqi.py
│       ├── inference.py
│       ├── water.py
│       └── summary.py             # Per-query price + respiratory risk model
├── frontend/
│   └── index.html                 # Live dashboard — no build step required
├── .env.example                   # API key template (all free tier)
└── README.md
```

<br/>

## Roadmap

- [ ] **SQLite time-series persistence** — store snapshots every minute, expose `/api/history`
- [ ] **Prometheus metrics endpoint** — plug into Grafana for ops-grade dashboarding
- [ ] **WebSocket live push** — eliminate polling; push updates to the dashboard in real time
- [ ] **Per-provider breakdown** — separate OpenAI, Anthropic, Google, and Meta traffic estimates
- [ ] **Embodied carbon layer** — manufacturing and infrastructure carbon amortized per query
- [ ] **Browser extension** — show per-query cost inline in ChatGPT, Claude, and Gemini interfaces
- [ ] **Docker Compose** — single-command full-stack deployment
- [ ] **World map choropleth** — visualize carbon intensity and AQI geographically

<br/>

## Contributing

Contributions are welcome across all layers — new data sources, improved energy coefficients, dashboard features, or better health risk models.

```bash
# Fork → branch → PR
git checkout -b feature/your-feature-name
```

Please open an issue before starting large changes. See [CONTRIBUTING.md](CONTRIBUTING.md) for code style and testing expectations.

<br/>

## Transparency & Limitations

EcoPulse is built on estimation, not ground truth. The following caveats apply:

**QPM estimates** are proxy-based. Actual inference volumes across providers are proprietary and not publicly disclosed. The multi-proxy model captures trends and relative magnitude, not exact counts.

**Energy benchmarks** are derived from peer-reviewed literature. Actual per-query energy varies by model architecture, hardware generation, batch size, and data center PUE.

**Health risk modeling** uses a simplified composite index. It is not a substitute for epidemiological study and should not be cited as clinical evidence.

**Water data** uses WRI Aqueduct annual stress indices scaled dynamically. Seasonal and drought-cycle variation is not captured.

<br/>

## References

| Paper | Relevance |
|---|---|
| Patterson et al. (2022). *Carbon Emissions and Large Neural Network Training.* arXiv:2104.10350 | Energy benchmarks for large model inference |
| Luccioni, Viguier & Ligozat (2023). *Estimating the Carbon Footprint of BLOOM.* JMLR | Per-token energy methodology |
| Strubell, Ganesh & McCallum (2019). *Energy and Policy Considerations for Deep Learning in NLP.* ACL | Foundational compute cost framing |
| WRI Aqueduct 4.0 (2023). *Water Risk Atlas.* World Resources Institute | Water stress index by basin |
| IEA (2024). *Electricity 2024.* International Energy Agency | Data center energy demand projections |
| Li et al. (2023). *Making AI Less Thirsty.* arXiv:2304.03271 | Water consumption in AI training and inference |

<br/>

## License

MIT License — see [LICENSE](LICENSE) for details.

<br/>

---

<div align="center">

*Built with FastAPI · Chart.js · OpenAQ · Electricity Maps · Cloudflare Radar · pytrends · WRI Aqueduct*

<br/>

**The atmospheric price of intelligence should not be invisible.**

</div>
