import redis

from config import REDIS

store = redis.StrictRedis(host=REDIS['HOST'], port=REDIS['PORT'], db=REDIS['DB'])
