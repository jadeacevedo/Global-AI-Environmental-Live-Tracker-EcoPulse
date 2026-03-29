"""
Water Stress Collector
Sources:
  1. WRI Aqueduct 4.0 — static annual water stress index (GeoJSON, free)
     https://www.wri.org/data/aqueduct-water-risk-atlas
  2. Real-time scaling: water evaporation per query estimated from
     Google/Microsoft published WUE (Water Usage Effectiveness) metrics.

Key metric: WUE (Water Usage Effectiveness) = liters per kWh of IT load
  - Industry range: 0.5 – 3.1 L/kWh (air-cooled to evaporative cooling)
  - We use regional climate-adjusted estimates.

Refresh: every 30 minutes (water stress is slow-changing).
"""

import asyncio
import logging
import os
from datetime import datetime, timezone

import httpx

logger = logging.getLogger(__name__)

REFRESH_INTERVAL = 1800  # 30 min

# Water Usage Effectiveness (L/kWh IT) — climate-adjusted regional estimates
# Higher in hot, dry climates that rely on evaporative cooling
WUE_BY_REGION = {
    "us-east-nova":   1.8,   # PJM grid, mixed cooling, moderate climate
    "us-west-oregon": 0.9,   # Columbia River hydro-cooling advantage
    "eu-ireland":     1.1,   # Cool climate, efficient air cooling possible
    "eu-frankfurt":   1.4,   # Mixed
    "ap-singapore":   2.6,   # Hot, humid; high cooling load
    "ap-tokyo":       1.9,   # Dense urban heat island
    "ap-sydney":      2.2,   # Dry Australian climate, water stress
}

# WRI Aqueduct baseline water stress (0–5 scale) for each region
# Sourced from: https://www.wri.org/applications/aqueduct/water-risk-atlas/
WATER_STRESS_INDEX = {
    "us-east-nova":   2.1,  # Medium-High (Potomac basin)
    "us-west-oregon": 1.3,  # Medium (Columbia River)
    "eu-ireland":     0.8,  # Low
    "eu-frankfurt":   1.7,  # Medium-High (Rhine pressures)
    "ap-singapore":   4.1,  # Extremely High (island state, no inland water)
    "ap-tokyo":       1.5,  # Medium
    "ap-sydney":      3.2,  # High (Murray-Darling basin stress)
}

STRESS_LABEL = {
    (0, 1): "Low",
    (1, 2): "Medium",
    (2, 3): "Medium-High",
    (3, 4): "High",
    (4, 5.1): "Extremely High",
}

def stress_label(index: float) -> str:
    for (lo, hi), label in STRESS_LABEL.items():
        if lo <= index < hi:
            return label
    return "Unknown"


class WaterStressCollector:
    def __init__(self, state: dict):
        self.state = state

    def liters_per_query(self, region: str, avg_wh_per_query: float = 0.32) -> float:
        """
        Estimate liters of water consumed per average AI query.
        L = WUE (L/kWh) × energy_per_query (kWh)
        """
        wue = WUE_BY_REGION.get(region, 1.8)
        kwh = avg_wh_per_query / 1000
        return round(wue * kwh, 6)

    async def collect(self):
        # Pull current QPM from shared state for live scaling
        qpm  = self.state.get("inference", {}).get("qpm", 22_000)
        # Weighted traffic distribution across regions
        traffic_share = {
            "us-east-nova":   0.35, "us-west-oregon": 0.15, "eu-ireland": 0.12,
            "eu-frankfurt":   0.10, "ap-singapore":   0.12, "ap-tokyo":   0.10,
            "ap-sydney":      0.06,
        }

        result = {}
        total_liters_per_min = 0.0

        for region, share in traffic_share.items():
            regional_qpm   = qpm * share
            l_per_query    = self.liters_per_query(region)
            liters_per_min = regional_qpm * l_per_query
            total_liters_per_min += liters_per_min

            result[region] = {
                "label":              self._region_label(region),
                "wue_l_per_kwh":      WUE_BY_REGION[region],
                "water_stress_index": WATER_STRESS_INDEX[region],
                "stress_label":       stress_label(WATER_STRESS_INDEX[region]),
                "l_per_query":        l_per_query,
                "liters_per_min":     round(liters_per_min, 2),
                "traffic_share":      share,
            }

        # Global aggregates
        result["_total_liters_per_min"]   = round(total_liters_per_min, 1)
        result["_total_liters_per_day"]   = round(total_liters_per_min * 60 * 24)
        result["_olympic_pools_per_day"]  = round(total_liters_per_min * 60 * 24 / 2_500_000, 2)
        result["_timestamp"]              = datetime.now(timezone.utc).isoformat()

        self.state["water"] = result
        logger.info(
            f"✅ Water: {round(total_liters_per_min):,} L/min "
            f"({result['_olympic_pools_per_day']} Olympic pools/day)"
        )

    def _region_label(self, region: str) -> str:
        labels = {
            "us-east-nova": "N. Virginia", "us-west-oregon": "Oregon",
            "eu-ireland": "Ireland", "eu-frankfurt": "Frankfurt",
            "ap-singapore": "Singapore", "ap-tokyo": "Tokyo", "ap-sydney": "Sydney",
        }
        return labels.get(region, region)

    async def run(self):
        await asyncio.sleep(5)  # Let inference estimator run first
        while True:
            try:
                await self.collect()
            except Exception as e:
                logger.error(f"WaterStressCollector error: {e}")
            await asyncio.sleep(REFRESH_INTERVAL)
