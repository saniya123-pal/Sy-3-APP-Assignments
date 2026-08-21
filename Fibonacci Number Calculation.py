import timeit

# 1. Naive Recursion
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


# 2. Memoized Recursion (Top-Down DP)
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}

    if n <= 1:
        return n

    if n in memo:
        return memo[n]

    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


# 3. Iterative / Tabulation DP (Bottom-Up)
def fib_dp(n):
    if n <= 1:
        return n

    a, b = 0, 1

    for _ in range(2, n + 1):
        a, b = b, a + b

    return b


# 4. Fast Doubling - O(log n)
def fib_fast_doubling(n):

    def fib_pair(k):
        if k == 0:
            return 0, 1

        a, b = fib_pair(k // 2)

        c = a * (2 * b - a)
        d = a * a + b * b

        if k % 2 == 0:
            return c, d
        else:
            return d, c + d

    return fib_pair(n)[0]


# Main Program
if __name__ == "__main__":

    n = 10

    print("Computing Fibonacci with four approaches:")
    print("[1] Naive recursion :", fib_recursive(n))
    print("[2] Memoized recursion :", fib_memo(n))
    print("[3] Iterative DP :", fib_dp(n))
    print("[4] Fast doubling :", fib_fast_doubling(n))

    print("\nFirst 15 Fibonacci numbers:")
    print([fib_dp(i) for i in range(15)])

    # Timing comparison
    n_big = 28

    t_naive = timeit.timeit(
        lambda: fib_recursive(n_big), number=1
    )

    t_dp = timeit.timeit(
        lambda: fib_dp(n_big), number=1
    )

    print("\nTiming fib(28):")
    print("Naive recursion :", t_naive, "sec")
    print("Iterative DP :", t_dp, "sec")

    # Large n
    n_huge = 100

    print("\nFibonacci(100) via iterative DP :",
          fib_dp(n_huge))

    print("Fibonacci(100) via fast doubling :",
          fib_fast_doubling(n_huge))