"""
Utilities.
"""

import time

# from: http://www.andreas-jung.com/contents/a-python-decorator-for-measuring-the-execution-time-of-methods
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%2.2f sec, %s' % (te-ts, method.__name__)
        return result

    return timed
