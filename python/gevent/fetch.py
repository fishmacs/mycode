import gevent.monkey
gevent.monkey.patch_socket()

import gevent
import urllib2
import json
import time


def fetch(pid):
    response = urllib2.urlopen('http://json-time.appspot.com/time.json')
    result = response.read()
    json_result = json.loads(result)
    dt = json_result['datetime']

    print('Process %s: %s' % (pid, dt))
    return dt


def synchronous():
    for i in range(1, 10):
        fetch(i)
        
        
def asynchronous():
    threads = [gevent.spawn(fetch, i) for i in xrange(10)]
    gevent.joinall(threads)
    
    
print('Synchrous:')
t = time.time()
synchronous()
print time.time() - t

print('Asynchronous')
t = time.time()
asynchronous()
print time.time() - t
