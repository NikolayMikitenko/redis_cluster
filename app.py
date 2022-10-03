import argparse
import redis
import time
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--id", help = "App ID. Mandatory (int).")
parser.add_argument("-k", "--key", help = "Key for get it value. Default: value = 'foo'")
parser.add_argument("-t", "--ttl", help = "TTL seconds. Default: value = 60.")
parser.add_argument("-s", "--sleep", help = "Sleep timeout for show refresh cache. Default: value = 5.")
args = parser.parse_args()
id = int(args.id) if args.id else None
if id is None:
    raise Exception("Please set mandatory argument --id. For more details see 'python app.py --help'")
key = args.key if args.key else 'foo'
ttl = int(args.ttl) if args.ttl else 60
sleep = float(args.sleep) if args.sleep else 5.0

ttl_refresh_cache = 0.1 * ttl
ttl_refresh_decision = ttl_refresh_cache / 2

r = redis.Redis(host='localhost', port=6379)

while True:
    ttl_last = r.ttl(name=key)
    print(f"ID: {id}. TTL last: {ttl_last} seconds")
    if ttl_last > ttl_refresh_cache:
        print(f"ID: {id}. Used cache.")
        print(f"ID: {id}. Value: '{r.get(name=key)}'")
    elif ttl_last < 0:
        print(f"ID: {id}. Key '{key}' missed in cache.")
        print(f"ID: {id}. Get value from source.")
        value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        print(f"ID: {id}. Value: '{value}'")
        r.set(name=key, value=value, ex=ttl)
    else:
        p = (random.randrange((ttl_refresh_cache - ttl_last)*100, ttl_refresh_cache*100, 1) / 100)   
        print(f"ID: {id}. Probability: {p}. Decision: value > {ttl_refresh_decision}.")
        #if (random.randrange((ttl_refresh_cache - ttl_last)*100, ttl_refresh_cache*100, 1) / 100) >= ttl_refresh_decision:        
        if p >= ttl_refresh_decision:        
            print(f"ID: {id}. Used probabilistic cache.")
            print(f"ID: {id}. Get value from source.")
            value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            print(f"ID: {id}. Value: '{value}'")
            r.set(name=key, value=value, ex=ttl)
        else:
            print(f"ID: {id}. Used cache.")
            print(f"ID: {id}. Value: '{r.get(name=key)}'")
    print('****************************************')
    time.sleep(sleep)