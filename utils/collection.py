import os
import redis

# visual_container = []
# results = {}

temp = None
new_col = {'expression': [], 'numeric_col': []}
data={}
img_container = {}
live_processing = {}
redis_instance = redis.StrictRedis.from_url(os.environ['REDIS_URL'])
# redis_instance = redis.StrictRedis.from_url('redis://localhost:6379')
