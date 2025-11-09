"""
Imagine a scenario where we have two threads working together to find prime numbers and print them. Say the first thread finds the prime number and the second thread is responsible for printing the found prime. The first thread (finder) sets a boolean flag whenever it determines an integer is a prime number. The second (printer) thread needs to know when the finder thread has hit upon a prime number

"""

import threading
import time


exit_flag = False
prime_holder = None
found_prime = False


def printer_work():
    global found_prime
    global prime_holder

    while not exit_flag:

        if found_prime:
            print(f"Printer thread: Found prime {prime_holder}")
            found_prime = False
            prime_holder = None
        time.sleep(0.1)


def is_prime(n):
    if n <= 1:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def finder_work():
    i = 1

    global prime_holder
    global found_prime

    while not exit_flag:
        while not is_prime(i):
            i += 1
        prime_holder = i
        found_prime = True

        while found_prime and not exit_flag:
            time.sleep(0.1)
        i += 1


if __name__ == "__main__":
    finder_thread = threading.Thread(target=finder_work)
    printer_worker_thread = threading.Thread(target=printer_work)
    finder_thread.start()
    printer_worker_thread.start()

    time.sleep(5)
    exit_flag = True
    finder_thread.join()
    printer_worker_thread.join()
