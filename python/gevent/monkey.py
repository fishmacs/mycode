import select
import gevent

from gevent import monkey
monkey.patch_select


while True:
    select.select([], [], [], 0)
    gevent.sleep(0.1)
    