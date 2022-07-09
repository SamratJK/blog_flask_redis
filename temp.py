import redis

r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
# r.set("username","password")
# print(r.exists("username"))
# print(r.get("username"))
r.hmset("tem",{"a":"b","c":"d"})
print(r.hget("tem","a"))