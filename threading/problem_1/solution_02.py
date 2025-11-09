import threading
import time

counter = 0
result = 0


def work():
    global counter
    global result

    counter += 1
    next_sum = result + counter
    print(f"{result} + {counter} = {next_sum}")
    print("-" * 20)
    result = next_sum


if __name__ == "__main__":
    N = 10
    print("Starting work...")
    start_time = time.time()
    print(time.ctime())
    threads = []
    for i in range(N):
        thread = threading.Thread(target=work)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Work finished.")
    print(f"Final result: {result}")
    print(time.ctime())
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
