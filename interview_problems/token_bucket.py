import threading
import time


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = capacity
        self.last_refill_timestamp = time.monotonic()
        self.lock = threading.Lock()

    def _refill(self, current_timestamp: float):
        elapsed = current_timestamp - self.last_refill_timestamp
        if elapsed <= 0:
            return
        added_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + added_tokens)
        self.last_refill_timestamp = current_timestamp

    def consume(self, tokens: int, current_timestamp: float) -> bool:
        with self.lock:
            self._refill(current_timestamp)
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def get_tokens(self, current_timestamp: float) -> float:
        with self.lock:
            self._refill(current_timestamp)
            return self.tokens


def consumer(bucket: TokenBucket, tokens: int, interval: float, name: str):
    """Continuously tries to consume tokens every 'interval' seconds."""
    while True:
        allowed = bucket.consume(tokens, time.monotonic())
        status = "✅ Allowed" if allowed else "❌ Blocked"
        print(f"{time.strftime('%X')} | {name} | Request {tokens} tokens | {status}")
        time.sleep(interval)


def monitor(bucket: TokenBucket):
    """Prints available tokens every second."""
    while True:
        now = time.monotonic()
        print(f"🪣 Tokens available: {bucket.get_tokens(now)}")
        time.sleep(1)


if __name__ == "__main__":
    bucket = TokenBucket(capacity=10, refill_rate=2)  # max 10, +2 tokens/sec

    # Start a monitor thread
    threading.Thread(target=monitor, args=(bucket,), daemon=True).start()

    # Start two consumers
    threading.Thread(
        target=consumer, args=(bucket, 3, 1.5, "Alice"), daemon=True
    ).start()
    threading.Thread(target=consumer, args=(bucket, 5, 2, "Bob"), daemon=True).start()

    # Keep main alive
    while True:
        time.sleep(0.5)
