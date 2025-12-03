"""
Redis Setup and Testing
"""
import redis
from django.core.cache import cache
from django_redis import get_redis_connection

print("=== Redis Connection Test ===")

try:
    # Redis connection olish
    redis_conn = get_redis_connection("default")
    
    # Ping test
    redis_conn.ping()
    print("✅ Redis serveriga ulanish muvaffaqiyatli")
    
    # Redis info
    info = redis_conn.info()
    print(f"\n📊 Redis Info:")
    print(f"  - Version: {info.get('redis_version')}")
    print(f"  - Used Memory: {info.get('used_memory_human')}")
    print(f"  - Connected Clients: {info.get('connected_clients')}")
    print(f"  - Total Keys: {redis_conn.dbsize()}")
    
except redis.ConnectionError:
    print("❌ Redis serveriga ulanib bo'lmadi!")
    print("Redis serverni ishga tushiring:")
    print("  - Linux/Mac: redis-server")
    print("  - Windows WSL: wsl redis-server")
    print("  - Docker: docker run -d -p 6379:6379 redis:alpine")


# === REDIS OPERATIONS ===
print("\n=== Redis Operations ===")

# String operations
cache.set('redis_test', 'Hello Redis!', timeout=60)
value = cache.get('redis_test')
print(f"String: {value}")

# Hash operations
redis_conn.hset('user:1000', mapping={
    'name': 'Ali',
    'email': 'ali@example.com',
    'age': 25
})
user = redis_conn.hgetall('user:1000')
print(f"Hash: {user}")

# List operations
redis_conn.rpush('tasks', 'Task 1', 'Task 2', 'Task 3')
tasks = redis_conn.lrange('tasks', 0, -1)
print(f"List: {tasks}")

# Set operations
redis_conn.sadd('tags', 'python', 'django', 'redis')
tags = redis_conn.smembers('tags')
print(f"Set: {tags}")

# Sorted Set operations
redis_conn.zadd('leaderboard', {'user1': 100, 'user2': 200, 'user3': 150})
top_users = redis_conn.zrevrange('leaderboard', 0, 2, withscores=True)
print(f"Sorted Set: {top_users}")


# === KEY PATTERNS ===
print("\n=== Key Patterns ===")

# Wildcard search
redis_conn.set('app:user:1', 'User 1')
redis_conn.set('app:user:2', 'User 2')
redis_conn.set('app:post:1', 'Post 1')

user_keys = redis_conn.keys('app:user:*')
print(f"User keys: {user_keys}")


# === TTL MANAGEMENT ===
print("\n=== TTL Management ===")

# Key yaratish
redis_conn.set('temp', 'Temporary data')
redis_conn.expire('temp', 10)  # 10 soniya

ttl = redis_conn.ttl('temp')
print(f"TTL: {ttl} soniya")


# === TRANSACTIONS ===
print("\n=== Redis Transactions ===")

pipe = redis_conn.pipeline()
pipe.set('key1', 'value1')
pipe.set('key2', 'value2')
pipe.incr('counter')
results = pipe.execute()
print(f"Transaction results: {results}")


# === PUB/SUB (Publish/Subscribe) ===
print("\n=== Pub/Sub Example ===")

# Publisher
redis_conn.publish('notifications', 'New message!')
print("Message published to 'notifications' channel")


print("\n✅ Redis setup va operatsiyalar muvaffaqiyatli!")