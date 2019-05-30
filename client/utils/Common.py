import functools

def once(method):
    """Make method once.

    It doesn't return result. 
    """
    @functools.wraps(method)
    def inner(*args, **kw):
        if not inner.called:
            method(*args, **kw)
            inner.called = True
        inner.called = False
        return inner

def time_cache(method):
    
    pass

