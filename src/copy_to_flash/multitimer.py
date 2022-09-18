import logging
import random
import string
from threading import Lock, Timer


def _gen_id(size: int):
    if size < 1:
        raise ValueError('incorrect size {}. Must be > 0'.format(size))

    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(size))


class Multitimer(object):
    def __init__(self, interval, f, *args, **kvargs) -> None:
        id = "{}:{}".format(__name__, _gen_id(12))
        self.__logger = logging.getLogger(id)
        self.__interval = interval
        self.__args = args
        self.__kvargs = kvargs
        self._fn = f
        self.__timer_lock = Lock()
        self.__stopped = False

    def start(self, run_imminently=False):
        if run_imminently:
            self.__logger.debug('Run function imminently before run timer')
            self.__run()

        self.__start_new_timer()

    def stop(self):
        self.__timer_lock.acquire()
        
        self.__stopped = True
        if self.__timer:
            if not self.__timer.is_alive():
                self.__timer.cancel()
                self.__logger.debug('Current timer have cancelled')
            else:
                self.__logger.debug('Timer is running. Waiting for finish...')

        self.__timer_lock.release()
    
    def __run(self):
        self.__logger.debug('Start timer function')
        self._fn(*self.__args, **self.__kvargs)
        self.__logger.debug('Timer function finnished')

    def __start_new_timer(self):
        self.__timer_lock.acquire()

        if self.__stopped:
            self.__logger.debug('Timer was stopped fully. Next run was not scheduled')
            return

        def run():
            self.__run()
            self.__start_new_timer()

        self.__timer = Timer(self.__interval, run)
        self.__timer.start()
        self.__logger.debug('Start new timer')

        self.__timer_lock.release()

    
