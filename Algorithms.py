# region Bubble sort
#                      Best           Average          Worst
# Time complexity:     O(n)           O(n^2)          O(n^2)
# Space complexity (worst): O(1)


def bubble_sort(Event, arr):
    for i in range(len(arr) - 1, 0, -1):
        for j in range(i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

            # Event.emit('output', j + 1)

            Event.emit('output', j + 1)


# endregion
# region Insertion sort
#                      Best           Average          Worst
# Time complexity:     O(n)           O(n^2)          O(n^2)
# Space complexity (worst): O(1)


def insertion_sort(Event, arr):
    for i in range(1, len(arr)):
        Event.emit('output', i)
        j = i - 1
        next_item = arr[i]

        while (arr[j] > next_item) and (j >= 0):
            arr[j + 1] = arr[j]
            Event.emit('output', j)
            j -= 1

        arr[j + 1] = next_item


# endregion
# region Selection sort
#                      Best           Average          Worst
# Time complexity:    O(n^2)          O(n^2)          O(n^2)
# Space complexity (worst): O(1)


def selection_sort(Event, arr):
    for i in range(len(arr)):

        min_i = i
        for j in range(i + 1, len(arr)):
            if arr[min_i] > arr[j]:
                min_i = j

            Event.emit('output', j)

        arr[i], arr[min_i] = arr[min_i], arr[i]


# endregion
# region Merge sort
#                      Best           Average          Worst
# Time complexity:  O(n log(n))     O(n log(n))     O(n log(n))
# Space complexity (worst): O(n)


def merge_sort_wrapper(Event, arr):
    merge_sort(Event, arr, 0, len(arr))


def merge_sort(Event, arr, l, r):
    if r - l > 1:
        mid = (l + r) // 2
        merge_sort(Event, arr, l, mid)
        merge_sort(Event, arr, mid, r)
        merge(Event, arr, l, mid, r)


def merge(Event, arr, l, m, r):
    left = arr[l:m]
    right = arr[m:r]
    i = 0
    j = 0
    for k in range(l, r):
        if j >= len(right) or (i < len(left) and left[i] < right[j]):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1

        Event.emit('output', k)


# endregion
# region Quick sort
# Time complexity:  O(n log(n))     O(n log(n))     O(n^2)
# Space complexity (worst): O(log(n))

def quick_sort_wrapper(Event, arr):
    quick_sort(Event, arr, 0, len(arr) - 1)


def quick_sort(Event, arr, low, high):
    if low < high:
        pi = partition(Event, arr, low, high)

        quick_sort(Event, arr, low, pi - 1)
        quick_sort(Event, arr, pi + 1, high)


def partition(Event, arr, low, high):
    i = (low - 1)
    pivot = arr[high]

    for j in range(low, high):

        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

            Event.emit('output', j)

    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1

# endregion
