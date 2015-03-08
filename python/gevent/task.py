import gevent
import random
import time


def task(pid):
    gevent.sleep(random.randint(0, 2) * 0.01)
    print ('Task %s done' % pid)
    

def synchronous():
    for i in range(1, 10):
        task(i)
        
        
def asynchronous():
    threads = [gevent.spawn(task, i) for i in xrange(10)]
    gevent.joinall(threads)
    
print('Synchronous:')
t = time.time()
synchronous()
print time.time() - t

t = time.time()
print ('Asynchronous:')
asynchronous()
print time.time() - t


