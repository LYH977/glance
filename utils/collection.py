import os
import redis

temp = None
data={}

visual_container = []

img_container = {}

results = {}

live_processing = {}

redis_instance = redis.StrictRedis.from_url(os.environ['REDIS_URL'])

# last_create_click = 1

# last_vtype = ''