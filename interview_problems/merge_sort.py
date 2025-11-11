import concurrent.futures


def merge(arr, start, mid, end):
    i, j = start, mid + 1
    temp = []

    # Merge both halves
    while i <= mid and j <= end:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1

    while i <= mid:
        temp.append(arr[i])
        i += 1

    while j <= end:
        temp.append(arr[j])
        j += 1

    arr[start : end + 1] = temp


def merge_sort(arr, start, end, executor=None, depth=0, max_depth=3):
    """Parallel merge sort with thread pool.

    Args:
        arr: List to be sorted.
        start, end: Boundaries of current segment.
        executor: ThreadPoolExecutor (shared across recursion).
        depth: Current recursion depth.
        max_depth: Depth threshold to prevent too many threads.
    """
    if start >= end:
        return

    mid = (start + end) // 2

    # Only parallelize up to limited depth to avoid thread explosion
    if executor and depth < max_depth:
        left_future = executor.submit(
            merge_sort, arr, start, mid, executor, depth + 1, max_depth
        )
        right_future = executor.submit(
            merge_sort, arr, mid + 1, end, executor, depth + 1, max_depth
        )
        left_future.result()
        right_future.result()
    else:
        merge_sort(arr, start, mid, executor, depth + 1, max_depth)
        merge_sort(arr, mid + 1, end, executor, depth + 1, max_depth)

    merge(arr, start, mid, end)


if __name__ == "__main__":
    import random

    arr = [random.randint(0, 1000) for _ in range(120)]

    print("Before:", arr)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        merge_sort(arr, 0, len(arr) - 1, executor)
    print("After: ", arr)
