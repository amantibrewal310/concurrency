import threading
import time
import random


class UberRide:
    def __init__(self):
        self.democrats = 0
        self.republicans = 0

        self.lock = threading.Lock()
        self.democrat_queue = threading.Semaphore(0)
        self.republican_queue = threading.Semaphore(0)

        self.barrier = threading.Barrier(4)

    def seated(self, name):
        print(f"{name} is seated.")

    def drive(self):
        print("🚗 Ride started!\n")

    def democrat(self):
        self._arrive("Democrat")

    def republican(self):
        self._arrive("Republican")

    def _arrive(self, party):
        with self.lock:
            if party == "Democrat":
                self.democrats += 1
            else:
                self.republicans += 1

            if self.democrats >= 4:
                for _ in range(4):
                    self.democrat_queue.release()
                self.democrats -= 4
            elif self.republicans >= 4:
                for _ in range(4):
                    self.republican_queue.release()
                self.republicans -= 4
            elif self.democrats >= 2 and self.republicans >= 2:
                for _ in range(2):
                    self.democrat_queue.release()
                    self.republican_queue.release()
                self.democrats -= 2
                self.republicans -= 2
            else:
                pass

        # wait for your turn
        if party == "Democrat":
            self.democrat_queue.acquire()
        else:
            self.republican_queue.acquire()

        # seat the passenger
        self.seated(party)

        # wait for all 4 to board
        member_id = self.barrier.wait()

        # one of the 4 threads starts the ride
        if member_id == 0:
            self.drive()


def test_uber_ride():
    uber = UberRide()
    threads = []

    for i in range(20):
        if random.choice(["D", "R"]) == "D":
            t = threading.Thread(target=uber.democrat)
        else:
            t = threading.Thread(target=uber.republican)
        threads.append(t)
        t.start()
        time.sleep(random.uniform(0.05, 0.2))

    for t in threads:
        t.join()


if __name__ == "__main__":
    test_uber_ride()
