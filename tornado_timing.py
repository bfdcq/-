import datetime
import time
from tornado import ioloop


def start(func, hour, immediate=False):
    def timing():
        now = datetime.datetime.now()
        start_time = datetime.datetime(now.year, now.month, now.day, hour)
        if now > start_time:
            t = (start_time + datetime.timedelta(1) - now).seconds
        else:
            t = (start_time - now).seconds
        t += time.time()
        print('start at %s next time' % str(datetime.datetime.fromtimestamp(t)))
        ioloop.IOLoop.current().add_timeout(t, func)

    if immediate:
        func()
    timing()
    ioloop.IOLoop.current().start()


def p(s):
    print(s)


if __name__ == '__main__':
    from functools import partial

    func = partial(p, '111')
    start(func, 2, True)
