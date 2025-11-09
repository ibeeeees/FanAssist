"""
Cache Warmer Service - Pre-fetch and cache player data on startup
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from app.services.popular_players import popular_players_service

logger = logging.getLogger(__name__)


class CacheWarmer:
    """Service to pre-fetch and cache player data"""
    
    def __init__(self):
        self.cache: Dict[str, Dict] = {}
        self.cache_ttl = 300  # 5 minutes in seconds
        self.last_fetch_time: Dict[str, datetime] = {}
        self.warmup_complete = False
        
    def is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.last_fetch_time:
            return False
        
        elapsed = (datetime.now() - self.last_fetch_time[key]).total_seconds()
        return elapsed < self.cache_ttl
    
    async def get_today_players(self) -> List[Dict]:
        """Get today's players (from cache if valid, otherwise fetch)"""
        cache_key = "today"
        
        if self.is_cache_valid(cache_key) and cache_key in self.cache:
            logger.info("📦 Returning cached data for today's players")
            return self.cache[cache_key]
        
        logger.info("🔄 Fetching fresh data for today's players...")
        players = await popular_players_service.get_popular_players_for_today()
        
        self.cache[cache_key] = players
        self.last_fetch_time[cache_key] = datetime.now()
        
        logger.info(f"✅ Cached {len(players)} players for today")
        return players
    
    async def get_tomorrow_players(self) -> List[Dict]:
        """Get tomorrow's players (from cache if valid, otherwise fetch)"""
        cache_key = "tomorrow"
        
        if self.is_cache_valid(cache_key) and cache_key in self.cache:
            logger.info("📦 Returning cached data for tomorrow's players")
            return self.cache[cache_key]
        
        logger.info("🔄 Fetching fresh data for tomorrow's players...")
        players = await popular_players_service.get_popular_players_for_tomorrow()
        
        self.cache[cache_key] = players
        self.last_fetch_time[cache_key] = datetime.now()
        
        logger.info(f"✅ Cached {len(players)} players for tomorrow")
        return players
    
    async def warmup_cache(self):
        """Pre-fetch today's and tomorrow's players on server startup"""
        logger.info("🔥 Starting cache warmup...")
        
        try:
            # Fetch both today and tomorrow in parallel
            today_task = asyncio.create_task(self.get_today_players())
            tomorrow_task = asyncio.create_task(self.get_tomorrow_players())
            
            today_players, tomorrow_players = await asyncio.gather(
                today_task,
                tomorrow_task,
                return_exceptions=True
            )
            
            # Check for errors
            if isinstance(today_players, Exception):
                logger.error(f"❌ Failed to fetch today's players: {today_players}")
            else:
                logger.info(f"✅ Warmed up cache with {len(today_players)} players for today")
            
            if isinstance(tomorrow_players, Exception):
                logger.error(f"❌ Failed to fetch tomorrow's players: {tomorrow_players}")
            else:
                logger.info(f"✅ Warmed up cache with {len(tomorrow_players)} players for tomorrow")
            
            self.warmup_complete = True
            logger.info("🎉 Cache warmup complete!")
            
        except Exception as e:
            logger.error(f"❌ Cache warmup failed: {e}")
            self.warmup_complete = False
    
    async def refresh_cache_periodically(self, interval_seconds: int = 300):
        """Background task to refresh cache every X seconds"""
        logger.info(f"🔄 Starting periodic cache refresh (every {interval_seconds}s)")
        
        while True:
            try:
                await asyncio.sleep(interval_seconds)
                logger.info("🔄 Refreshing cache...")
                await self.warmup_cache()
            except Exception as e:
                logger.error(f"❌ Periodic cache refresh failed: {e}")
    
    def clear_cache(self):
        """Manually clear the cache"""
        self.cache.clear()
        self.last_fetch_time.clear()
        self.warmup_complete = False
        logger.info("🧹 Cache cleared")
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        stats = {
            "warmup_complete": self.warmup_complete,
            "cache_ttl_seconds": self.cache_ttl,
            "cached_keys": list(self.cache.keys()),
            "cache_ages": {}
        }
        
        for key, last_fetch in self.last_fetch_time.items():
            age_seconds = (datetime.now() - last_fetch).total_seconds()
            stats["cache_ages"][key] = {
                "age_seconds": round(age_seconds, 2),
                "is_valid": age_seconds < self.cache_ttl,
                "players_count": len(self.cache.get(key, []))
            }
        
        return stats


# Global cache warmer instance
cache_warmer = CacheWarmer()
