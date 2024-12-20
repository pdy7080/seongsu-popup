# backend/utils/cache.py
from functools import lru_cache
from datetime import datetime, timedelta

class Cache:
    def __init__(self, ttl_seconds=3600):
        self.cache = {}
        self.ttl = timedelta(seconds=ttl_seconds)

    def get(self, key):
        if key in self.cache:
            item = self.cache[key]
            if datetime.now() - item['timestamp'] < self.ttl:
                return item['value']
            del self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = {
            'value': value,
            'timestamp': datetime.now()
        }

cache = Cache()

# 데코레이터로 사용
def cached(ttl_seconds=3600):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator