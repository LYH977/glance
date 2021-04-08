import os
import redis

temp = None

new_col = {'expression': [], 'numeric_col': []}

data={}

visual_container = []

img_container = {}

results = {}

live_processing = {}

redis_instance = redis.StrictRedis.from_url(os.environ['REDIS_URL'])
# redis_instance = redis.StrictRedis.from_url('redis://localhost:6379')


# last_create_click = 1

# last_vtype = ''