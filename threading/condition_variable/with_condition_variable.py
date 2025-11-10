import threading
from threading import Condition
import time

condition = Condition()
found_prime = False
prime_holder = None

exit_flag = False


def is_prime(n):
    if n <= 1:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def print_work():
    global found_prime, prime_holder
    while not exit_flag:
        with condition:
            while not found_prime and not exit_flag:
                condition.wait()
            print(f"First prime number found: {prime_holder}")

            prime_holder = None
            found_prime = False
            condition.notify()


def find_prime():
    global found_prime, prime_holder
    i = 2
    while not exit_flag:
        while not is_prime(i):
            i += 1

        with condition:
            prime_holder = i
            found_prime = True
            condition.notify()

        with condition:
            while found_prime and not exit_flag:
                condition.wait()
            i += 1


if __name__ == "__main__":
    printer_thread = threading.Thread(target=print_work)
    finder_thread = threading.Thread(target=find_prime)

    printer_thread.start()
    finder_thread.start()

    condition.acquire()
    time.sleep(5)
    exit_flag = True
    condition.notify_all()
    condition.release()
    printer_thread.join()
    finder_thread.join()
