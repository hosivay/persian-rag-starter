import hashlib
import json
import os
import time

CACHE_FILE = os.getenv("CACHE_FILE", "cache.json")
RATE_LIMIT_COOLDOWN = int(os.getenv("RATE_LIMIT_COOLDOWN", "5"))
RATE_LIMIT: dict[str, float] = {}


def get_cache_key(prompt: str) -> str:
    return hashlib.md5(prompt.encode()).hexdigest()


def load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache: dict):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)


def get_cached(prompt: str) -> str | None:
    cache = load_cache()
    key = get_cache_key(prompt)
    return cache.get(key)


def set_cached(prompt: str, result: str):
    cache = load_cache()
    key = get_cache_key(prompt)
    cache[key] = result
    save_cache(cache)


def check_rate_limit(user_id: str) -> bool:
    now = time.time()
    if user_id in RATE_LIMIT:
        if now - RATE_LIMIT[user_id] < RATE_LIMIT_COOLDOWN:
            return False
    RATE_LIMIT[user_id] = now
    return True
