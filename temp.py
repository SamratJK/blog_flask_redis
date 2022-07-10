import redis

r = redis.StrictRedis(
    "localhost", 6379, charset="utf-8", decode_responses=True
)

r.hmset("tem", {"a": "b", "c": "d"})
print(r.hget("tem", "a"))
