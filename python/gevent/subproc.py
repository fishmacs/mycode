import gevent
from gevent.subprocess import Popen, PIPE
from gevent import subprocess


def call(*cmd):
    p = Popen(cmd, stdout=PIPE, shell=True)
    out, err = p.communicate()
    print '....', cmd, out.rstrip(), err


def call1(cmd):
    subprocess.call([cmd])
    
        
def cron():
    while True:
        print 'cron'
        gevent.sleep(0.2)
        
#call('whoami', 'sleep 1', 'whoami')
call1('sleep 5')        
g = gevent.spawn(cron)
#call('ls', 'whoami')
call1('sleep 5')
g.kill()
