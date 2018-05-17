import threading
import time
import heapq
import datetime
import logging

logger = logging.getLogger(__name__)


class _Timeout(object):
    def __init__(self, deadline, callback):
        self.deadline = deadline
        self.callback = callback

    def __lt__(self, other):
        return self.deadline < other.deadline

    def __le__(self, other):
        return self.deadline <= other.deadline


class Timing(object):
    _instance = None

    def __init__(self):
        self.max_sleep_time = 30
        self.task_heap = []
        self.callbacks = []
        self.todo_list = []

    @staticmethod
    def instance():
        if Timing._instance is None:
            Timing._instance = Timing()
        return Timing._instance

    def add_task(self, func, runtime):
        task = _Timeout(runtime, func)
        heapq.heappush(self.task_heap, task)

    def _run(self):
        while True:
            now = time.time()
            while self.task_heap:
                if self.task_heap[0].callback is None:
                    # 没有回调函数 清除这个task
                    heapq.heappop(self.task_heap)
                elif self.task_heap[0].deadline <= now:
                    self.todo_list.append(heapq.heappop(self.task_heap))
                else:
                    break

            # 重建堆
            self.task_heap = [x for x in self.task_heap if x.callback is not None]
            heapq.heapify(self.task_heap)

            # 执行 func
            while self.todo_list:
                todo = self.todo_list.pop()
                todo.callback()

            sleep_time = max(0, min(self.task_heap[0].deadline - time.time(), self.max_sleep_time))
            time.sleep(sleep_time)

    def start(self):
        t = threading.Thread(target=self._run)
        t.start()


def add_timing_task(func, interval=0, hour=0, minute=0, immediate=False):
    timing = Timing.instance()
    if immediate:
        timing.todo_list.append(_Timeout(0, func))

    def _run():
        if interval:
            t = time.time()
            next_time = t + interval
            timing.add_task(_loop, next_time)
            logger.info('function %s start at %s next time' % (func, str(datetime.datetime.fromtimestamp(next_time))))
        else:
            now = datetime.datetime.now()
            start_time = datetime.datetime(now.year, now.month, now.day, hour, minute)
            if now > start_time:
                t = (start_time + datetime.timedelta(1) - now).total_seconds()
            else:
                t = (start_time - now).total_seconds()

            t += time.time()
            logger.info('function %s start at %s next time' % (func, str(datetime.datetime.fromtimestamp(t))))
            timing.add_task(_loop, t)

    def _loop():
        func()
        _run()

    _run()


if __name__ == "__main__":
    from functools import partial


    def p(x):
        print(x)


    t = Timing.instance()
    f1 = partial(p, 'pppppppppppppppppppppppppppp')
    f2 = partial(p, 'qqqqqqqqqqqqqqqqqqqqqqqqqqqq')
    add_timing_task(f1, hour=15, minute=3)
    add_timing_task(f2, 2)
    t.start()
