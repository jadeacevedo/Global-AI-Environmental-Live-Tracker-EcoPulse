"""
Carbon Intensity Collector
Fetches live grid carbon intensity (gCO2eq/kWh) from Electricity Maps API.
Free tier: 10 calls/month per zone → we cache aggressively (every 10 min).

Docs: https://static.electricitymaps.com/api/docs/index.html
Free token: https://api.electricitymap.org/free-tier
"""

import asyncio
import logging
import os
from datetime import datetime, timezone

import httpx

logger = logging.getLogger(__name__)

# Major hyperscale data center regions mapped to Electricity Maps zone codes
DC_ZONES = {
    "us-east-nova":   {"zone": "US-MIDA-PJM",  "label": "N. Virginia",   "lat": 38.9, "lon": -77.4},
    "us-west-oregon": {"zone": "US-NW-PACW",   "label": "Oregon",        "lat": 45.5, "lon": -122.6},
    "eu-ireland":     {"zone": "IE",            "label": "Ireland",       "lat": 53.3, "lon": -6.2},
    "eu-frankfurt":   {"zone": "DE",            "label": "Frankfurt",     "lat": 50.1, "lon": 8.6},
    "ap-singapore":   {"zone": "SG",            "label": "Singapore",     "lat": 1.3,  "lon": 103.8},
    "ap-tokyo":       {"zone": "JP-TK",         "label": "Tokyo",         "lat": 35.7, "lon": 139.7},
    "ap-sydney":      {"zone": "AU-NSW",        "label": "Sydney",        "lat": -33.9,"lon": 151.2},
}

# Fallback static intensities (gCO2eq/kWh) when API unavailable
STATIC_FALLBACK = {
    "US-MIDA-PJM": 370, "US-NW-PACW": 120, "IE": 280,
    "DE": 350, "SG": 470, "JP-TK": 500, "AU-NSW": 610,
}

REFRESH_INTERVAL = 600  # seconds (10 min) — respects free-tier limits


class CarbonCollector:
    def __init__(self, state: dict):
        self.state = state
        self.token = os.getenv("ELECTRICITY_MAPS_TOKEN", "")
        self.base_url = "https://api.electricitymap.org/v3"

    async def fetch_zone(self, client: httpx.AsyncClient, zone_id: str) -> dict:
        """Fetch carbon intensity for a single zone."""
        url = f"{self.base_url}/carbon-intensity/latest?zone={zone_id}"
        headers = {"auth-token": self.token} if self.token else {}
        try:
            r = await client.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                return {
                    "gco2_kwh":      data.get("carbonIntensity"),
                    "fossil_pct":    data.get("fossilFuelPercentage"),
                    "renewable_pct": 100 - (data.get("fossilFuelPercentage") or 0),
                    "source":        "live",
                }
        except Exception as e:
            logger.warning(f"Carbon API error for {zone_id}: {e}")
        # Fallback
        return {
            "gco2_kwh":      STATIC_FALLBACK.get(zone_id, 400),
            "fossil_pct":    None,
            "renewable_pct": None,
            "source":        "static_fallback",
        }

    async def collect(self):
        result = {}
        async with httpx.AsyncClient() as client:
            tasks = {
                dc_id: self.fetch_zone(client, meta["zone"])
                for dc_id, meta in DC_ZONES.items()
            }
            fetched = await asyncio.gather(*tasks.values())
            for dc_id, data in zip(tasks.keys(), fetched):
                result[dc_id] = {**DC_ZONES[dc_id], **data}

        # Compute global weighted average (weight by estimated traffic share)
        traffic_weights = {
            "us-east-nova": 0.35, "us-west-oregon": 0.15, "eu-ireland": 0.12,
            "eu-frankfurt": 0.10, "ap-singapore": 0.12, "ap-tokyo": 0.10, "ap-sydney": 0.06,
        }
        weighted_avg = sum(
            result[dc]["gco2_kwh"] * traffic_weights.get(dc, 0.1)
            for dc in result
            if result[dc].get("gco2_kwh")
        )
        result["_global_avg_gco2_kwh"] = round(weighted_avg, 1)
        result["_timestamp"] = datetime.now(timezone.utc).isoformat()

        self.state["carbon"] = result
        logger.info(f"✅ Carbon: global avg {weighted_avg:.1f} gCO2/kWh")

    async def run(self):
        while True:
            try:
                await self.collect()
            except Exception as e:
                logger.error(f"CarbonCollector error: {e}")
            await asyncio.sleep(REFRESH_INTERVAL)
