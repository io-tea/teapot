import asyncio


class PeriodicTask:
    def __init__(self, func, interval):
        self.func = func
        self.interval = interval
        self._loop = asyncio.get_event_loop()
        self._set()

    def _set(self):
        self._handler = self._loop.call_later(self.interval, self._run)

    def _run(self):
        self.func()
        self._set()
