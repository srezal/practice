import time

import numpy as np

N = 10**4
M = 10**5
T1 = np.ones(M, dtype=int)


def calc_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"Время расчета {func.__name__}: {round(time.time() - start_time, 2)}s")
        return result

    return wrapper


@calc_time_decorator
def calc_base_2(t1, n):
    for _ in range(n):
        r = t1 + t1  # noqa


@calc_time_decorator
def calc_base_3(t1, n):
    for _ in range(n):
        r = t1 + t1 + t1  # noqa


@calc_time_decorator
def calc_base_4(t1, n):
    for _ in range(n):
        r = t1 + t1 + t1 + t1  # noqa


@calc_time_decorator
def calc_base_no_save_2(t1, n):
    for _ in range(n):
        _ = t1 + t1


@calc_time_decorator
def calc_base_no_save_3(t1, n):
    for _ in range(n):
        _ = t1 + t1 + t1


@calc_time_decorator
def calc_base_no_save_4(t1, n):
    for _ in range(n):
        _ = t1 + t1 + t1 + t1


@calc_time_decorator
def calc_ufunc_2(t1, n):
    for _ in range(n):
        r = np.empty(t1.shape)
        np.add(t1, t1, out=r)


@calc_time_decorator
def calc_ufunc_3(t1, n):

    for _ in range(n):
        r = np.empty(t1.shape)
        np.add(t1, t1, out=r)
        np.add(r, t1, out=r)


@calc_time_decorator
def calc_ufunc_4(t1, n):
    for _ in range(n):
        r = np.empty(t1.shape)
        np.add(t1, t1, out=r)
        np.add(r, t1, out=r)
        np.add(r, t1, out=r)


@calc_time_decorator
def calc_ufunc_memory_before_2(t1, n):
    r = np.empty(t1.shape)
    for _ in range(n):
        np.add(t1, t1, out=r)


@calc_time_decorator
def calc_ufunc_memory_before_3(t1, n):
    r = np.empty(t1.shape)
    for _ in range(n):
        np.add(t1, t1, out=r)
        np.add(r, t1, out=r)


@calc_time_decorator
def calc_ufunc_memory_before_4(t1, n):
    r = np.empty(t1.shape)
    for _ in range(n):
        np.add(t1, t1, out=r)
        np.add(r, t1, out=r)
        np.add(r, t1, out=r)


calc_base_2(T1, N)
calc_base_3(T1, N)
calc_base_4(T1, N)

calc_base_no_save_2(T1, N)
calc_base_no_save_3(T1, N)
calc_base_no_save_4(T1, N)

calc_ufunc_2(T1, N)
calc_ufunc_3(T1, N)
calc_ufunc_4(T1, N)

calc_ufunc_memory_before_2(T1, N)
calc_ufunc_memory_before_3(T1, N)
calc_ufunc_memory_before_4(T1, N)
