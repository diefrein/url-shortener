from functools import wraps
import pickle, redis, os, logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=0,
    decode_responses=False
)

def clear_cache_for_function(func, *args, **kwargs):
    cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
    redis_client.delete(cache_key)
    
def cache_query(ttl=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"sql_cache:{func.__name__}:{str(args[1:])}:{str(kwargs)}"
            
            cached_data = redis_client.get(cache_key)
            if cached_data:
                log.info(f"Getting data from cache, cache_key = {cache_key}")
                return pickle.loads(cached_data)
            
            result = func(*args, **kwargs)
            
            log.info(f"Сaching data, cache_key = {cache_key}")
            redis_client.setex(cache_key, ttl, pickle.dumps(result))
            return result
        return wrapper
    return decorator