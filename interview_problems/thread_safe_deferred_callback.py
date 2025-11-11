import threading


class DeferredCallbackExecutor:

    def __init__(self):
        self._callbacks = list()
        self._condition = threading.Condition()

    def add_callback(self, callback):
        with self._condition:
            self._callbacks.append(callback)
            self._condition.notify()

    def run(self):
        while True:
            with self._condition:
                while not self._callbacks:
                    self._condition.wait()

                callback = self._callbacks.pop(0)
                callback()
