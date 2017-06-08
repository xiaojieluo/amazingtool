import cProfile
import os
import pstats
import redis

class Cache(object):
    '''
    使用 Redis 作为缓存
    '''
    def __init__(self, host='localhost', port=6379, db=0):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.r = redis.Redis(connection_pool=self.pool)

if __name__ == '__main__':
    cache = Cache()
    print(cache.r.set('key', 'k'))
    
def do_cprofile(filename):
    '''
    decorator for function calling
    '''
    def wrapper(func):
        def profiled_func(*args, **kw):
            #Flag for do profiling or not.
            # DO_PROF = os.gevent('PROFILING')
            DO_PROF = True
            if DO_PROF:
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kw)
                profile.disable()
                sortBy = 'tottime'
                ps = pstats.Stats(profile).sort_stats(sortBy)
                ps.dump_stats(filename)
            else:
                result = func(*args, **kw)
            return result
        return profiled_func
    return wrapper
