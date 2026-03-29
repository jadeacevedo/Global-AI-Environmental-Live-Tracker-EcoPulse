"""
Google Trends Collector
Uses pytrends (unofficial Google Trends API) to track AI-related search
velocity as a proxy for real-time usage intent/volume.

pytrends: https://github.com/GeneralMills/pytrends
Install: pip install pytrends

Keywords tracked in 5 batches (pytrends limit = 5 per request):
  Batch A: ChatGPT, Claude AI, Gemini AI, AI chatbot, Copilot
  Batch B: image generation, AI video, Midjourney, Sora, Stable Diffusion

Refresh: every 20 minutes (Google Trends has rate limits).
"""

import asyncio
import logging
import os
import time
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

REFRESH_INTERVAL = 1200  # 20 min

KEYWORD_BATCHES = [
    ["ChatGPT", "Claude AI", "Gemini AI", "AI chatbot", "Copilot"],
    ["image generation AI", "Midjourney", "Sora AI", "AI video generator", "Stable Diffusion"],
]

class TrendsCollector:
    def __init__(self, state: dict):
        self.state = state
        self._last_fetch = 0

    def _try_import(self):
        try:
            from pytrends.request import TrendReq
            return TrendReq(hl="en-US", tz=0, timeout=(10, 25))
        except ImportError:
            logger.warning("pytrends not installed — run: pip install pytrends")
            return None

    async def collect(self):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self._sync_collect)
        self.state["trends"] = result

    def _sync_collect(self) -> dict:
        pt = self._try_import()
        if not pt:
            return self._mock_trends()

        all_scores = {}
        for batch in KEYWORD_BATCHES:
            try:
                pt.build_payload(batch, timeframe="now 1-H", geo="")
                df = pt.interest_over_time()
                if not df.empty:
                    latest = df.iloc[-1]
                    for kw in batch:
                        if kw in latest:
                            all_scores[kw] = int(latest[kw])
                time.sleep(3)  # Respect rate limits
            except Exception as e:
                logger.warning(f"Trends batch error: {e}")
                for kw in batch:
                    all_scores[kw] = 50  # neutral fallback

        # Aggregate AI hype index (0–100)
        scores = [v for v in all_scores.values() if v is not None]
        hype_index = round(sum(scores) / len(scores)) if scores else 50

        # Velocity: compare to prior window (stored in state)
        prev_hype = self.state.get("trends", {}).get("hype_index", hype_index)
        velocity  = round(hype_index - prev_hype, 1)

        return {
            "keywords":    all_scores,
            "hype_index":  hype_index,       # 0–100 composite
            "velocity":    velocity,          # change from last window
            "trending_up": velocity > 5,
            "_timestamp":  datetime.now(timezone.utc).isoformat(),
        }

    def _mock_trends(self) -> dict:
        """Realistic fallback when pytrends unavailable."""
        import random, math
        hour = datetime.now(timezone.utc).hour
        base = 55 + 15 * math.sin(math.pi * (hour - 6) / 14)
        return {
            "keywords": {
                "ChatGPT": int(base + random.gauss(0, 5)),
                "Claude AI": int(base * 0.7 + random.gauss(0, 4)),
                "Gemini AI": int(base * 0.8 + random.gauss(0, 4)),
                "AI chatbot": int(base * 0.9 + random.gauss(0, 5)),
                "Midjourney": int(base * 0.5 + random.gauss(0, 3)),
            },
            "hype_index":  int(base),
            "velocity":    round(random.gauss(0, 3), 1),
            "trending_up": random.random() > 0.5,
            "_mock":       True,
            "_timestamp":  datetime.now(timezone.utc).isoformat(),
        }

    async def run(self):
        while True:
            try:
                await self.collect()
                logger.info(f"✅ Trends: hype_index={self.state['trends'].get('hype_index')}")
            except Exception as e:
                logger.error(f"TrendsCollector error: {e}")
            await asyncio.sleep(REFRESH_INTERVAL)
