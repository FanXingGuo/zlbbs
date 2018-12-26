import memcache

cache=memcache.Client(["127.0.0.1:11211"],debug=True)

def set(key,value,timeout=120):
    return cache.set(key,value,timeout)
def get(key):
    return cache.get(key)
def delete(key):
    return cache.delete(key)

if __name__ == '__main__':
    set("1","A")
    print(get("1"))